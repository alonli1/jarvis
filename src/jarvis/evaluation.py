from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import Config
from .retrieval import retrieve_hits
from .workflows import tool_status

_CATEGORIES = {"retrieval", "literature", "qft", "gr", "computation"}
_MODES = {"retrieval", "tool_status"}


class EvaluationError(ValueError):
    pass


@dataclass(frozen=True)
class EvaluationCase:
    id: str
    category: str
    mode: str
    expected_evidence: tuple[str, ...]
    minimum_matches: int
    question: str | None = None


def _error(path: Path, message: str) -> EvaluationError:
    return EvaluationError(f"{path}: {message}")


def _string(value: object, path: Path, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _error(path, f"{field} must be a non-empty string")
    return value


def _relative_path(value: str, path: Path) -> str:
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise _error(path, "source_path must be repository-relative")
    return value


def load_cases(cases_path: Path) -> list[EvaluationCase]:
    """Load strict evidence/tool evaluation cases from category directories."""
    if not cases_path.is_dir():
        raise EvaluationError(f"{cases_path}: cases directory does not exist")

    cases: list[EvaluationCase] = []
    case_ids: set[str] = set()
    for path in sorted(cases_path.glob("*/*.yaml")):
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise EvaluationError(f"{path}: invalid YAML: {exc}") from exc
        if not isinstance(raw, dict):
            raise _error(path, "case must be a mapping")

        category = _string(raw.get("category"), path, "category")
        mode = _string(raw.get("mode"), path, "mode")
        allowed = {"id", "category", "mode", "expected_evidence", "criteria"}
        if mode == "retrieval":
            allowed.add("question")
        unknown = set(raw) - allowed
        if unknown:
            raise _error(path, f"unsupported field: {min(unknown)}")
        if category not in _CATEGORIES:
            raise _error(path, f"unsupported category: {category}")
        if path.parent.name != category:
            raise _error(path, f"category does not match directory: {category}")
        if mode not in _MODES:
            raise _error(path, f"unsupported mode: {mode}")

        case_id = _string(raw.get("id"), path, "id")
        if case_id in case_ids:
            raise _error(path, f"duplicate id: {case_id}")
        case_ids.add(case_id)

        evidence = raw.get("expected_evidence")
        if not isinstance(evidence, list) or not evidence:
            raise _error(path, "expected_evidence must be a non-empty list")
        evidence_field = "source_path" if mode == "retrieval" else "tool_id"
        expectations: list[str] = []
        for item in evidence:
            if not isinstance(item, dict) or set(item) != {evidence_field}:
                raise _error(path, f"expected_evidence entries must contain only {evidence_field}")
            value = _string(item[evidence_field], path, evidence_field)
            expectations.append(_relative_path(value, path) if mode == "retrieval" else value)
        if len(expectations) != len(set(expectations)):
            raise _error(path, "expected_evidence entries must be unique")

        criteria = raw.get("criteria")
        if not isinstance(criteria, dict) or set(criteria) != {"minimum_matches"}:
            raise _error(path, "criteria must contain only minimum_matches")
        minimum_matches = criteria["minimum_matches"]
        if (
            isinstance(minimum_matches, bool)
            or not isinstance(minimum_matches, int)
            or not 0 < minimum_matches <= len(expectations)
        ):
            raise _error(path, "minimum_matches must be a positive integer within expectations")

        question = None
        if mode == "retrieval":
            question = _string(raw.get("question"), path, "question")
        cases.append(
            EvaluationCase(
                id=case_id,
                category=category,
                mode=mode,
                question=question,
                expected_evidence=tuple(expectations),
                minimum_matches=minimum_matches,
            )
        )
    if not cases:
        raise EvaluationError(f"{cases_path}: no YAML cases found")
    return cases


def _result(case: EvaluationCase, found: set[str]) -> dict[str, object]:
    expected = list(case.expected_evidence)
    matched = sum(value in found for value in expected)
    result: dict[str, object] = {
        "id": case.id,
        "category": case.category,
        "mode": case.mode,
        "matched_count": matched,
        "score": matched / len(expected),
        "passed": matched >= case.minimum_matches,
    }
    field = "source_paths" if case.mode == "retrieval" else "tool_ids"
    result[f"expected_{field}"] = expected
    result[f"found_{field}"] = sorted(found)
    return result


def evaluate_cases(
    config: Config,
    cases: list[EvaluationCase],
    retriever: Callable[..., list] = retrieve_hits,
    status_provider: Callable[[Path], list[dict]] = tool_status,
) -> dict[str, object]:
    """Run deterministic source/tool checks without model calls."""
    statuses: set[str] | None = None
    results = []
    for case in cases:
        if case.mode == "retrieval":
            found = {hit.chunk.source_path for hit in retriever(config, case.question)}
        else:
            if statuses is None:
                statuses = {
                    item["id"] for item in status_provider(config.root) if item["status"] == "available"
                }
            found = statuses
        results.append(_result(case, found))
    passed = sum(result["passed"] for result in results)
    return {
        "schema_version": "1.0",
        "scope": "evidence/tool evaluation; not scientific-result verification",
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "cases": results,
    }
