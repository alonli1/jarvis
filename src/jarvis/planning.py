from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from .models import ResearchPlan, TaskPacket
from .workflows import _run_path, _write_json, load_manifest


def plan_digest(plan: ResearchPlan) -> str:
    encoded = json.dumps(plan.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def ordered_tasks(plan: ResearchPlan) -> list[str]:
    dependencies = {task.id: set(task.dependencies) for task in plan.tasks}
    ordered = []
    while dependencies:
        ready = [task_id for task_id in dependencies if dependencies[task_id] <= set(ordered)]
        for task_id in ready:
            ordered.append(task_id)
            del dependencies[task_id]
    return ordered


def persist_plan(root: Path, run_id: str, plan: ResearchPlan) -> Path:
    run = _run_path(SimpleNamespace(root=root), run_id)
    manifest_path = run / "manifest.json"
    manifest = load_manifest(manifest_path)
    if manifest["version"] != 2:
        raise ValueError("Research plans require a Manifest v2 run")
    path = run / "plan.json"
    _write_json(path, {**plan.model_dump(mode="json"), "sha256": plan_digest(plan)})
    manifest["plan"] = str(path.relative_to(run))
    manifest["tasks"] = [task.model_dump(mode="json") for task in plan.tasks]
    if manifest["plan"] not in manifest["artifacts"]:
        manifest["artifacts"].append(manifest["plan"])
    _write_json(manifest_path, manifest)
    return path


def create_task_packets(root: Path, run_id: str, plan: ResearchPlan) -> list[Path]:
    run = _run_path(SimpleNamespace(root=root), run_id)
    task_by_id = {task.id: task for task in plan.tasks}
    packets = []
    for task_id in ordered_tasks(plan):
        task = task_by_id[task_id]
        if task.status in {"complete", "completed"}:
            continue
        dependencies = [task_by_id[dependency] for dependency in task.dependencies]
        if any(dependency.status not in {"complete", "completed"} for dependency in dependencies):
            continue
        dependency_artifacts = {}
        for dependency in dependencies:
            paths = []
            for artifact in dependency.artifacts:
                path = (run / artifact).resolve()
                try:
                    path.relative_to(run)
                except ValueError as exc:
                    raise ValueError("Task artifacts must remain within the run") from exc
                if not path.is_file():
                    raise ValueError(
                        f"Completed dependency {dependency.id!r} is missing artifact: {artifact}"
                    )
                paths.append(artifact)
            dependency_artifacts[dependency.id] = paths
        packet = TaskPacket(
            run_id=run_id,
            task=task,
            dependency_artifacts=dependency_artifacts,
            plan_sha256=plan_digest(plan),
        )
        path = run / "tasks" / f"{task.id}.json"
        payload = packet.model_dump(mode="json")
        if path.exists() and json.loads(path.read_text(encoding="utf-8")) != payload:
            raise FileExistsError(f"Task packet already exists with different content: {task.id}")
        _write_json(path, payload)
        packets.append(path)
    return packets
