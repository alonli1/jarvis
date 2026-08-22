from __future__ import annotations

import re
from pathlib import Path

import yaml


def normalize_tag(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def load_taxonomy(root: Path) -> dict[str, dict]:
    path = root / "topics" / "taxonomy.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    tags = data.get("research_tags", {})
    if not isinstance(tags, dict):
        raise TypeError(f"{path} must contain a research_tags mapping")
    return tags


def classify_tags(
    raw_tags: list[str], taxonomy: dict[str, dict], text: str = ""
) -> list[str]:
    normalized = {normalize_tag(tag) for tag in raw_tags if tag}
    searchable = text.lower()
    matches: list[str] = []
    for name, rule in taxonomy.items():
        any_tags = {normalize_tag(tag) for tag in rule.get("any", [])}
        all_tags = {normalize_tag(tag) for tag in rule.get("all", [])}
        phrases = [str(phrase).lower() for phrase in rule.get("phrases", [])]
        if (
            normalized.intersection(any_tags)
            or (all_tags and all_tags.issubset(normalized))
            or any(phrase in searchable for phrase in phrases)
        ):
            matches.append(name)
    return matches


def expanded_tags(
    raw_tags: list[str], taxonomy: dict[str, dict], text: str = ""
) -> list[str]:
    tags = [normalize_tag(tag) for tag in raw_tags if tag]
    return list(dict.fromkeys(tags + classify_tags(raw_tags, taxonomy, text)))
