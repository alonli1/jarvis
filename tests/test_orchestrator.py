import json
from dataclasses import replace

import pytest

from jarvis.config import load_config
from jarvis.models import ResearchPlan, ResearchTask
from jarvis.orchestrator import (
    export_host_task,
    import_host_task_result,
    load_task_packet,
    schedule_ready_tasks,
)
from jarvis.planning import persist_plan
from jarvis.workflows import prepare_computation


def test_scheduler_materializes_fresh_context_packets(tmp_path, monkeypatch):
    config = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    executable: python\n    ecosystem: python\n"
        "    package: sympy\n    capabilities: [symbolic_algebra, numerical_calculation]\n",
        encoding="utf-8",
    )
    config = replace(config, root=tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(config, "Schedule test", "python")
    plan = ResearchPlan(
        id="PLAN",
        research_question="q",
        success_criteria=["done"],
        stop_conditions=["stop"],
        tasks=[ResearchTask(id="T001", description="collect", status="pending", kind="literature")],
    )

    batch = schedule_ready_tasks(config.root, bundle.id, plan)
    packet = load_task_packet(batch.packets[0])

    assert batch.fresh_context_required is True
    assert packet.task.id == "T001"
    assert packet.task.kind == "literature"


def test_host_dispatch_exports_a_packet_and_imports_only_provisional_output(tmp_path, monkeypatch):
    config = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    executable: python\n    ecosystem: python\n"
        "    package: sympy\n    capabilities: [symbolic_algebra, numerical_calculation]\n",
        encoding="utf-8",
    )
    config = replace(config, root=tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(config, "Host dispatch", "python")
    plan = ResearchPlan(
        id="PLAN",
        research_question="q",
        success_criteria=["done"],
        stop_conditions=["stop"],
        tasks=[ResearchTask(id="T001", description="collect", status="pending", kind="literature")],
    )
    persist_plan(config.root, bundle.id, plan)
    schedule_ready_tasks(config.root, bundle.id, plan)

    handoff = export_host_task(config.root, bundle.id, "T001")
    payload = json.loads(handoff.read_text())
    result = tmp_path / "host-result.md"
    result.write_text("Untrusted host output.\n", encoding="utf-8")
    artifact = import_host_task_result(
        config.root,
        bundle.id,
        "T001",
        result,
        "codex",
        fresh_context=True,
        provider="ide",
        model="codex",
    )
    manifest = json.loads((bundle.path / "manifest.json").read_text())

    assert payload["packet"]["task"]["id"] == "T001"
    assert payload["host_contract"]["result_must_remain_provisional"] is True
    assert artifact.path == "provisional/host-T001/host-result.md"
    assert manifest["tasks"][0]["status"] == "pending"
    assert manifest["claims"] == []
    assert manifest["model_usage"][0]["provider"] == "ide"
    assert manifest["decision_log"][0]["decision"] == "host result imported as provisional"


def test_host_dispatch_rejects_non_fresh_import_without_mutating_a_run(tmp_path, monkeypatch):
    config = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    executable: python\n    ecosystem: python\n"
        "    package: sympy\n    capabilities: [symbolic_algebra, numerical_calculation]\n",
        encoding="utf-8",
    )
    config = replace(config, root=tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(config, "Host rejection", "python")
    plan = ResearchPlan(
        id="PLAN",
        research_question="q",
        success_criteria=["done"],
        stop_conditions=["stop"],
        tasks=[ResearchTask(id="T001", description="collect", status="pending")],
    )
    persist_plan(config.root, bundle.id, plan)
    schedule_ready_tasks(config.root, bundle.id, plan)
    result = tmp_path / "host-result.md"
    result.write_text("output\n", encoding="utf-8")
    manifest_path = bundle.path / "manifest.json"
    before = manifest_path.read_bytes()

    with pytest.raises(ValueError, match="fresh-context"):
        import_host_task_result(
            config.root, bundle.id, "T001", result, "codex", fresh_context=False
        )
    assert manifest_path.read_bytes() == before
