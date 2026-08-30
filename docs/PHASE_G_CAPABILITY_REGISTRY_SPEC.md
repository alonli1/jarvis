# Phase G milestone G1 — scientific capability registry

## Objective

Evolve `packages/registry.yaml` from installation diagnostics into a
capability-based, deterministic registry that downstream computation and
orchestration code can query without hard-coding package names.

## Non-goals

- Do not install, configure, or repair Wolfram or third-party packages.
- Do not execute scientific claims, create a planner, or alter Manifest v2.
- Do not add document-level privacy fields, provider dependencies, or a new
  foundational skill.

## Current-state evidence

- `packages/registry.yaml` version 1 records six tools, package markers, and
  topics, but no capability or verification metadata.
- `jarvis.workflows.tool_status()` performs the only registry interpretation;
  `prepare_computation()` persists its diagnostics in a computation manifest.
- `uv run jarvis doctor` on 2026-08-30 found Python/SymPy available and the
  installed Wolfram, xAct, FeynCalc, Matchete, and FIRE7 surface blocked by a
  failed Wolfram runtime smoke test.
- The Phase G roadmap requires capability-based selection and tool-specific
  scientific check templates before native planning begins.

## Interface and compatibility

- Registry version 2 retains every version 1 field and adds `capabilities`,
  `domains`, `execution`, and `verification` metadata.
- `load_tool_registry(root)` returns validated, normalized entries. Version 1
  registries remain readable for existing clones.
- `tool_status(root)` retains its current diagnostic fields and augments them
  with normalized capability metadata.
- `select_tools(root, capabilities)` returns only available matching tools,
  ordered by registry order, and records the capabilities matched by each
  result. A missing capability is represented by an empty result, not a
  fallback to an unrelated package.

## Scientific and provenance invariants

- Availability is a runtime diagnostic, not scientific verification.
- Declared check templates identify required checks but cannot promote claims
  or replace recorded independent evidence.
- Existing explicit computation execution, logs, scripts, and Manifest v2
  semantics remain unchanged.

## Tests and acceptance

- Validate v1 compatibility, v2 metadata validation, and duplicate rejection.
- Validate that selection is deterministic, capability-specific, and excludes
  missing or runtime-blocked tools.
- Preserve existing computation workflow and evaluation tests.
- Record the Wolfram runtime limitation as an execution-gate outcome, not as
  package absence.

## Routing and review limitation

This is a consequential but additive registry interface. The current
coordinator session has Honey plugin instructions available, so no
`jarvis_architect` or critical-review subagent is spawned. The coordinator used
a structured compatibility and provenance review; Phase G execution workflows
will receive independent review only from a verified plugin-disabled context.

## Ordered implementation

1. Add a small registry module with versioned normalization and validation.
2. Move diagnostics to that registry module without changing their observable
   statuses.
3. Enrich the committed registry with the existing packages' capabilities and
   declared check templates.
4. Add focused tests, run the relevant suite, document the checkpoint, and
   commit the validated milestone.
