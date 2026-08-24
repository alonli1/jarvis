from __future__ import annotations

import os
import re
from datetime import UTC, datetime
from pathlib import Path

import httpx
import yaml
from pypdf import PdfReader

ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = "title,year,citationCount,referenceCount,externalIds,references.paperId"
ARXIV = re.compile(
    r"(?:arxiv\s*:\s*|arxiv\.org/(?:abs|pdf)/)"
    r"(\d{4}\.\d{4,5}|(?:astro-ph|cond-mat|gr-qc|hep-ex|hep-lat|hep-ph|hep-th|"
    r"math-ph|nucl-ex|nucl-th|quant-ph)/\d{7})",
    re.IGNORECASE,
)
DOI = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)


def paper_identifier(reference: dict) -> str | None:
    if reference.get("arxiv"):
        return f"ARXIV:{reference['arxiv']}"
    if reference.get("doi"):
        return f"DOI:{reference['doi']}"
    return None


def manifest_identifiers(reference: dict) -> list[str]:
    identifiers = []
    if reference.get("arxiv"):
        identifiers.append(f"arxiv:{str(reference['arxiv']).lower()}")
    if reference.get("doi"):
        identifiers.append(f"doi:{str(reference['doi']).lower()}")
    return identifiers


def fetch_citations(references: list[dict], client: httpx.Client) -> tuple[dict, list[str]]:
    selected = [(reference, paper_identifier(reference)) for reference in references]
    selected = [(reference, identifier) for reference, identifier in selected if identifier]
    response = client.post(
        ENDPOINT,
        params={"fields": FIELDS},
        json={"ids": [identifier for _, identifier in selected]},
    )
    response.raise_for_status()
    results = response.json()
    if not isinstance(results, list) or len(results) != len(selected):
        raise ValueError("Semantic Scholar returned an unexpected batch response")

    papers, unresolved = {}, []
    for (reference, _), item in zip(selected, results, strict=True):
        if not item or not item.get("paperId"):
            unresolved.append(reference["id"])
            continue
        papers[reference["id"]] = {
            "semantic_scholar_id": item["paperId"],
            "identifiers": [f"s2:{item['paperId']}"],
            "citation_count": item.get("citationCount"),
            "reference_count": item.get("referenceCount"),
            "references": [
                f"s2:{cited['paperId']}"
                for cited in item.get("references") or []
                if cited and cited.get("paperId")
            ],
        }
    unresolved.extend(
        reference["id"] for reference in references if not paper_identifier(reference)
    )
    return papers, unresolved


def sync_citations(root: Path, user_agent: str) -> tuple[Path, int, int]:
    manifest = yaml.safe_load(
        (root / "knowledge" / "references.yaml").read_text(encoding="utf-8")
    )
    headers = {"User-Agent": user_agent}
    if os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    with httpx.Client(timeout=90, headers=headers) as client:
        papers, unresolved = fetch_citations(manifest["references"], client)
    path = root / "literature" / "citations.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "source": "Semantic Scholar Academic Graph API",
                "source_url": "https://api.semanticscholar.org/api-docs/graph",
                "updated_at": datetime.now(UTC).isoformat(),
                "papers": papers,
                "unresolved": sorted(unresolved),
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path, len(papers), len(unresolved)


def _clean_doi(value: str) -> str:
    return value.rstrip(".,;:)]}").lower()


def sync_pdf_citations(root: Path) -> tuple[Path, int, int]:
    manifest = yaml.safe_load(
        (root / "knowledge" / "references.yaml").read_text(encoding="utf-8")
    )
    references = manifest["references"]
    by_id = {reference["id"]: reference for reference in references}
    papers = {}
    sidecars = sorted((root / "knowledge").glob("*/*.pdf.meta.yaml"))
    for sidecar in sidecars:
        metadata = yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}
        reference_id = metadata.get("reference_id")
        pdf = sidecar.with_name(sidecar.name.removesuffix(".meta.yaml"))
        if reference_id not in by_id or not pdf.exists():
            continue
        text = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)
        found = {f"arxiv:{match.lower()}" for match in ARXIV.findall(text)}
        found.update(f"doi:{_clean_doi(match)}" for match in DOI.findall(text))
        own = set(manifest_identifiers(by_id[reference_id]))
        papers[reference_id] = {
            "identifiers": sorted(own),
            "citation_count": None,
            "reference_count": len(found - own),
            "references": sorted(found - own),
        }
    path = root / "literature" / "citations.yaml"
    unresolved = sorted(set(by_id) - set(papers))
    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "source": "Local PDF arXiv/DOI extraction",
                "updated_at": datetime.now(UTC).isoformat(),
                "papers": papers,
                "unresolved": unresolved,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path, len(papers), len(unresolved)
