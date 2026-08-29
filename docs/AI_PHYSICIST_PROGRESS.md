# AI-physicist roadmap progress

## 2026-08-29 — Phase A baseline audit complete

- Baseline: `9aa8b6063798355970ee2c47991fe3ccbb36edd8` on `ai-physicist-roadmap`.
- Evidence: [AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md](AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md).
- Validation: dependency sync, 47 passing tests, 63% coverage, diagnostics, retrieval, live literature query, and explicit computation workbench execution.
- Known limitation: Ruff has 14 pre-existing findings; Semantic Scholar rate-limited the live query.
- Honey isolation: unavailable in this Codex environment; no architecture or critical-review subagent was used.

## Next milestone

Phase F execution: resume the five bounded PhysicsIntern/Jarvis known-answer
experiments after Codex's model-catalog runtime defect is repaired.

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

## 2026-08-29 — Phase E science-aware router v1 complete

- Added deterministic `jarvis route --dry-run` with explicit role priors, eleven bounded risk features, configurable capability tiers, reasons, and safe unavailable-profile failures.
- The router makes no provider request and cannot silently route below its computed epistemic floor.
- Validation: focused router tests, CLI smoke test, and full suite (`67 passed`).

## 2026-08-29 — Phase F preparation complete

- Added provider-neutral provisional-artifact import into Manifest v2 runs:
  contained copy, stable SHA-256 digest, source/role metadata, duplicate and
  traversal rejection, and ZIP/Markdown handoff support.
- Added optional role-tagged `ModelUsage` and run-persisted usage records.
- Validation: focused manifest/workflow tests (`9 passed`), full suite (`70
  passed`), and changed-file Ruff/format checks. Repository-wide Ruff still has
  15 pre-existing findings outside this milestone.
- Scope: no PhysicsIntern workspace, scientific agent, scientific claim, or
  known-answer investigation was run.

## 2026-08-29 — Phase F bootstrap and isolation verified; execution blocked

- Bootstrap: official upstream script with `host=codex`, PhysicsIntern commit
  `41d75f998710948e90b9254fba1cc501fe09fc84`, disposable workspace under
  `/tmp/jarvis-physicsintern-phase-f`.
- Isolation: `codex --disable plugins` sets `plugins=false`; an isolated runtime
  audit found no Honey and found all eight local PhysicsIntern skills plus seven
  local roles.
- Pilot: the free-scalar survey was produced and a separate symbolic oracle
  rejected a seeded wrong sign, but the autonomous workflow could not continue.
- Blocker: every isolated `codex exec` fails on a malformed model catalog
  (`base_instructions` absent for eight models); see `BLOCKER.md`. No five-case
  evaluation, imported run, scientific claim, or Phase F acceptance decision was
  made.

## Current blocker

Phase F remains in progress: F01 is complete and provisionally imported; F02--F05
remain to be run in independent disposable workspaces.

## 2026-08-29 — Phase F runtime recovery and F01 complete

- Recovery: reused Antigravity's installed OpenAI Codex extension runtime
  `0.151.0-alpha.7.1` at its recorded absolute path.  It passed a
  plugin-disabled model smoke test without the old `base_instructions` failure.
- Isolation: the recovered process reported `plugins=false`; its audit found no
  Honey directive/skill and found all eight PhysicsIntern skills and seven
  PhysicsIntern roles.  No global cache, authentication, or plugin setting was
  changed.
- F01 (free scalar, QFT): PhysicsIntern's completed, reviewed derivation and
  finite-difference calculation agree with an independent deterministic oracle;
  the seeded opposite mass sign is rejected.  The disposable workspace revision
  is `baa91ee`.
- Provenance: selected F01 artifacts were imported as provisional material into
  `20260829T154526Z-literature-phase-f-f01-evidence-context-for-a-f`.  Raw
  session logs were not imported.  The runtime did not report a per-role model
  identifier, so telemetry records `not-reported-by-runtime` rather than
  inventing a model name.
- Case contract: [PHASE_F_CASES.md](PHASE_F_CASES.md) defines F01--F05, their
  literature/deterministic bases, and withheld seeded checks.

## 2026-08-29 — Phase F F02 dispatch capability blocked

- A fresh F02 EFT workspace was successfully bootstrapped and populated with
  only its bounded question and evidence pointer.
- The recovered plugin-disabled `codex exec` process reaches the model, but its
  PhysicsIntern coordinator exposes no usable fresh-context `spawn_agent`:
  the trace shows a `wait` collaboration call with no receiver at the required
  survey dispatch point.  No F02 scientific artifact was accepted or imported.
- This is a distinct external runtime-host limitation, not the repaired model
  catalog issue.  The F02 workspace is preserved pending a plugin-disabled
  invocation mode with generated-role dispatch support; see `BLOCKER.md`.

## 2026-08-29 — Process-isolated dispatch capsule blocked

- A Phase-F-only adapter under `/tmp` created fresh, plugin-disabled recovered
  Codex sessions, role/prompt hashes, staged-input manifests, stdout/stderr
  provenance, and output-contract validation.  Two non-scientific role smoke
  artifacts passed those local checks.
- The planner smoke trace could still see the parent F02 workspace through
  `../../../`, so the capsule cannot protect hidden oracles and forbidden
  reviews.  `bubblewrap` is present but non-privileged user namespaces are
  disabled by the kernel, preventing the required filesystem boundary.
- F02--F05 remain unaccepted.  This is an external OS-isolation blocker, not a
  PhysicsIntern methodology result; see `BLOCKER.md`.
