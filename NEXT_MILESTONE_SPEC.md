# Milestone spec — Phase C Manifest v2 scientific result types

## Objective

Add provider-neutral typed scientific-result records and let newly created run bundles write Manifest v2, while a public reader normalizes v1 and v2 manifests without rewriting existing v1 files.

## Non-goals

- No model profiles, telemetry collection, router, orchestration, task execution, claim promotion workflow, or UI.
- No migration of existing on-disk v1 bundles.
- No model or AI action may mark a result `human_verified`.
- No document-level privacy tiers.

## Current-state evidence

- `src/jarvis/models.py` contains corpus and novelty models only.
- `src/jarvis/workflows.py:_new_run` writes a dictionary with `version: 1`.
- `prepare_literature`, `prepare_ideation`, and `prepare_computation` add workflow-specific fields to that dictionary.
- `execute_computation` and `handoff` read raw `manifest.json` mappings directly.

## Interfaces and data model

Add Pydantic records in `jarvis.models`:

- `EvidenceReference`: `kind`, `reference`, optional `locator`.
- `ScientificClaim`: stable ID, statement, kind, explicit claim status, scope/conventions mappings, evidence references, known issues, `created_by`, and `human_reviewed`.
- `VerificationRecord`: ID, method, outcome, artifact reference, optional notes.
- `ModelUsage`: provider, model, optional input/output tokens, latency milliseconds, and estimated cost.
- `ResearchTask`: ID, description, status, dependencies, and artifact references.
- `DecisionRecord`: ID, decision, rationale, artifact references.
- `ScientificFlag`: code, severity, message, optional artifact reference.

Use a closed claim-status set: `candidate`, `source_grounded`, `derived_once`, `computed_once`, `independently_checked`, `contradicted`, `ai_verified`, `human_verified`, `published_or_external`, `retired`. Reject a `human_verified` claim unless `human_reviewed` is true. This is a data-integrity guard, not proof of human action.

Add `load_manifest(path)` in `jarvis.workflows`. It accepts v1/v2 JSON mappings, rejects unsupported versions or malformed required v1 identity fields, and returns a normalized mapping with all v2 collection keys present. It preserves the source `version` and never writes or migrates a v1 file.

New `_new_run` manifests write `version: 2` plus empty `plan`, `tasks`, `claims`, `model_usage`, `verification`, `flags`, and `decision_log` fields. Existing fields and all workflow-specific additions remain unchanged.

## Backward compatibility

- Existing v1 manifests continue to work with `execute_computation` and `handoff` unmodified.
- `load_manifest()` gives callers a stable v2-shaped view of v1 data, without changing its on-disk version.
- Existing CLI commands and run IDs remain unchanged.

## Scientific/provenance invariants

- Claims distinguish status from evidence and verification records.
- Artifact/source references remain run-local or source-citable strings; no evidence is discarded.
- V1 bundles are not silently migrated.
- `human_verified` always requires an explicit `human_reviewed` data assertion; future actor authorization remains an orchestration concern.

## Required tests

1. Record validation accepts valid evidence/claim/verification/task/usage/decision/flag models.
2. `human_verified` without `human_reviewed` is rejected.
3. A v1 fixture loads with v2 default collections and retains `version: 1` on disk.
4. New literature and computation runs write v2 defaults and keep current workflow fields.
5. Existing workflow/handoff tests remain green.

## Acceptance criteria

- V1 is readable, unchanged on disk, and exposes v2 default collections through the reader.
- New runs contain only the specified v2 delta and preserve all previous fields.
- Typed records are provider-neutral and serializable.
- No new code can construct a `human_verified` claim without `human_reviewed=True`.

## Model/routing implications and review limitation

Honey isolation remains unavailable because the installed cache lacks hook/state source and no supported writable state is exposed. No Sol architecture/reviewer agent may be used. The main coordinator performed two checks: this scope limits changes to data contracts and defaults; raw v1 consumers remain untouched. A parent-level adversarial review must verify v1 non-migration, status guarding, and provenance retention before commit.

## Ordered implementation steps

1. Add the typed records and status guard with focused model tests.
2. Add a non-mutating manifest reader and v2 defaults for new runs.
3. Test v1 preservation plus v2 generation through existing workflows.
4. Run focused and broader tests, inspect the diff, update progress, and checkpoint.
