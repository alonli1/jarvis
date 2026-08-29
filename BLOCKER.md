# Phase F execution blocker

Phase F's scientific bootstrap experiments cannot run in this session.

- The official `physics-intern@physics-intern-codex` plugin is installed in the
  local cache and contains `init-physics-intern`, but that skill is absent from
  this session's live skill catalog.
- Honey is active in this session. Its installed cache exposes skills only; no
  supported writable per-user state or hook implementation is present. The
  repository policy therefore forbids PhysicsIntern, architecture, critical
  review, and all scientific subagents while this injection is active.
- The installed bootstrap skill is restricted to an explicit user invocation in
  a dedicated empty research workspace. It must not be run from this repository.

Safe non-scientific preparation is complete at Phase F's import/telemetry
checkpoint: external artifacts can now be copied into a JARVIS run as
provisional, digest-recorded evidence and role-tagged model telemetry can be
persisted.

To resume Phase F, use a session where both conditions hold: the official skill
is live in the skill catalog and Honey isolation is mechanically verified. Then,
with an explicit `$init-physics-intern` invocation, create a dedicated empty
PhysicsIntern workspace; use JARVIS retrieval/computation runs as evidence/tool
substrate and perform the five known-answer investigations.
