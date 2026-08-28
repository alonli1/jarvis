from __future__ import annotations

from datetime import date

import httpx

from ..config import Config
from ..models import LiteratureRecord
from .arxiv import ArxivSource
from .inspire import InspireSource
from .openalex import OpenAlexSource
from .semantic_scholar import SemanticScholarSource


def _source_error(exc: Exception) -> str:
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        if status == 429:
            return "rate limited (HTTP 429); retry later or configure this source's API key"
        return f"HTTP {status} from literature provider"
    return f"{type(exc).__name__}: {exc}"


def source_registry(config: Config):
    ua = config.literature.user_agent
    return {
        "arxiv": ArxivSource(ua),
        "inspire": InspireSource(ua),
        "openalex": OpenAlexSource(ua),
        "semantic_scholar": SemanticScholarSource(ua),
    }


def deduplicate(records: list[LiteratureRecord]) -> list[LiteratureRecord]:
    best: dict[str, LiteratureRecord] = {}
    for record in records:
        key = record.stable_key
        if key not in best:
            best[key] = record
            continue
        current = best[key]
        # Prefer the record with the richer abstract; keep citation count if available.
        if len(record.abstract) > len(current.abstract):
            if record.citation_count is None:
                record.citation_count = current.citation_count
            best[key] = record
        elif current.citation_count is None and record.citation_count is not None:
            current.citation_count = record.citation_count
    return sorted(best.values(), key=lambda r: r.published or date.min, reverse=True)


def search_all(
    config: Config,
    query: str,
    since: date,
    sources: list[str] | None = None,
) -> tuple[list[LiteratureRecord], dict[str, str]]:
    registry = source_registry(config)
    names = sources or list(registry)
    records: list[LiteratureRecord] = []
    errors: dict[str, str] = {}
    for name in names:
        if name not in registry:
            errors[name] = "unknown source"
            continue
        try:
            records.extend(
                registry[name].search(query, since, config.literature.max_results_per_query)
            )
        except Exception as exc:  # noqa: BLE001 - one source outage must not kill the watch
            errors[name] = _source_error(exc)
    return deduplicate(records), errors
