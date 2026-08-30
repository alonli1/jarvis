from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class Chunk(BaseModel):
    id: str
    text: str
    source_path: str
    title: str | None = None
    page: int | None = None
    section: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchHit(BaseModel):
    chunk: Chunk
    score: float


class LiteratureRecord(BaseModel):
    source: str
    source_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    abstract: str = ""
    published: date | None = None
    url: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    citation_count: int | None = None
    raw: dict[str, Any] = Field(default_factory=dict, exclude=True)

    @property
    def stable_key(self) -> str:
        if self.doi:
            return f"doi:{self.doi.lower()}"
        if self.arxiv_id:
            return f"arxiv:{self.arxiv_id.lower()}"
        return f"{self.source}:{self.source_id}"


class NoveltyClaim(BaseModel):
    id: str
    claim: str
    keywords: list[str] = Field(default_factory=list)
    search_queries: list[str] = Field(default_factory=list)
    status: str = "active"


class NoveltyMatch(BaseModel):
    project: str
    claim_id: str
    claim: str
    paper: LiteratureRecord
    score: float
    risk: str
    reasons: list[str]
    judge_assessment: str | None = None


class EvidenceReference(BaseModel):
    kind: str
    reference: str
    locator: str | None = None


class ScientificClaim(BaseModel):
    id: str
    statement: str
    kind: str
    status: Literal[
        "candidate",
        "source_grounded",
        "derived_once",
        "computed_once",
        "independently_checked",
        "contradicted",
        "ai_verified",
        "human_verified",
        "published_or_external",
        "retired",
    ]
    scope: dict[str, Any] = Field(default_factory=dict)
    conventions: dict[str, Any] = Field(default_factory=dict)
    evidence: list[EvidenceReference] = Field(default_factory=list)
    known_issues: list[str] = Field(default_factory=list)
    created_by: str
    human_reviewed: bool = False

    @model_validator(mode="after")
    def human_verification_requires_review(self) -> ScientificClaim:
        if self.status == "human_verified" and not self.human_reviewed:
            raise ValueError("human_verified claims require human_reviewed=True")
        return self


class VerificationRecord(BaseModel):
    id: str
    method: str
    outcome: str
    artifact: str
    notes: str | None = None
    claim_id: str | None = None
    independent: bool = False


class ModelUsage(BaseModel):
    provider: str
    model: str
    role: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_ms: int | None = None
    estimated_cost: float | None = None


class ProvisionalArtifact(BaseModel):
    id: str
    source_label: str
    role: str | None = None
    path: str
    sha256: str
    imported_at: datetime


class ResearchTask(BaseModel):
    id: str
    description: str
    status: str
    kind: str = "analysis"
    objective: str | None = None
    dependencies: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    verification_method: str | None = None
    budget_units: int = Field(default=1, ge=1)
    stop_conditions: list[str] = Field(default_factory=list)
    route: dict[str, Any] = Field(default_factory=dict)


class ResearchPlan(BaseModel):
    id: str
    research_question: str
    success_criteria: list[str] = Field(min_length=1)
    conventions: dict[str, Any] = Field(default_factory=dict)
    tasks: list[ResearchTask] = Field(min_length=1)
    stop_conditions: list[str] = Field(min_length=1)
    max_leaf_tasks: int = Field(default=12, ge=1)

    @model_validator(mode="after")
    def valid_dependency_graph(self) -> ResearchPlan:
        task_ids = [task.id for task in self.tasks]
        if len(set(task_ids)) != len(task_ids):
            raise ValueError("ResearchPlan task ids must be unique")
        known = set(task_ids)
        for task in self.tasks:
            if task.id in task.dependencies:
                raise ValueError(f"ResearchPlan task {task.id!r} cannot depend on itself")
            unknown = set(task.dependencies) - known
            if unknown:
                raise ValueError(
                    f"ResearchPlan task {task.id!r} has unknown dependencies: {sorted(unknown)}"
                )
        if len(self.tasks) > self.max_leaf_tasks:
            raise ValueError("ResearchPlan exceeds max_leaf_tasks")
        remaining = {task.id: set(task.dependencies) for task in self.tasks}
        resolved = set()
        while remaining:
            ready = {
                task_id for task_id, dependencies in remaining.items() if dependencies <= resolved
            }
            if not ready:
                raise ValueError("ResearchPlan dependency graph contains a cycle")
            resolved.update(ready)
            for task_id in ready:
                del remaining[task_id]
        return self


class TaskPacket(BaseModel):
    run_id: str
    task: ResearchTask
    dependency_artifacts: dict[str, list[str]] = Field(default_factory=dict)
    plan_sha256: str

    @model_validator(mode="after")
    def contains_only_run_relative_artifacts(self) -> TaskPacket:
        for artifacts in self.dependency_artifacts.values():
            for artifact in artifacts:
                path = Path(artifact)
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("TaskPacket artifacts must be run-relative")
                if any("review" in part.lower() for part in path.parts):
                    raise ValueError("TaskPacket cannot include reviewer artifacts")
        return self


class DecisionRecord(BaseModel):
    id: str
    decision: str
    rationale: str
    artifacts: list[str] = Field(default_factory=list)


class ScientificFlag(BaseModel):
    code: str
    severity: str
    message: str
    artifact: str | None = None
