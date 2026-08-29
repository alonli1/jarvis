# Milestone spec — Phase A current-HEAD baseline audit

## Objective

Record a reproducible baseline for `9aa8b6063798355970ee2c47991fe3ccbb36edd8` before adding AI-physicist evaluation, routing, or research-state behavior.

## Non-goals

- No changes to retrieval, Dropbox, graph, MCP, skills, run bundles, computation, model routing, or document-access semantics.
- No document-level privacy tiers.
- No repair of pre-existing lint findings in this documentation-only milestone.

## Current-state evidence

- `src/jarvis/workflows.py` has v1 manifests and deterministic computation runs.
- `src/jarvis/llm.py` has only the existing `complete()` wrapper; no telemetry or profiles.
- `src/jarvis/cli.py` has no `eval` or `route` command.
- `docs/AUDIT.md` is a historical 2026-08-25 audit of `10879cc`, not the current baseline.

## Interfaces and compatibility

Add only dated audit/progress documentation. Production interfaces and stored run data remain unchanged.

## Scientific and provenance invariants

- Record commands, environment, outcomes, and known failures.
- Do not treat a successful process check as a scientific result.
- Preserve v1 run-bundle behavior and existing source/evidence semantics.

## Required validation

1. `uv sync --extra dev`
2. `uv run pytest -q`
3. `uv run pytest --cov=jarvis --cov-report=term-missing -q`
4. `uv run ruff check .`
5. `uv run jarvis doctor`
6. Local retrieval smoke test.
7. Live literature-query smoke test, recording partial-provider failure if any.
8. Explicit computation workbench preparation and execution.

## Acceptance criteria

- A dated baseline audit records exact HEAD, commands, results, failures, and known limitations.
- A durable progress file identifies Phase B as next work.
- No production behavior changes.

## Model and routing implications

Honey could not be mechanically isolated: the installed cache has no hook/state implementation and the environment exposes neither `CLAUDE_PLUGIN_ROOT` nor a supported writable state. No architecture or critical-review subagent was used; a Luna explorer supplied bounded repository evidence. This limitation has no effect on the Phase A audit.

## Ordered implementation steps

1. Run and record the baseline checks.
2. Update autonomous Honey instructions that required user action.
3. Add audit and progress checkpoints.
4. Inspect the diff and commit only milestone-owned files.
