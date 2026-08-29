# AI-physicist roadmap progress

## 2026-08-29 — Phase A baseline audit complete

- Baseline: `9aa8b6063798355970ee2c47991fe3ccbb36edd8` on `ai-physicist-roadmap`.
- Evidence: [AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md](AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md).
- Validation: dependency sync, 47 passing tests, 63% coverage, diagnostics, retrieval, live literature query, and explicit computation workbench execution.
- Known limitation: Ruff has 14 pre-existing findings; Semantic Scholar rate-limited the live query.
- Honey isolation: unavailable in this Codex environment; no architecture or critical-review subagent was used.

## Next milestone

Phase D: add provider-neutral model profiles and telemetry without changing retrieval behavior.

## 2026-08-29 — Phase B evaluation-suite foundation complete

- Added 20 source/tool-evidence cases across retrieval, literature (including paper-reproduction prerequisites), QFT, GR, and computation.
- Added `jarvis eval run`, which produces a machine-readable report without a model call and treats case failures as report data.
- Validation: focused evaluation/CLI tests, full suite (`50 passed`), new-code Ruff check, and a real local report (`20 passed`, `0 failed`).
- Scope: this is evidence/tool availability evaluation only; it does not validate scientific answers, derivations, or claims.

## 2026-08-29 — Phase C Manifest v2 scientific result types complete

- Added provider-neutral typed evidence, claim, verification, model-usage, task, decision, and flag records.
- New runs write Manifest v2 defaults; `load_manifest()` provides a non-mutating v2-shaped view of v1 manifests.
- `human_verified` claim status requires `human_reviewed=True`; this guards data consistency but is not human-actor authorization.
- Validation: manifest/workflow tests and full suite (`54 passed`).

## 2026-08-29 — Phase D profiles and telemetry complete

- Added optional configured model profiles, structured completion telemetry, and `jarvis ask --profile`.
- Preserved the existing default model and text-only completion API; no routing or retrieval behavior changed.
- Validation: focused configuration/runtime/CLI tests and full suite (`61 passed`).
