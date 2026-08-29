# Milestone spec — Phase D runtime model profiles and telemetry

## Objective

Add provider-neutral configured model profiles and request telemetry around the existing LiteLLM boundary, without changing retrieval behavior or adding task routing.

## Scope

- Extend `assistant.toml`/`config.py` with optional profiles while preserving `assistant.default_model`.
- Replace the bare `llm.complete()` return path with a structured internal result that preserves the existing text-returning compatibility wrapper.
- Record provider/model, latency, and usage when LiteLLM exposes it; telemetry absence must not fail an answer.
- Add explicit profile selection to `jarvis ask`; no automatic routing.

## Non-goals

- No router, classifier, budget policy, orchestration, claim promotion, or provider migration.
- No change to retrieval source selection, prompt instructions, or document-access semantics.

## Compatibility/provenance invariants

- Existing `jarvis ask QUESTION --model MODEL` remains valid and semantically unchanged.
- Default behavior continues to use `assistant.default_model` when no profile/override is selected.
- Telemetry is additive, provider-neutral, and never fabricates unavailable usage values.
- Model usage records retain the existing run-bundle provenance boundary; no new run is required for ordinary `ask`.

## Required tests and acceptance

1. Old configuration loads unchanged; profiles validate unique names and required model IDs.
2. Text compatibility wrapper returns unchanged output.
3. Structured result captures supplied usage/latency and safely handles missing usage.
4. `jarvis ask` accepts a configured profile and rejects unknown profiles clearly.
5. Existing tests and Phase B eval report remain green.

## Review limitation

Honey isolation remains unavailable, so the main coordinator must make the bounded profile/telemetry design decision and perform a parent-level compatibility review; do not spawn architecture or critical-review agents.
