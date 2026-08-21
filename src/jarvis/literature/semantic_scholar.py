from __future__ import annotations

from datetime import date
import os

import httpx

from .base import LiteratureSource
from ..models import LiteratureRecord


class SemanticScholarSource(LiteratureSource):
    name = "semantic_scholar"
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def search(self, query: str, since: date, limit: int) -> list[LiteratureRecord]:
        headers = {"User-Agent": self.user_agent}
        if os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
            headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
        params = {
            "query": query.replace("-", " "),
            "limit": min(limit, 100),
            "publicationDateOrYear": f"{since.isoformat()}:",
            "fields": "title,abstract,authors,publicationDate,url,externalIds,citationCount",
        }
        with httpx.Client(timeout=30, headers=headers) as client:
            response = client.get(self.endpoint, params=params)
            response.raise_for_status()
            data = response.json()
        out: list[LiteratureRecord] = []
        for item in data.get("data", []):
            ext = item.get("externalIds") or {}
            pub = None
            if item.get("publicationDate"):
                try:
                    pub = date.fromisoformat(item["publicationDate"])
                except ValueError:
                    pass
            out.append(
                LiteratureRecord(
                    source=self.name,
                    source_id=item.get("paperId", ""),
                    title=item.get("title") or "",
                    authors=[a.get("name", "") for a in item.get("authors", []) if a.get("name")],
                    abstract=item.get("abstract") or "",
                    published=pub,
                    url=item.get("url"),
                    doi=ext.get("DOI"),
                    arxiv_id=ext.get("ArXiv"),
                    citation_count=item.get("citationCount"),
                )
            )
        return out
