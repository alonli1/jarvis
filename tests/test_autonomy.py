from jarvis.autonomy import AutonomyPolicy, admit_plan
from jarvis.models import ResearchPlan, ResearchTask


def plan(task: ResearchTask, question="Check a bounded identity"):
    return ResearchPlan(
        id="P",
        research_question=question,
        success_criteria=["check recorded"],
        stop_conditions=["evidence unavailable"],
        tasks=[task],
    )


def test_bounded_autonomy_admits_only_allowed_plans():
    assert admit_plan(
        plan(ResearchTask(id="T1", description="Derive", status="pending", kind="derivation"))
    ).admitted
    denied = admit_plan(
        plan(ResearchTask(id="T1", description="Edit manuscript", status="pending", kind="review"))
    )
    assert not denied.admitted
    assert "forbidden external action" in denied.reasons[0]
    kind_denied = admit_plan(
        plan(ResearchTask(id="T1", description="x", status="pending", kind="publication")),
        AutonomyPolicy(),
    )
    assert not kind_denied.admitted
