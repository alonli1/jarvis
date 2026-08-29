# Task: implement the next approved Jarvis AI-physicist milestone

Honey may be used for bounded implementation but is never a completion gate. Do not ask the user to enable it, disable it, or start a fresh session.

Read:
1. the current root `AGENTS.md`;
2. `HONEY_MODE_GUIDE.md`;
3. `JARVIS_AI_Physicist_Repo_Aware_Implementation_Roadmap_2026-08-29.md`;
4. the implementation-ready milestone/specification produced by the preceding Honey-OFF architecture session.

## Hard routing boundary

Unless Honey isolation has been verified by the agent, do not spawn `jarvis_architect`, `jarvis_critical_reviewer`, PhysicsIntern agents, or future Jarvis scientific agents. You may use:
- the main Terra/high coordinator;
- `jarvis_explorer` for bounded read-only exploration;
- `jarvis_implementer` for bounded code changes.

If the approved specification is missing, materially ambiguous, or a consequential architecture/scientific-state decision becomes necessary, write `ARCHITECTURE_HANDOFF.md` containing:
- the unresolved question;
- repository evidence and relevant files/symbols;
- why it is consequential;
- alternatives discovered;
- tests/failures that exposed it;
- the smallest decision needed to resume implementation.
Resolve the smallest decision using the autonomous Honey-isolation policy, update the specification, and resume.

## Implementation procedure

1. Verify current HEAD and confirm the approved milestone still applies.
2. Use `jarvis_explorer` only where targeted read-heavy exploration saves parent context.
3. Implement the smallest coherent milestone; do not expand scope.
4. Preserve existing retrieval, Dropbox, MCP, graph, skills, run-bundle, and computation infrastructure unless the specification explicitly migrates it.
5. Preserve scientific validation/provenance requirements even when Honey/YAGNI would otherwise reduce code.
6. Add/update tests for changed behavior.
7. Run narrow tests first and broader relevant tests afterward.
8. Summarize changed files, tests, unresolved risks, and the next roadmap gate.

Checkpoint each validated milestone, update progress, and continue autonomously until a documented stop condition occurs.
