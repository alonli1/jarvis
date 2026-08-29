# Milestone spec — Phase B evaluation-suite foundation

## Objective

Add a small deterministic `jarvis eval run` harness and 20 source/tool-evidence cases across retrieval, literature, QFT, GR, computation, and paper reproduction. Produce a machine-readable report before adding profiles, routing, orchestration, or v2 run state.

## Non-goals

- No model call, answer grading, model routing, telemetry, orchestration, or Manifest v2.
- No scientific derivation or claim verification. The initial suite scores only deterministic evidence retrieval and registered-tool availability.
- No migration of existing retrieval, Dropbox, graph, MCP, skills, run-bundle, or computation interfaces.
- No document-level privacy tiers.

## Current-state evidence

- `src/jarvis/retrieval.py:12` exposes `retrieve_hits()` and `retrieval_result()` with cited source paths/pages.
- `src/jarvis/workflows.py:316` exposes registered-tool detection through `tool_status()`.
- `src/jarvis/cli.py` has no eval command or group.
- There is no `src/jarvis/evaluation.py`, `tests/test_evaluation.py`, or `evals/` directory.
- `knowledge/references.yaml` and the local corpus include canonical EFT, GR, QFT-in-curved-space, and computational-tool material suitable for source-evidence expectations.

## Interfaces and data model

Add `evals/cases/<category>/*.yaml`, with exactly one mapping per file:

```yaml
id: stable-case-id
category: retrieval|literature|qft|gr|computation
mode: retrieval|tool_status
question: non-empty question for retrieval mode
expected_evidence:
  - source_path: repo-relative source path
criteria:
  minimum_matches: positive integer
```

For `tool_status`, `expected_evidence` contains `tool_id` entries and no question is required. The loader rejects malformed files, duplicate IDs, category/path mismatches, unsupported modes, and criteria that exceed supplied expectations.

Add public evaluation functions in `jarvis.evaluation` to load cases and return a JSON-serializable report. Each retrieval result records expected/found source paths, matched count, score (`matched / expected`), and pass/fail from `minimum_matches`. Tool-status results use registered tool IDs with the same transparent scoring. The report records schema version, total/passed/failed counts, and case results.

Add a Typer subgroup: `jarvis eval run [--cases PATH] [--output PATH]`. It writes stable JSON to stdout or the requested output path and exits non-zero only for malformed inputs or an unexpected evaluator error, not for evaluated case failures.

## Backward compatibility

Existing commands, `assistant.toml`, v1 manifests, and default model behavior remain unchanged. The new command reads repository-relative fixture files only; it does not create research runs or alter the index.

## Scientific and provenance invariants

- Each corpus expectation names an actual repository source path; no uninspected equation or scientific claim is encoded as an answer key.
- The report labels the scope as evidence/tool evaluation, not scientific-result verification.
- Tool-status cases test installed registered capabilities, not correctness of their output.
- Future answer/derivation grading must capture conventions, source evidence, and independent checks before it can promote scientific claims.

## Required tests

1. Valid YAML loads and duplicate/malformed cases fail clearly.
2. Retrieval scoring handles matched, missed, and partial expected sources using a fake retriever.
3. Tool-status scoring handles available and absent tool IDs without local machine dependencies.
4. `jarvis eval run` emits parseable JSON and writes `--output` when requested.
5. Existing test suite remains green.

## Acceptance criteria

- At least 20 starter cases exist across all five fixture directories, including paper-reproduction cases under `literature/`.
- Every case has explicit expected evidence and a scoring threshold.
- `jarvis eval run` produces a machine-readable report without any LLM call.
- Reported case failures are data, not command crashes.
- The initial scope and limitations are documented.

## Model and routing implications

No runtime model-selection behavior changes. Honey could not be mechanically isolated in this environment, so no architecture or critical-review subagent was used; the main coordinator made this bounded interface decision and will perform a parent-level adversarial review before validation.

## Ordered implementation steps

1. Add strict case loading and deterministic scoring around existing retrieval/tool APIs.
2. Add the CLI command and focused tests.
3. Add 20 corpus/tool-grounded starter cases and suite documentation.
4. Run narrow tests, the eval command, and the relevant broader suite.
5. Inspect the diff, update progress, and checkpoint the milestone.
