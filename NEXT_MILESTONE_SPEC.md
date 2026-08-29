# Milestone spec — Phase F execution: PhysicsIntern/Jarvis experiments

## Objective

Run five bounded known-answer investigations in a dedicated PhysicsIntern
workspace while preserving JARVIS evidence, computation, provisional-artifact,
and role-telemetry provenance.

## Preconditions and blocker

This milestone is blocked in the current CLI runtime. Before execution:

- The official upstream bootstrap script must create a dedicated empty workspace.
- `codex --disable plugins` must report `plugins=false` and runtime evidence
  must show no Honey directives.
- The Codex model catalog must load with `base_instructions` for the selected
  model and permit repeated fresh-context dispatches.

`BLOCKER.md` records the current evidence and no scientific agent may be spawned
until all three conditions hold.

## Current-state evidence

- Commit `89cdccd` provides Manifest v2 `provisional_artifacts`, contained
  file-level import, role-tagged `ModelUsage`, and portable ZIP handoffs.
- `prepare_literature`, retrieval/graph tools, and `prepare_computation` remain
  the existing evidence and deterministic-computation substrates.
- PhysicsIntern upstream commit `41d75f9` bootstrapped a disposable Codex
  workspace and an isolated free-scalar survey completed; no full investigation
  or accepted scientific result exists.

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

1. Repair or upgrade the external Codex runtime without altering Jarvis, then
   verify the corrected model catalog and provider reachability.
2. Re-run the plugin-disabled isolation audit and retain its runtime evidence.
3. Resume the official upstream-script workspace or bootstrap a fresh disposable
   one if needed.
4. Define five known-answer cases and their seeded-error checks before execution.
5. Run the cases with JARVIS retrieval/computation substrates and import their
   selected provisional artifacts plus telemetry.
6. Verify reproducibility, update progress/blocker, and commit the validated
   Phase F execution milestone.
