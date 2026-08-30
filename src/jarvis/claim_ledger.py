from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import ScientificClaim, VerificationRecord
from .workflows import _run_path, _write_json, load_manifest


@dataclass(frozen=True)
class PromotionAssessment:
    eligible: bool
    policy: str
    reasons: tuple[str, ...]


def verification_policy(claim: ScientificClaim) -> tuple[str, bool]:
    if claim.kind == "source_result":
        return "source_comparison", False
    if claim.kind in {"derived_result", "computed_result"}:
        return "independent_check", True
    return "independent_check", True


def promotion_assessment(
    claim: ScientificClaim, records: list[VerificationRecord], run: Path
) -> PromotionAssessment:
    policy, requires_independence = verification_policy(claim)
    reasons = []
    if claim.status == "contradicted":
        reasons.append("claim is contradicted")
    matching = [record for record in records if record.claim_id == claim.id]
    passing = [record for record in matching if record.outcome == "passed"]
    if not matching:
        reasons.append("no claim-scoped verification record")
    elif not passing:
        reasons.append("no passed verification record")
    if requires_independence and passing and not any(record.independent for record in passing):
        reasons.append("no independent passed verification record")
    for record in passing:
        artifact = (run / record.artifact).resolve()
        try:
            artifact.relative_to(run)
        except ValueError:
            reasons.append(f"verification artifact escapes run: {record.id}")
            continue
        if not artifact.is_file():
            reasons.append(f"verification artifact is missing: {record.id}")
    return PromotionAssessment(not reasons, policy, tuple(reasons))


def promote_claim(root: Path, run_id: str, claim: ScientificClaim) -> PromotionAssessment:
    run = _run_path(type("Config", (), {"root": root})(), run_id)
    manifest_path = run / "manifest.json"
    manifest = load_manifest(manifest_path)
    if manifest["version"] != 2:
        raise ValueError("Claim promotion requires a Manifest v2 run")
    records = [VerificationRecord.model_validate(record) for record in manifest["verification"]]
    assessment = promotion_assessment(claim, records, run)
    if not assessment.eligible:
        return assessment
    promoted = claim.model_copy(update={"status": "ai_verified"})
    existing = [item for item in manifest["claims"] if item.get("id") != claim.id]
    existing.append(promoted.model_dump(mode="json"))
    manifest["claims"] = existing
    manifest["decision_log"].append(
        {
            "id": f"PROMOTE-{claim.id}",
            "decision": "ai_verified",
            "rationale": f"policy={assessment.policy}; passed claim-scoped verification",
            "artifacts": [record.artifact for record in records if record.claim_id == claim.id],
        }
    )
    _write_json(manifest_path, manifest)
    return assessment
