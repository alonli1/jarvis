import json
from dataclasses import replace

import pytest
from pydantic import ValidationError

from jarvis.config import load_config
from jarvis.models import (
    DecisionRecord,
    EvidenceReference,
    ModelUsage,
    ProvisionalArtifact,
    ResearchTask,
    ScientificClaim,
    ScientificFlag,
    VerificationRecord,
)
from jarvis.workflows import load_manifest, prepare_computation, prepare_literature


def config_for(tmp_path):
    source = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages/registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    ecosystem: python\n    executable: python\n"
        "    package: sympy\n    purpose: checks\n    related_topics: []\n"
    )
    return replace(source, root=tmp_path)


def test_scientific_records_are_provider_neutral_and_serializable():
    evidence = EvidenceReference(kind="paper", reference="doi:10.1/example", locator="p. 2")
    claim = ScientificClaim(
        id="CLAIM-1",
        statement="A source-supported statement.",
        kind="source_result",
        status="source_grounded",
        scope={"theory": "example"},
        conventions={"units": "natural"},
        evidence=[evidence],
        created_by="ai",
    )
    records = [
        claim,
        VerificationRecord(
            id="VERIFY-1", method="symbolic", outcome="passed", artifact="checks.md"
        ),
        ModelUsage(
            provider="local", model="example", role="research", input_tokens=1, output_tokens=2
        ),
        ProvisionalArtifact(
            id="ART-1",
            source_label="test",
            role="research",
            path="provisional/ART-1/result.txt",
            sha256="0" * 64,
            imported_at="2026-08-29T00:00:00+00:00",
        ),
        ResearchTask(
            id="TASK-1", description="Check result", status="pending", artifacts=["checks.md"]
        ),
        DecisionRecord(id="DEC-1", decision="Check independently", rationale="Required"),
        ScientificFlag(code="GAP", severity="warning", message="Needs review"),
    ]

    assert all(json.loads(record.model_dump_json()) for record in records)


def test_human_verified_claim_requires_human_reviewed():
    with pytest.raises(ValidationError, match="human_reviewed=True"):
        ScientificClaim(
            id="CLAIM-1",
            statement="A statement.",
            kind="derived_result",
            status="human_verified",
            created_by="ai",
        )


def test_load_manifest_normalizes_v1_without_rewriting(tmp_path):
    path = tmp_path / "manifest.json"
    raw = {
        "version": 1,
        "id": "run-1",
        "workflow": "literature",
        "query": "question",
        "created_at": "2026-08-29T00:00:00+00:00",
        "corpus_revision": "sha256:example",
        "status": "prepared",
        "inputs": [],
        "citations": [],
        "tools": [],
        "artifacts": [],
    }
    path.write_text(json.dumps(raw), encoding="utf-8")
    before = path.read_bytes()

    manifest = load_manifest(path)

    assert manifest["version"] == 1
    assert manifest["plan"] is None
    assert all(
        manifest[key] == []
        for key in (
            "tasks",
            "claims",
            "model_usage",
            "verification",
            "flags",
            "decision_log",
            "provisional_artifacts",
        )
    )
    assert path.read_bytes() == before


def test_new_runs_write_v2_manifest_defaults(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.workflows.retrieve_hits", lambda *args, **kwargs: [])
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")

    literature = json.loads(
        (prepare_literature(cfg, "Question").path / "manifest.json").read_text()
    )
    computation = json.loads(
        (prepare_computation(cfg, "Check identity", "python").path / "manifest.json").read_text()
    )

    for manifest, workflow in ((literature, "literature"), (computation, "computation")):
        assert manifest["version"] == 2
        assert manifest["workflow"] == workflow
        assert manifest["plan"] is None
        assert all(
            manifest[key] == []
            for key in (
                "tasks",
                "claims",
                "model_usage",
                "verification",
                "flags",
                "decision_log",
                "provisional_artifacts",
            )
        )
    assert computation["engine"] == "python"
