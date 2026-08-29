import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from jarvis import cli
from jarvis.evaluation import EvaluationError, evaluate_cases, load_cases


def write_case(root: Path, category: str, name: str, text: str) -> None:
    path = root / category / f"{name}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_load_cases_is_strict_and_rejects_duplicate_ids(tmp_path):
    cases_path = tmp_path / "cases"
    case = """id: case-one
category: retrieval
mode: retrieval
question: Find evidence.
expected_evidence:
  - source_path: knowledge/source.pdf
criteria:
  minimum_matches: 1
"""
    write_case(cases_path, "retrieval", "one", case)
    loaded = load_cases(cases_path)
    assert loaded[0].id == "case-one"

    write_case(cases_path, "retrieval", "two", case)
    with pytest.raises(EvaluationError, match="duplicate id"):
        load_cases(cases_path)

    (cases_path / "retrieval" / "two.yaml").unlink()
    write_case(cases_path, "retrieval", "invalid", "id: invalid\n")
    with pytest.raises(EvaluationError, match="category"):
        load_cases(cases_path)


def test_evaluate_cases_scores_retrieval_and_tool_status(tmp_path):
    cases_path = tmp_path / "cases"
    write_case(
        cases_path,
        "retrieval",
        "partial",
        """id: partial
category: retrieval
mode: retrieval
question: Find evidence.
expected_evidence:
  - source_path: knowledge/found.pdf
  - source_path: knowledge/missed.pdf
criteria:
  minimum_matches: 2
""",
    )
    write_case(
        cases_path,
        "computation",
        "tool",
        """id: tool
category: computation
mode: tool_status
expected_evidence:
  - tool_id: python
  - tool_id: absent
criteria:
  minimum_matches: 1
""",
    )
    report = evaluate_cases(
        SimpleNamespace(root=tmp_path),
        load_cases(cases_path),
        retriever=lambda *_: [SimpleNamespace(chunk=SimpleNamespace(source_path="knowledge/found.pdf"))],
        status_provider=lambda _: [
            {"id": "python", "status": "available"},
            {"id": "absent", "status": "missing"},
        ],
    )
    assert report["passed"] == 1
    assert report["failed"] == 1
    results = {result["id"]: result for result in report["cases"]}
    assert results["partial"]["matched_count"] == 1
    assert results["partial"]["score"] == 0.5
    assert results["tool"]["found_tool_ids"] == ["python"]


def test_eval_run_emits_json_and_writes_output(tmp_path, monkeypatch):
    report = {"schema_version": "1.0", "total": 1, "passed": 0, "failed": 1, "cases": []}
    monkeypatch.setattr(cli, "load_config", lambda: SimpleNamespace(root=tmp_path))
    monkeypatch.setattr(cli, "load_cases", lambda _: [])
    monkeypatch.setattr(cli, "evaluate_cases", lambda *_: report)
    output = tmp_path / "report.json"

    result = CliRunner().invoke(cli.app, ["eval", "run"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == report

    result = CliRunner().invoke(
        cli.app, ["eval", "run", "--output", str(output)]
    )
    assert result.exit_code == 0
    assert json.loads(output.read_text(encoding="utf-8")) == report
