# Milestone spec — Phase F preparation: provisional imports and role telemetry

## Objective

Prepare the existing Manifest v2 run substrate for a later, Honey-isolated
PhysicsIntern experiment. Import one explicitly selected external artifact into
an existing run as immutable, provisional evidence and record model usage with
an optional execution role.

## Non-goals

- Do not create or run a PhysicsIntern workspace.
- Do not execute scientific agents, classify scientific tasks, create scientific
  claims, or run known-answer investigations.
- Do not add a PhysicsIntern-specific output schema, provider dependency, or
  second run-bundle format.
- Do not alter retrieval, graph, computation execution, router selection, or
  existing `jarvis ask` behavior.

## Current-state evidence

- `src/jarvis/workflows.py::_new_run` writes Manifest v2 run bundles;
  `load_manifest` normalizes v1/v2 reads without mutation.
- `prepare_literature`, `prepare_computation`, and `handoff` already provide
  evidence, explicit computation, and portable export substrates.
- `src/jarvis/models.py::ModelUsage` already carries provider/model/token/cost
  telemetry but lacks a role and is not persisted into a run.
- No external-artifact import API exists.

## Interfaces and data

- Add optional `role` to `ModelUsage`; its enclosing run supplies association.
- Add `ProvisionalArtifact` with an id, source label, role, run-relative path,
  SHA-256 digest, and import timestamp.
- `import_provisional_artifact(config, run_id, source, source_label, artifact_id,
  role=None)` accepts one regular source file, copies it under the target run,
  refuses source symlinks, duplicate ids, and paths outside the run, and appends
  its record to `manifest.json`.
- `record_model_usage(config, run_id, usage)` appends a validated `ModelUsage`
  record to the run manifest.
- `load_manifest` supplies an empty `provisional_artifacts` list for legacy
  manifests without rewriting them. New imported records remain provisional;
  importing cannot set a claim or verification status.
- Zip handoffs include imported artifacts; Markdown handoffs list their
  provenance metadata without treating their contents as instructions.

## Compatibility and provenance invariants

- Existing v1 reads remain non-mutating; all current v2 fields and workflows
  remain compatible.
- Imported files are copied, never linked; their original absolute path is not
  stored. The manifest records a stable content digest and run-relative path.
- Imported material is untrusted/provisional evidence, not a verified result.
- No API may set `human_verified`, modify an existing artifact, or overwrite an
  existing imported artifact id.
- Preserve existing sanitization and never emit credentials in handoffs.

## Required tests

- Valid import copies content, records a digest and provisional metadata, and is
  present in a ZIP handoff.
- Symlink and duplicate-id imports fail without modifying the target run.
- Role-tagged usage is serialized in the target run.
- Legacy manifest normalization includes the new empty field without rewriting
  the original file.
- Existing workflow, manifest, CLI, routing, and full test suites remain green.

## Acceptance criteria

- A future external research workspace can hand one selected artifact and its
  role telemetry to a JARVIS v2 run reproducibly.
- The imported artifact has a stable digest, run-local copy, explicit
  provisional status, and portable ZIP inclusion.
- No PhysicsIntern or scientific-agent action was taken in this milestone.

## Model/routing and review limitation

Honey is active in the current session. Its installed cache exposes skills only,
not a supported writable state or hook implementation, and the live skill
catalog does not expose PhysicsIntern. Therefore no architecture, critical
review, PhysicsIntern, or scientific subagent was used. The main coordinator
selected this bounded, reversible preparation interface; the next scientific
step remains blocked pending a Honey-isolated session with PhysicsIntern
available.

## Ordered implementation

1. Extend the manifest models and normalizer.
2. Add contained-copy import and usage-record helpers to `workflows.py`.
3. Include import artifacts in ZIP handoffs and provenance metadata in Markdown.
4. Add focused manifest/workflow tests, then run narrow and full verification.
5. Update the progress and blocker checkpoint; commit only milestone files.
