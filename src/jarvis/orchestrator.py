from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

from .models import ModelUsage, ProvisionalArtifact, ResearchPlan, TaskPacket
from .planning import create_task_packets, plan_digest
from .workflows import (
    _run_path,
    _write_json,
    import_provisional_artifact,
    load_manifest,
    record_model_usage,
)


@dataclass(frozen=True)
class OrchestrationBatch:
    run_id: str
    packets: tuple[Path, ...]
    fresh_context_required: bool = True


def schedule_ready_tasks(root: Path, run_id: str, plan: ResearchPlan) -> OrchestrationBatch:
    """Materialize ready task packets; execution stays with a separate fresh context."""
    return OrchestrationBatch(run_id=run_id, packets=tuple(create_task_packets(root, run_id, plan)))


def load_task_packet(path: Path) -> TaskPacket:
    return TaskPacket.model_validate_json(path.read_text(encoding="utf-8"))


def _packet(root: Path, run_id: str, task_id: str) -> tuple[Path, TaskPacket]:
    if not task_id or Path(task_id).name != task_id:
        raise ValueError("Task id must be a single path component")
    run = _run_path(SimpleNamespace(root=root), run_id)
    path = run / "tasks" / f"{task_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Unknown task packet: {task_id}")
    packet = load_task_packet(path)
    if packet.run_id != run_id or packet.task.id != task_id:
        raise ValueError("Task packet identity does not match its requested run and task")
    plan_path = run / "plan.json"
    if not plan_path.is_file():
        raise FileNotFoundError("Task packet requires a persisted plan")
    plan = ResearchPlan.model_validate_json(plan_path.read_text(encoding="utf-8"))
    if packet.plan_sha256 != plan_digest(plan):
        raise ValueError("Task packet no longer matches the persisted plan")
    return path, packet


def export_host_task(root: Path, run_id: str, task_id: str) -> Path:
    """Export a validated packet for a fresh IDE or extension-host context."""
    packet_path, packet = _packet(root, run_id, task_id)
    run = _run_path(SimpleNamespace(root=root), run_id)
    output = run / "host_dispatch" / f"{task_id}.json"
    _write_json(
        output,
        {
            "version": 1,
            "packet": packet.model_dump(mode="json"),
            "packet_path": str(packet_path.relative_to(run)),
            "host_contract": {
                "fresh_context_required": True,
                "result_must_remain_provisional": True,
                "forbidden": ["claim promotion", "task completion", "reviewer-artifact access"],
            },
        },
    )
    manifest_path = run / "manifest.json"
    manifest = load_manifest(manifest_path)
    relative = str(output.relative_to(run))
    if relative not in manifest["artifacts"]:
        manifest["artifacts"].append(relative)
        _write_json(manifest_path, manifest)
    return output


def import_host_task_result(
    root: Path,
    run_id: str,
    task_id: str,
    source: Path,
    host: str,
    *,
    fresh_context: bool,
    provider: str | None = None,
    model: str | None = None,
) -> ProvisionalArtifact:
    """Import a host result without interpreting it as scientific success."""
    if not fresh_context:
        raise ValueError("Host result import requires a fresh-context declaration")
    if not host.strip() or "/" in host or "\\" in host:
        raise ValueError("Host must be a non-empty label, not a path")
    if bool(provider) != bool(model):
        raise ValueError("Provider and model must be recorded together")
    packet_path, _ = _packet(root, run_id, task_id)
    artifact = import_provisional_artifact(
        SimpleNamespace(root=root),
        run_id,
        source,
        f"host:{host}",
        f"host-{task_id}",
        role=f"host:{host}",
    )
    if provider and model:
        record_model_usage(
            SimpleNamespace(root=root),
            run_id,
            ModelUsage(provider=provider, model=model, role=f"host:{host}"),
        )
    run = _run_path(SimpleNamespace(root=root), run_id)
    manifest_path = run / "manifest.json"
    manifest = load_manifest(manifest_path)
    manifest["decision_log"].append(
        {
            "id": f"host-dispatch-{task_id}",
            "decision": "host result imported as provisional",
            "rationale": f"Fresh context declared by host:{host}.",
            "artifacts": [str(packet_path.relative_to(run)), artifact.path],
        }
    )
    _write_json(manifest_path, manifest)
    return artifact
