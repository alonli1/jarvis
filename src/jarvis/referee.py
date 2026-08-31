from __future__ import annotations

from pydantic import BaseModel, Field


class RefereeFinding(BaseModel):
    id: str
    severity: str
    claim_id: str | None = None
    observation: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str


class RefereeReport(BaseModel):
    manuscript: str
    findings: list[RefereeFinding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ResearchIdea(BaseModel):
    id: str
    title: str
    evidence: list[str] = Field(min_length=1)
    gap: str
    assumptions: list[str] = Field(default_factory=list)
    falsifier: str
    cheapest_decisive_test: str
    novelty_scope: str


def render_referee_report(report: RefereeReport) -> str:
    lines = [f"# Technical review — {report.manuscript}", ""]
    for finding in report.findings:
        lines += [f"## {finding.id} — {finding.severity}", "", finding.observation, ""]
        lines += [f"- Evidence: {item}" for item in finding.evidence]
        lines += [f"- Recommendation: {finding.recommendation}", ""]
    lines += ["## Limitations", "", *(f"- {item}" for item in report.limitations)]
    return "\n".join(lines).rstrip() + "\n"
