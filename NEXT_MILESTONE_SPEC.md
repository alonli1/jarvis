# Milestone spec — Phase F execution: PhysicsIntern/Jarvis experiments

## Objective

Run five bounded known-answer investigations in a dedicated PhysicsIntern
workspace while preserving JARVIS evidence, computation, provisional-artifact,
and role-telemetry provenance.

## Preconditions and blocker

The runtime prerequisite is satisfied by the recovered extension runtime.
Before each remaining execution:

- The official upstream bootstrap script must create a dedicated empty workspace.
- `codex --disable plugins` must report `plugins=false` and runtime evidence
  must show no Honey directives.
- The recovered Codex executable must remain usable with `--disable plugins`
  and expose usable fresh-context `spawn_agent`/`wait_agent` dispatches to the
  generated PhysicsIntern workspace roles.
- If native dispatch is unavailable, a process-isolated transport must enforce
  an OS-level capsule filesystem boundary; prompt-only or path-based staging is
  insufficient because it cannot protect private oracle material.

`BLOCKER.md` records the historical standalone defect and recovery evidence.

## Current-state evidence

- Commit `89cdccd` provides Manifest v2 `provisional_artifacts`, contained
  file-level import, role-tagged `ModelUsage`, and portable ZIP handoffs.
- `prepare_literature`, retrieval/graph tools, and `prepare_computation` remain
  the existing evidence and deterministic-computation substrates.
- PhysicsIntern upstream commit `41d75f9` bootstrapped a disposable Codex
  workspace; F01 has complete reviewed artifacts, an independent deterministic
  check, and provisional import.  See `docs/PHASE_F_CASES.md`.

## Interfaces and boundaries

- Use `import_provisional_artifact` only for selected regular output files,
  retaining source label, role, run-relative path, digest, and timestamp.
- Use `record_model_usage` for each role/model invocation in its associated
  Manifest v2 run.
- Keep imported material provisional. Only recorded checks can change claim or
  verification status; no AI action may mark a result human verified.
- Do not add a PhysicsIntern dependency or nested workspace inside this repo.

## Scientific/provenance invariants

- Survey outputs must cite JARVIS evidence with source path plus page/section.
- Computation must use explicit JARVIS workbench execution and retain scripts,
  raw logs, conventions, assumptions, and independent checks.
- Seeded mistakes must be declared before testing and independent checks must
  detect at least some of them.
- Preserve original artifacts by digest; do not import credentials or absolute
  source paths into run bundles or exports.

## Required validation and acceptance

- Five known-answer investigations have complete reproducible artifacts.
- At least one retrieval/graph output and one computation workbench are used
  where applicable.
- Each run records model/provider/role telemetry and provisional imported output.
- Independent checks catch seeded mistakes.
- Existing test suite and relevant new integration checks pass.

## Model/routing implication

The generic coding router is not scientific classification. PhysicsIntern may be
used only after Honey isolation; no architecture or critical-review agent is
permitted while Honey is active.

## Ordered execution

1. Reconfirm the recovered plugin-disabled runtime before each scientific run.
2. Bootstrap a fresh disposable workspace for each remaining case.
3. Run F02--F05 from `docs/PHASE_F_CASES.md` with JARVIS
   retrieval/computation substrates and import their
   selected provisional artifacts plus telemetry.
4. Verify reproducibility, produce the five-case evaluation, update
   progress/blocker, and commit the validated
   Phase F execution milestone.
