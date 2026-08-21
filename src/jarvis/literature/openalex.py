from __future__ import annotations

from datetime import date
import os

import httpx

from .base import LiteratureSource
from ..models import LiteratureRecord


class OpenAlexSource(LiteratureSource):
    name = "openalex"
    endpoint = "https://api.openalex.org/works"

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def search(self, query: str, since: date, limit: int) -> list[LiteratureRecord]:
        params = {
            "search": query,
            "filter": f"from_publication_date:{since.isoformat()}",
            "per_page": min(limit, 100),
            "sort": "publication_date:desc",
        }
        if os.getenv("OPENALEX_API_KEY"):
            params["api_key"] = os.environ["OPENALEX_API_KEY"]
        with httpx.Client(timeout=30, headers={"User-Agent": self.user_agent}) as client:
            response = client.get(self.endpoint, params=params)
            response.raise_for_status()
            data = response.json()
        out: list[LiteratureRecord] = []
        for work in data.get("results", []):
            ids = work.get("ids") or {}
            doi = ids.get("doi") or work.get("doi")
            if doi and doi.startswith("https://doi.org/"):
                doi = doi.removeprefix("https://doi.org/")
            arxiv_id = None
            for key, value in ids.items():
                if "arxiv" in key.lower() and value:
                    arxiv_id = str(value).rsplit("/", 1)[-1]
            pub = None
            if work.get("publication_date"):
                try:
                    pub = date.fromisoformat(work["publication_date"])
                except ValueError:
                    pass
            authors = []
            for auth in work.get("authorships", []):
                name = (auth.get("author") or {}).get("display_name")
                if name:
                    authors.append(name)
            out.append(
                LiteratureRecord(
                    source=self.name,
                    source_id=str(work.get("id", "")).rsplit("/", 1)[-1],
                    title=work.get("title") or work.get("display_name") or "",
                    authors=authors,
                    abstract="",
                    published=pub,
                    url=work.get("doi") or work.get("id"),
                    doi=doi,
                    arxiv_id=arxiv_id,
                    citation_count=work.get("cited_by_count"),
                )
            )
        return out
