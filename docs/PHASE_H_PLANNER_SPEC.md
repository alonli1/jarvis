# Phase H milestone H1 — deterministic research plans and task packets

## Objective

Add provider-neutral, deterministic plan and task-packet records to Manifest v2
runs. The milestone validates a bounded dependency graph, fixed task budget,
and explicit stop conditions; it does not call or schedule a model.

## Current-state evidence

- `ScientificClaim`, `VerificationRecord`, and a minimal `ResearchTask` already
  exist in `src/jarvis/models.py`.
- `workflows._new_run()` stores `plan: null` and `tasks: []` in Manifest v2,
  while `load_manifest()` preserves old manifests through non-mutating defaults.
- `routing.py` has deterministic role floors, including `research_planning`,
  but no planner execution interface.
- Phase F validated role-separated research artifacts; Phase H must preserve
  their provenance discipline without copying PhysicsIntern prompts.

## Interfaces

- `ResearchTask` gains optional machine-readable kind, objective, verification
  method, budget, and stop condition fields while retaining its existing
  serializable fields.
- `ResearchPlan` contains a question, success criteria, conventions,
  bounded tasks, stop conditions, and a maximum leaf-task budget. Validation
  rejects duplicate IDs, unknown dependencies, cycles, self-dependencies, and
  plans exceeding their declared budget.
- `TaskPacket` is a run-relative leaf-execution input with dependency artifact
  references, selected route metadata, and an immutable plan digest.
- `persist_plan()` persists a plan and task records into a Manifest v2 run.
  `create_task_packets()` writes ready task JSON only after deterministic graph
  validation; dependent packets require completed dependencies and existing,
  run-contained artifacts. It never performs a model call.

## Constraints and invariants

- No packet may expose absolute paths, credentials, hidden oracle material, or
  reviewer verdicts.
- Packets refer only to known run-relative artifacts; a task can execute only
  after dependencies are complete and their declared artifacts exist.
- Plan/task persistence requires Manifest v2 and cannot promote claims or mark
  a result human verified.
- Existing literature, ideation, computation, routing, and v1 manifest views
  remain compatible.

## Acceptance

- Representative QFT/GR-shaped plans serialize reproducibly with deterministic
  task ordering and no runaway fan-out.
- Invalid graphs and over-budget plans fail before mutation.
- Packets are contained, omit execution/model calls, and record only validated
  upstream artifacts.
- Focused planner/manifest tests and the full suite pass.

## Review limitation

Honey directives are visible in the coordinator context, so no architecture or
critical-review subagent is used. This H1 interface is intentionally confined
to deterministic data validation; parent-level review checks compatibility,
containment, and provenance before implementation.
