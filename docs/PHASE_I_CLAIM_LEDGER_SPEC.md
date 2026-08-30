# Phase I milestone I1 — deterministic claim-promotion guard

## Objective

Make `ai_verified` a policy-gated scientific state. A claim may be promoted
only when claim-scoped, passed verification records point to contained run
artifacts and satisfy the claim kind's independent-check policy.

## Non-goals

- No model, reviewer, or external literature call.
- No automatic human verification or novelty determination.
- No research-memory index yet; that follows once ledger records are stable.

## Interfaces

- `VerificationRecord` gains optional `claim_id` and `independent` fields with
  backward-compatible defaults.
- `verification_policy(claim)` selects required evidence for source, derivation,
  computation, and other claim kinds.
- `promotion_assessment(claim, records, run)` reports policy outcome and missing
  requirements without mutation.
- `promote_claim()` writes a Manifest v2 claim only after assessment passes;
  it cannot alter `human_verified` state.

## Invariants

- `ai_verified` requires a passed, claim-scoped record, an existing contained
  artifact, and independence when policy requires it.
- Contradicted claims and failing verification records cannot be promoted.
- A policy decision records its rationale in the run decision log; normal
  manifests and legacy v1 views remain compatible.

## Acceptance

- Missing, failing, unrelated, non-independent, and escaping-artifact records
  are rejected for promotion.
- A bounded symbolic/computation-style claim can be promoted only with a valid
  independent record.
- Focused ledger/manifest tests and the full suite pass.

## Review limitation

Honey directives remain visible in this coordinator context, so this additive,
deterministic policy is reviewed in the parent context rather than by an
architecture or critical-review subagent.
