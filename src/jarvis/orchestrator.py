from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import ResearchPlan, TaskPacket
from .planning import create_task_packets


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
