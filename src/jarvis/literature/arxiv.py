from __future__ import annotations

from datetime import date, datetime, time, timezone
import re

import feedparser
import httpx

from .base import LiteratureSource
from ..models import LiteratureRecord


class ArxivSource(LiteratureSource):
    name = "arxiv"
    endpoint = "https://export.arxiv.org/api/query"

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def search(self, query: str, since: date, limit: int) -> list[LiteratureRecord]:
        start = datetime.combine(since, time.min, tzinfo=timezone.utc).strftime("%Y%m%d%H%M")
        end = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
        cleaned = re.sub(r'["()]', ' ', query)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        terms = [t for t in cleaned.split(" ") if len(t) > 2][:8]
        text_query = " AND ".join(f"all:{t}" for t in terms) or "all:physics"
        search_query = f"({text_query}) AND submittedDate:[{start} TO {end}]"
        with httpx.Client(timeout=30, headers={"User-Agent": self.user_agent}) as client:
            response = client.get(
                self.endpoint,
                params={
                    "search_query": search_query,
                    "start": 0,
                    "max_results": limit,
                    "sortBy": "submittedDate",
                    "sortOrder": "descending",
                },
            )
            response.raise_for_status()
        feed = feedparser.loads(response.text)
        records: list[LiteratureRecord] = []
        for entry in feed.entries:
            arxiv_id = entry.id.rsplit("/", 1)[-1].split("v", 1)[0]
            published = None
            if getattr(entry, "published_parsed", None):
                p = entry.published_parsed
                published = date(p.tm_year, p.tm_mon, p.tm_mday)
            doi = getattr(entry, "arxiv_doi", None)
            records.append(
                LiteratureRecord(
                    source=self.name,
                    source_id=arxiv_id,
                    title=" ".join(entry.title.split()),
                    authors=[a.name for a in getattr(entry, "authors", [])],
                    abstract=" ".join(getattr(entry, "summary", "").split()),
                    published=published,
                    url=entry.id,
                    doi=doi,
                    arxiv_id=arxiv_id,
                )
            )
        return records
