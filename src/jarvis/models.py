from __future__ import annotations

from datetime import date, datetime
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
    dependencies: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)


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
