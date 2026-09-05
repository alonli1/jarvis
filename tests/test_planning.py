import json
from dataclasses import replace

import pytest
from pydantic import ValidationError

from jarvis.config import load_config
from jarvis.models import ResearchPlan, ResearchTask, TaskPacket
from jarvis.planning import create_task_packets, ordered_tasks, persist_plan, plan_digest
from jarvis.workflows import prepare_computation


def config_for(tmp_path):
    source = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    executable: python\n    ecosystem: python\n"
        "    package: sympy\n    capabilities: [symbolic_algebra, numerical_calculation]\n",
        encoding="utf-8",
    )
    return replace(source, root=tmp_path)


def plan() -> ResearchPlan:
    return ResearchPlan(
        id="PLAN-1",
        research_question="Check a bounded known answer.",
        success_criteria=["Independent check recorded."],
        stop_conditions=["Required evidence unavailable."],
        max_leaf_tasks=2,
        tasks=[
            ResearchTask(id="T001", description="Collect evidence", status="pending"),
            ResearchTask(
                id="T002",
                description="Check algebra",
                status="pending",
                dependencies=["T001"],
                artifacts=["outputs/check.json"],
            ),
        ],
    )


def test_plan_is_deterministic_and_persists_without_model_execution(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(cfg, "Planner test", "python")
    research_plan = plan()

    path = persist_plan(cfg.root, bundle.id, research_plan)
    packets = create_task_packets(cfg.root, bundle.id, research_plan)
    manifest = json.loads((bundle.path / "manifest.json").read_text())

    assert ordered_tasks(research_plan) == ["T001", "T002"]
    assert json.loads(path.read_text())["sha256"] == plan_digest(research_plan)
    assert manifest["plan"] == "plan.json"
    assert [task["id"] for task in manifest["tasks"]] == ["T001", "T002"]
    assert [packet.name for packet in packets] == ["T001.json"]
    assert json.loads(packets[0].read_text())["task"]["id"] == "T001"


def test_plan_rejects_cycles_unknown_dependencies_and_budget_overrun():
    with pytest.raises(ValidationError, match="unknown dependencies"):
        ResearchPlan(
            id="bad",
            research_question="q",
            success_criteria=["done"],
            stop_conditions=["stop"],
            tasks=[
                ResearchTask(id="T001", description="x", status="pending", dependencies=["bad"])
            ],
        )
    with pytest.raises(ValidationError, match="contains a cycle"):
        ResearchPlan(
            id="cycle",
            research_question="q",
            success_criteria=["done"],
            stop_conditions=["stop"],
            tasks=[
                ResearchTask(id="T001", description="x", status="pending", dependencies=["T002"]),
                ResearchTask(id="T002", description="x", status="pending", dependencies=["T001"]),
            ],
        )
    with pytest.raises(ValidationError, match="exceeds max_leaf_tasks"):
        ResearchPlan(
            id="over",
            research_question="q",
            success_criteria=["done"],
            stop_conditions=["stop"],
            max_leaf_tasks=1,
            tasks=[
                ResearchTask(id="T001", description="x", status="pending"),
                ResearchTask(id="T002", description="x", status="pending"),
            ],
        )


def test_task_packet_rejects_absolute_or_parent_artifact_paths():
    task = ResearchTask(id="T001", description="x", status="pending")
    with pytest.raises(ValidationError, match="run-relative"):
        TaskPacket(
            run_id="run",
            task=task,
            dependency_artifacts={"T000": ["../outside.txt"]},
            plan_sha256="0" * 64,
        )


def test_dependent_packet_requires_completed_dependency_and_existing_artifact(
    tmp_path, monkeypatch
):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(cfg, "Planner dependency test", "python")
    artifact = bundle.path / "outputs" / "evidence.json"
    artifact.write_text("{}", encoding="utf-8")
    research_plan = ResearchPlan(
        id="PLAN-2",
        research_question="q",
        success_criteria=["done"],
        stop_conditions=["stop"],
        tasks=[
            ResearchTask(
                id="T001",
                description="source",
                status="completed",
                artifacts=["outputs/evidence.json"],
            ),
            ResearchTask(id="T002", description="check", status="pending", dependencies=["T001"]),
        ],
    )

    packets = create_task_packets(cfg.root, bundle.id, research_plan)

    assert [packet.name for packet in packets] == ["T002.json"]
    packet = json.loads(packets[0].read_text())
    assert packet["dependency_artifacts"] == {"T001": ["outputs/evidence.json"]}
    research_plan.tasks[0].artifacts = ["outputs/missing.json"]
    with pytest.raises(ValueError, match="missing artifact"):
        create_task_packets(cfg.root, bundle.id, research_plan)
