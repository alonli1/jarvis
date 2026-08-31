# Phase J milestone J2 — host-neutral task dispatch

## Objective

Let an IDE agent, Codex session, or extension-hosted agent execute a Jarvis task
without requiring a model API, Ollama, MCP, or a provider-specific adapter.

## Interface

1. `jarvis dispatch schedule RUN_ID PLAN.json` validates and persists a research
   plan, then materializes only ready task packets.
2. `jarvis dispatch export RUN_ID TASK_ID` writes a validated packet plus a host
   contract to `host_dispatch/TASK_ID.json` in the run.
3. A host starts a fresh context, works only from that packet and its allowed
   run-relative dependencies, then writes a result file.
4. `jarvis dispatch import-result RUN_ID TASK_ID RESULT --host HOST
   --fresh-context` copies that file into `provisional/`, records an explicit
   decision entry, and optionally records truthful provider/model telemetry.

## Invariants

- Packet identity and plan digest must match the persisted run.
- The host declaration of a fresh context is required but is not treated as
  independently verified isolation.
- Host output remains provisional: import cannot complete a task, promote a
  claim, or create scientific verification.
- Packet exports contain no reviewer artifacts; existing task-packet path checks
  remain authoritative.
- A host may omit provider/model metadata. Jarvis must not invent it.

## Scope

This is a transport for a human- or IDE-hosted agent, including this Codex
workspace. It is not a background agent loop, a substitute for PhysicsIntern
isolation, or evidence of native/PhysicsIntern parity.

## Routing limitation

Honey instructions are visible in the coordinator session, so no architecture or
scientific subagent was used. The coordinator selected the smallest additive
protocol and retained existing Manifest v2 provisional-artifact semantics.
