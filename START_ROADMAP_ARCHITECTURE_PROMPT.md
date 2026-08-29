# Task: prepare the next Jarvis AI-physicist milestone

The agent owns Honey isolation. Inspect the installed plugin and runtime evidence; do not ask the user to toggle Honey or restart. If Honey cannot be mechanically isolated, do not spawn architecture/critical-review/scientific agents: make and record the smallest necessary main-coordinator decision instead.

Read:
1. root `AGENTS.md`;
2. `HONEY_MODE_GUIDE.md`;
3. `JARVIS_AI_Physicist_Repo_Aware_Implementation_Roadmap_2026-08-29.md`;
4. the current repository state and recent commits.

## Goal

Produce one implementation-ready next milestone for the AI-physicist roadmap without implementing the whole roadmap.

## Procedure

1. Verify the roadmap baseline against current HEAD and identify any assumptions invalidated by newer commits.
2. Use `jarvis_explorer` for bounded repository evidence when useful.
3. Use `jarvis_architect` for consequential design only when Honey isolation is verified; otherwise use the main coordinator and record the limitation.
4. Use `jarvis_critical_reviewer` only when Honey isolation is verified and the milestone changes model routing, orchestration, research-state/evidence/provenance semantics, or independent expensive review is otherwise justified.
5. Do not modify production code unless a tiny architecture-enabling probe is truly necessary; prefer producing a precise specification.
6. Write `NEXT_MILESTONE_SPEC.md` containing:
   - objective and non-goals;
   - current-state evidence with files/symbols;
   - exact interfaces/data models/config changes;
   - migration/backward-compatibility constraints;
   - required tests and acceptance criteria;
   - model/routing implications;
   - scientific/provenance invariants;
   - ordered implementation steps.
7. Proceed directly to implementation after the specification; do not wait for a user or session transition.
