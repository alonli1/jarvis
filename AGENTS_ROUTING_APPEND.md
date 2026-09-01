## Codex development routing

This section governs **development of the Jarvis software repository**. It does not replace the four scientific research skills under `.agents/skills/`, and it must not change their scientific contracts.

### Default operating mode

Use the main Codex thread as the coordinator and integration owner. The project-local Codex config makes the ordinary parent model `gpt-5.6-terra` at high reasoning effort.

Do not spawn a subagent for trivial work when delegation would cost more than doing the task directly. Delegate when it reduces context pollution, enables useful parallelism, or materially improves reasoning quality.

### Named development agents

- `jarvis_explorer`: use for read-only repository search, dependency tracing, test inspection, log/config inspection, and current-state inventory. Prefer this agent for independent parallel read-heavy tasks.
- `jarvis_implementer`: use for the default bounded software implementation after the requirement is understood: features, tests, adapters, schemas, CLI work, refactors, and ordinary bug fixes.
- `jarvis_architect`: use for consequential or ambiguous architecture, especially AI-physicist orchestration, scientific state/evidence semantics, model routing, cross-cutting interfaces, or decisions costly to reverse.
- `jarvis_critical_reviewer`: use only for high-consequence independent review, repeated failures, or changes that could affect scientific correctness, orchestration, routing, provenance, or research-state semantics.

### Escalation policy

Prefer the cheapest model that can correctly complete and verify the task:

`Luna -> Terra -> GPT-5.6 high -> GPT-5.6 xhigh`

Do not escalate merely because a task is large. Escalate because ambiguity, coupling, epistemic risk, repeated failure, or irreversible consequences justify stronger reasoning.

If a cheaper agent produces sufficient evidence and the result passes appropriate tests/review, do not repeat the same work with a stronger model.

Use `jarvis_critical_reviewer` only when the expected value of independent expensive review exceeds its token cost.


### Honey runtime boundary

Honey is installed globally and may be active. Treat Honey state as a hard routing boundary, not merely a style preference.

**When Honey is ON** (including lite/full/ultra): operate in software-implementation mode. The main Terra coordinator may work directly and may use `jarvis_explorer` and `jarvis_implementer`. Do **not** spawn `jarvis_architect`, `jarvis_critical_reviewer`, PhysicsIntern agents, or future Jarvis scientific agents while Honey is active. If consequential architecture/scientific ambiguity appears, stop before deciding it and prepare a handoff for a Honey-OFF session.

**When Honey is OFF**: architecture/science mode is allowed. `jarvis_architect`, `jarvis_critical_reviewer`, and scientific agents may be used according to the escalation policy.

Do not treat `honey lite` as isolation: Honey's SubagentStart hook still injects its directive whenever the mode is anything other than `off`.

After an architecture/science decision becomes an implementation-ready specification, return to a fresh Honey-ON software session for bounded coding. See `HONEY_MODE_GUIDE.md`.

### Parallelism

Parallelize independent read-heavy tasks such as codebase exploration, test inventory, documentation checks, or separate non-overlapping investigations.

Do not let multiple agents concurrently edit overlapping files. The main thread owns dependency ordering, integration, final tests, and the final user-facing summary.

### Scientific boundary

Jarvis's `.agents/skills/` remain the source of truth for literature understanding, research ideation, reproducible computation, and library management.

Do not route scientific derivations, literature judgments, novelty claims, or scientific validation through generic software minimization rules. When implementing a scientific algorithm from the literature, separate:

1. scientific specification and validation, which must preserve assumptions, conventions, provenance, checks, and citations; from
2. software implementation, which may be delegated to `jarvis_implementer` and optimized for simplicity.

Honey-style output/code minimization is acceptable for ordinary software work, but it must never suppress scientific evidence, independent checks, failed approaches that matter, or required provenance.

### Roadmap implementation discipline

When implementing the AI-physicist roadmap:

1. read the current roadmap and current repository state before changing architecture;
2. use `jarvis_explorer` to gather bounded evidence when several files/subsystems must be inspected;
3. use `jarvis_architect` before changing a consequential interface or scientific-state model;
4. implement only the next coherent milestone, not the entire roadmap in one patch;
5. preserve existing working retrieval, Dropbox, MCP, graph, skills, run-bundle, and computation infrastructure unless the roadmap explicitly requires a migration;
6. add tests for each new behavior;
7. run relevant tests before declaring a milestone complete;
8. use `jarvis_critical_reviewer` only at milestone boundaries or when failures/risks justify it.
