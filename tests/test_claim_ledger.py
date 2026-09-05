import json
from dataclasses import replace

import pytest

from jarvis.claim_ledger import (
    contradict_claim,
    mark_human_verified,
    promote_claim,
    promotion_assessment,
    record_verification,
)
from jarvis.config import load_config
from jarvis.models import ScientificClaim, VerificationRecord
from jarvis.workflows import prepare_computation


def config_for(tmp_path):
    source = load_config()
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "registry.yaml").write_text(
        "version: 1\ntools:\n  - id: python\n    executable: python\n    ecosystem: python\n"
        "    package: sympy\n    capabilities: [symbolic_algebra, numerical_calculation]\n",
        encoding="utf-8",
    )
    return replace(source, root=tmp_path)


def claim(status="computed_once"):
    return ScientificClaim(
        id="CLAIM-1",
        statement="A bounded result.",
        kind="computed_result",
        status=status,
        created_by="ai",
    )


def test_promotion_requires_claim_scoped_independent_contained_evidence(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(cfg, "Ledger test", "python")
    artifact = bundle.path / "outputs" / "check.txt"
    artifact.write_text("passed", encoding="utf-8")
    good = VerificationRecord(
        id="VERIFY-1",
        claim_id="CLAIM-1",
        method="symbolic",
        outcome="passed",
        artifact="outputs/check.txt",
        independent=True,
    )

    assert promotion_assessment(claim(), [good], bundle.path).eligible
    manifest_path = bundle.path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["verification"] = [good.model_dump(mode="json")]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assessment = promote_claim(cfg.root, bundle.id, claim())
    promoted = json.loads(manifest_path.read_text())

    assert assessment.eligible
    assert promoted["claims"][0]["status"] == "ai_verified"
    assert promoted["decision_log"][0]["decision"] == "ai_verified"


def test_promotion_rejects_missing_failing_unrelated_or_escaping_evidence(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    records = [
        VerificationRecord(
            id="wrong", claim_id="OTHER", method="symbolic", outcome="passed", artifact="x"
        ),
        VerificationRecord(
            id="failed", claim_id="CLAIM-1", method="symbolic", outcome="failed", artifact="x"
        ),
        VerificationRecord(
            id="escape",
            claim_id="CLAIM-1",
            method="symbolic",
            outcome="passed",
            artifact="../x",
            independent=True,
        ),
    ]

    assessment = promotion_assessment(claim(), records, run)

    assert not assessment.eligible
    assert "verification artifact escapes run: escape" in assessment.reasons
    assert not promotion_assessment(claim("contradicted"), [], run).eligible


def test_contradiction_and_human_verification_are_explicit_actions(tmp_path, monkeypatch):
    cfg = config_for(tmp_path)
    monkeypatch.setattr("jarvis.tool_registry.importlib.metadata.version", lambda _: "1.0")
    bundle = prepare_computation(cfg, "Ledger state test", "python")
    artifact = bundle.path / "outputs" / "counterexample.txt"
    artifact.write_text("counterexample", encoding="utf-8")
    contradiction = VerificationRecord(
        id="VERIFY-CONTRA",
        claim_id="CLAIM-1",
        method="counterexample",
        outcome="contradicted",
        artifact="outputs/counterexample.txt",
        independent=True,
    )

    contradict_claim(cfg.root, bundle.id, claim(), contradiction)
    manifest = json.loads((bundle.path / "manifest.json").read_text())

    assert manifest["claims"][0]["status"] == "contradicted"
    assert manifest["verification"][0]["outcome"] == "contradicted"
    mark_human_verified(cfg.root, bundle.id, claim(), "Researcher A")
    manifest = json.loads((bundle.path / "manifest.json").read_text())
    assert manifest["claims"][0]["status"] == "human_verified"
    assert manifest["claims"][0]["human_reviewed"] is True
    with pytest.raises(ValueError, match="reviewer identity"):
        mark_human_verified(cfg.root, bundle.id, claim(), " ")
    with pytest.raises(ValueError, match="already exists"):
        record_verification(cfg.root, bundle.id, contradiction)
