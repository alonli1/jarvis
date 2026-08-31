from dataclasses import replace

from jarvis.config import load_config
from jarvis.models import ResearchPlan, ResearchTask
from jarvis.orchestrator import load_task_packet, schedule_ready_tasks
from jarvis.workflows import prepare_computation


def test_scheduler_materializes_fresh_context_packets(tmp_path, monkeypatch):
    config = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    executable: python\n    ecosystem: python\n    package: sympy\n",
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
