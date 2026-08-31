from __future__ import annotations

from dataclasses import dataclass

from .models import ResearchPlan


@dataclass(frozen=True)
class AutonomyPolicy:
    max_tasks: int = 4
    allowed_kinds: frozenset[str] = frozenset({"literature", "derivation", "computation", "review"})
    forbidden_terms: frozenset[str] = frozenset(
        {"publish", "manuscript edit", "edit manuscript", "submit"}
    )


@dataclass(frozen=True)
class AutonomyAdmission:
    admitted: bool
    reasons: tuple[str, ...]


def admit_plan(plan: ResearchPlan, policy: AutonomyPolicy | None = None) -> AutonomyAdmission:
    policy = policy or AutonomyPolicy()
    reasons = []
    if len(plan.tasks) > policy.max_tasks:
        reasons.append("task budget exceeds autonomy policy")
    question = plan.research_question.lower()
    if any(term in question for term in policy.forbidden_terms):
        reasons.append("research question requests forbidden external action")
    for task in plan.tasks:
        if task.kind not in policy.allowed_kinds:
            reasons.append(f"task {task.id} has disallowed kind: {task.kind}")
        text = f"{task.description} {task.objective or ''}".lower()
        if any(term in text for term in policy.forbidden_terms):
            reasons.append(f"task {task.id} requests forbidden external action")
    if not plan.stop_conditions:
        reasons.append("plan lacks stop conditions")
    return AutonomyAdmission(not reasons, tuple(reasons))
