# Milestone spec — Phase F execution: PhysicsIntern/Jarvis experiments

## Objective

Run five bounded known-answer investigations in a dedicated PhysicsIntern
workspace while preserving JARVIS evidence, computation, provisional-artifact,
and role-telemetry provenance.

## Preconditions and blocker

This milestone is blocked in the current session. Before execution:

- `init-physics-intern` must appear in the live skill catalog.
- Honey isolation must be mechanically verified from installed/runtime evidence.
- The user must explicitly invoke `$init-physics-intern` for a dedicated empty
  workspace; the official bootstrap skill prohibits implicit invocation.

`BLOCKER.md` records the current evidence and no scientific agent may be spawned
until all three conditions hold.

## Current-state evidence

- Commit `89cdccd` provides Manifest v2 `provisional_artifacts`, contained
  file-level import, role-tagged `ModelUsage`, and portable ZIP handoffs.
- `prepare_literature`, retrieval/graph tools, and `prepare_computation` remain
  the existing evidence and deterministic-computation substrates.
- No PhysicsIntern workspace, agent output, scientific result, or known-answer
  experiment has been created in this repository.

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

1. Verify the preconditions and isolate Honey reversibly.
2. Bootstrap the dedicated empty workspace only through the explicit official
   skill invocation.
3. Define five known-answer cases and their seeded-error checks before execution.
4. Run the cases with JARVIS retrieval/computation substrates and import their
   selected provisional artifacts plus telemetry.
5. Verify reproducibility, update progress/blocker, and commit the validated
   Phase F execution milestone.
