from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from pathlib import Path
import math
import re

import yaml

from .config import Config
from .literature import search_all
from .llm import complete
from .models import LiteratureRecord, NoveltyClaim, NoveltyMatch


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_+\-/]{2,}")
STOP = {
    "the", "and", "for", "from", "with", "that", "this", "into", "using", "our", "are",
    "we", "of", "to", "in", "a", "an", "is", "on", "as", "by", "or", "be", "can",
}


def tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text) if t.lower() not in STOP]


def cosine_text(a: str, b: str) -> float:
    ca, cb = Counter(tokens(a)), Counter(tokens(b))
    if not ca or not cb:
        return 0.0
    dot = sum(ca[k] * cb.get(k, 0) for k in ca)
    na = math.sqrt(sum(v * v for v in ca.values()))
    nb = math.sqrt(sum(v * v for v in cb.values()))
    return dot / (na * nb) if na and nb else 0.0


def keyword_score(claim: NoveltyClaim, paper: LiteratureRecord) -> tuple[float, list[str]]:
    hay = f"{paper.title} {paper.abstract}".lower()
    hits = [kw for kw in claim.keywords if kw.lower() in hay]
    denom = max(1, min(len(claim.keywords), 5))
    return min(1.0, len(hits) / denom), hits


def overlap_score(claim: NoveltyClaim, paper: LiteratureRecord) -> tuple[float, list[str]]:
    text_sim = cosine_text(claim.claim + " " + " ".join(claim.keywords), paper.title + " " + paper.abstract)
    kw_score, kw_hits = keyword_score(claim, paper)
    title_sim = cosine_text(claim.claim, paper.title)
    score = 0.45 * text_sim + 0.35 * kw_score + 0.20 * title_sim
    reasons = [
        f"claim/paper lexical similarity={text_sim:.2f}",
        f"title similarity={title_sim:.2f}",
    ]
    if kw_hits:
        reasons.append("matched keywords: " + ", ".join(kw_hits[:8]))
    return min(1.0, score), reasons


def risk_label(config: Config, score: float) -> str:
    if score >= config.novelty.critical_threshold:
        return "CRITICAL"
    if score >= config.novelty.high_threshold:
        return "HIGH"
    if score >= config.novelty.medium_threshold:
        return "MEDIUM"
    return "LOW"


def load_claims(project_dir: Path) -> tuple[str, list[NoveltyClaim]]:
    path = project_dir / "novelty.yaml"
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    project = data.get("project", project_dir.name)
    claims = [NoveltyClaim.model_validate(c) for c in data.get("claims", [])]
    return project, [c for c in claims if c.status == "active"]


def queries_for_claim(claim: NoveltyClaim) -> list[str]:
    if claim.search_queries:
        return claim.search_queries
    if claim.keywords:
        return [" ".join(claim.keywords[:5])]
    return [claim.claim]


def judge_with_llm(model: str, claim: NoveltyClaim, paper: LiteratureRecord) -> str:
    system = """You are adjudicating possible prior-art overlap for a physics manuscript.
Do not decide legal patent novelty. Compare only scientific contribution overlap.
Return: OVERLAP=[low|medium|high], then 2-5 concise sentences explaining what is shared,
what differs, and what the researchers should inspect in the paper. Do not invent details
not present in the title/abstract."""
    user = f"""MANUSCRIPT CLAIM:\n{claim.claim}\n\nCLAIM KEYWORDS:\n{', '.join(claim.keywords)}\n\nNEW PAPER TITLE:\n{paper.title}\n\nABSTRACT:\n{paper.abstract}\n"""
    return complete(model, system, user, temperature=0.0)


def evaluate_project(
    config: Config,
    project_dir: Path,
    days: int,
    sources: list[str] | None = None,
    judge_model: str | None = None,
) -> tuple[list[NoveltyMatch], dict[str, str]]:
    project, claims = load_claims(project_dir)
    since = date.today() - timedelta(days=days)
    matches: dict[tuple[str, str], NoveltyMatch] = {}
    errors: dict[str, str] = {}
    for claim in claims:
        all_records: list[LiteratureRecord] = []
        for query in queries_for_claim(claim):
            records, source_errors = search_all(config, query, since, sources)
            all_records.extend(records)
            errors.update(source_errors)
        # de-dup within this claim
        unique = {r.stable_key: r for r in all_records}.values()
        for paper in unique:
            score, reasons = overlap_score(claim, paper)
            risk = risk_label(config, score)
            if risk == "LOW":
                continue
            match = NoveltyMatch(
                project=project,
                claim_id=claim.id,
                claim=claim.claim,
                paper=paper,
                score=score,
                risk=risk,
                reasons=reasons,
            )
            if judge_model and risk in {"HIGH", "CRITICAL"}:
                try:
                    match.judge_assessment = judge_with_llm(judge_model, claim, paper)
                except Exception as exc:
                    match.judge_assessment = f"LLM judge failed: {type(exc).__name__}: {exc}"
            matches[(claim.id, paper.stable_key)] = match
    ranked = sorted(matches.values(), key=lambda m: m.score, reverse=True)
    return ranked, errors


def render_markdown(matches: list[NoveltyMatch], errors: dict[str, str]) -> str:
    lines = ["# Literature novelty watch", ""]
    if not matches:
        lines += ["No medium-or-higher overlap candidates were found in this run.", ""]
    for m in matches:
        paper = m.paper
        lines += [
            f"## {m.risk} — {m.claim_id} — score {m.score:.2f}",
            "",
            f"**Paper:** {paper.title}",
            f"**Source:** {paper.source}",
            f"**Published:** {paper.published or 'unknown'}",
            f"**URL:** {paper.url or 'unavailable'}",
            "",
            "**Claim under watch**",
            "",
            m.claim,
            "",
            "**Why it was flagged**",
            "",
        ]
        lines += [f"- {reason}" for reason in m.reasons]
        if m.judge_assessment:
            lines += ["", "**LLM adjudication**", "", m.judge_assessment]
        lines.append("")
    if errors:
        lines += ["## Source errors", ""]
        lines += [f"- **{name}:** {message}" for name, message in sorted(errors.items())]
        lines.append("")
    lines += [
        "---",
        "This report is triage, not proof of scientific novelty. Inspect flagged papers directly before changing a manuscript claim.",
        "",
    ]
    return "\n".join(lines)
