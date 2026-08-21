from __future__ import annotations

from datetime import date
from enum import IntEnum
from typing import Any
from pydantic import BaseModel, Field


class Visibility(IntEnum):
    public = 0
    group = 1
    confidential = 2

    @classmethod
    def parse(cls, value: str) -> "Visibility":
        return cls[value]


class Chunk(BaseModel):
    id: str
    text: str
    source_path: str
    title: str | None = None
    page: int | None = None
    section: str | None = None
    visibility: str = "public"
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
