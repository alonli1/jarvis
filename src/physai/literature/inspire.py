from __future__ import annotations

from datetime import date

import httpx

from .base import LiteratureSource
from ..models import LiteratureRecord


class InspireSource(LiteratureSource):
    name = "inspire"
    endpoint = "https://inspirehep.net/api/literature"

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def search(self, query: str, since: date, limit: int) -> list[LiteratureRecord]:
        # INSPIRE's query syntax supports date ranges and free text.
        inspire_query = f"({query}) and date {since.isoformat()}->"
        with httpx.Client(timeout=30, headers={"User-Agent": self.user_agent}) as client:
            response = client.get(
                self.endpoint,
                params={"q": inspire_query, "size": limit, "sort": "mostrecent"},
            )
            response.raise_for_status()
            data = response.json()
        out: list[LiteratureRecord] = []
        for hit in data.get("hits", {}).get("hits", []):
            md = hit.get("metadata", {})
            titles = md.get("titles") or []
            title = titles[0].get("title", "") if titles else ""
            abstracts = md.get("abstracts") or []
            abstract = abstracts[0].get("value", "") if abstracts else ""
            arxiv_eprints = md.get("arxiv_eprints") or []
            arxiv_id = arxiv_eprints[0].get("value") if arxiv_eprints else None
            dois = md.get("dois") or []
            doi = dois[0].get("value") if dois else None
            pub = None
            earliest = md.get("earliest_date")
            if earliest:
                try:
                    pub = date.fromisoformat(earliest[:10])
                except ValueError:
                    pass
            authors = [a.get("full_name", "") for a in md.get("authors", []) if a.get("full_name")]
            control = str(md.get("control_number", hit.get("id", "")))
            out.append(
                LiteratureRecord(
                    source=self.name,
                    source_id=control,
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    published=pub,
                    url=f"https://inspirehep.net/literature/{control}",
                    doi=doi,
                    arxiv_id=arxiv_id,
                    citation_count=(md.get("citation_count") if isinstance(md.get("citation_count"), int) else None),
                )
            )
        return out
