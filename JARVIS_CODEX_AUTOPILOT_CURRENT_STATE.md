# JARVIS AUTOPILOT — continue from the current Codex-routing state with no user intervention

You are operating inside the current `alonli1/jarvis` repository.

The user has already completed the initial Codex routing installation and the explorer smoke test. The smoke test was independently verified from a Codex rollout JSONL:

- a real subagent spawned;
- `agent_role = jarvis_explorer`;
- runtime model = `gpt-5.6-luna`;
- reasoning effort = `medium`;
- the custom explorer instructions loaded;
- the explorer made no file modifications;
- the runtime sandbox still reported `workspace-write` rather than the intended `read-only`.

Do **not** reinstall the routing setup and do **not** overwrite the working `.codex/` configuration just because a newer guide exists.

The user's goal is now to proceed with the Jarvis AI-physicist roadmap with **no routine user intervention**. Do not ask the user to copy files, toggle Honey, start fresh sessions, choose models, approve ordinary architectural choices, or manually advance between milestones. Make the safest reasonable choice yourself and continue.

The user deliberately removed document-level privacy tiers. Do not reintroduce them.

---

## 1. First inspect the current state

Before changing anything:

1. Read root `AGENTS.md`.
2. Inspect `.codex/config.toml`.
3. Inspect `.codex/agents/*.toml`.
4. Locate and read the current AI-physicist roadmap. Prefer:
   `JARVIS_AI_Physicist_Repo_Aware_Implementation_Roadmap_2026-08-29.md`
   but if it was moved, find the current repo-aware roadmap by name/content.
5. Read any existing:
   - `HONEY_MODE_GUIDE.md`
   - `START_ROADMAP_ARCHITECTURE_PROMPT.md`
   - `START_ROADMAP_IMPLEMENTATION_PROMPT.md`
   - `NEXT_MILESTONE_SPEC.md`
   - `ARCHITECTURE_HANDOFF.md`
6. Inspect current `git status`, branch, HEAD, and recent commits.
7. Do not discard or overwrite unrelated uncommitted user work.

Treat the repository contents as authoritative over older setup bundles.

---

## 2. Preserve the already-working routing configuration

Do not rerun the original routing installer.

Unless a current file is demonstrably invalid, preserve:

```text
.codex/config.toml
.codex/agents/jarvis-explorer.toml
.codex/agents/jarvis-implementer.toml
.codex/agents/jarvis-architect.toml
.codex/agents/jarvis-critical-reviewer.toml
```

The intended roles remain:

- main coordinator: `gpt-5.6-terra`, high;
- `jarvis_explorer`: `gpt-5.6-luna`, medium;
- `jarvis_implementer`: `gpt-5.6-terra`, high;
- `jarvis_architect`: `gpt-5.6` / Sol, high;
- `jarvis_critical_reviewer`: `gpt-5.6` / Sol, xhigh.

Do not change these merely to simplify the task.

The explorer's hard read-only sandbox was not enforced by the Antigravity Codex runtime in the smoke test. Therefore continue treating the explorer as logically read-only through its developer instructions and verify that it does not modify files. Do not spend time redesigning the whole routing system solely to fix that sandbox discrepancy unless it becomes a real safety/correctness problem.

---

## 3. Patch stale Honey instructions automatically

The user's actual environment is:

- Codex extension inside Antigravity IDE;
- Honey is installed as a Codex plugin;
- `/honey off` returned:
  `Couldn’t persist the setting: this environment has no node and no CLAUDE_PLUGIN_ROOT. I’ll treat Honey as off for this conversation.`

Therefore any repository instruction that *requires the user* to run `/honey off`, `/honey full`, disable/enable the plugin manually, replace bundle files, or restart sessions is stale for autonomous operation.

Patch only the relevant documentation/instruction sections so that:

- Honey is desirable for bounded software implementation;
- Honey must not influence consequential architecture or scientific/research-agent reasoning;
- **the agent, not the user, owns Honey isolation attempts and fallback behavior**;
- the workflow never blocks solely because Honey cannot be toggled.

Do not replace the whole `AGENTS.md`. Merge/update only the Honey/autopilot portions needed.

If `HONEY_MODE_GUIDE.md` exists, update it to describe the autonomous policy below.

---

## 4. Autonomous Honey isolation policy

The goal is to keep Honey out of architecture/scientific reasoning without requiring the user to operate plugin UI.

### 4.1 Determine the actual Honey mechanism

Inspect the installed Honey plugin files and current environment read-only.

From the prior rollout, Honey was visible under a path similar to:

```text
~/.codex/plugins/cache/greenpt/honey/1.1.0/
```

Do not assume the exact version/path; discover it.

Determine, from Honey's own installed source, how its active state is represented and how its `SubagentStart`/skill activation is gated.

Do not rely on memory when the installed plugin source can answer the question.

### 4.2 Preferred isolation

If Honey's own installed code shows that removing/altering a small per-user state file is the supported way to make the hook inactive, and the current sandbox permits that operation **without requiring user approval**, you may use that mechanism.

Before changing such state:

1. record the original state;
2. make the smallest reversible change;
3. never uninstall Honey;
4. never alter workspace-wide/admin settings;
5. never delete the plugin installation/cache itself;
6. restore the original state when useful after the architecture/science phase.

If modifying Honey state would require explicit user approval, do **not** stop and ask. Use the fallback below.

### 4.3 Verify isolation when practical

After an automated Honey-off attempt, verify it using the strongest evidence available in this environment:

- child/subagent developer instructions;
- rollout/session JSONL if locally accessible;
- absence of Honey hook/skill injection;
- absence of Honey-specific directives in the child context.

Do not accept a model's self-report alone when runtime evidence is accessible.

### 4.4 Safe fallback if Honey cannot be isolated automatically

If Honey cannot be safely disabled without user intervention:

- **do not spawn `jarvis_architect`, `jarvis_critical_reviewer`, PhysicsIntern, or future scientific agents while Honey injection is active**;
- perform the necessary architecture decision in the main Terra/high coordinator context instead;
- use `jarvis_explorer` only for bounded factual repository exploration if helpful;
- explicitly record in the milestone spec that the Sol architecture review was skipped because Honey could not be mechanically isolated;
- continue rather than asking the user to toggle anything.

Correctness and autonomous progress are more important than perfectly realizing the preferred model mix.

For an especially consequential decision, perform two independent parent-level analyses at different points in the workflow and compare them rather than spawning a Honey-contaminated high-capability reviewer.

---

## 5. Prepare the next milestone automatically

If there is no valid current `NEXT_MILESTONE_SPEC.md`, produce one.

Use the current roadmap and current repository state, not an old baseline.

Procedure:

1. Compare the roadmap assumptions with current HEAD.
2. Identify the **next coherent unmet milestone**, not the whole roadmap.
3. Use `jarvis_explorer` for bounded repository evidence when it saves parent context.
4. If Honey has been mechanically isolated, use `jarvis_architect` for consequential design decisions.
5. If Honey cannot be isolated, use the main Terra/high coordinator for architecture as described above.
6. Use `jarvis_critical_reviewer` only if:
   - Honey is verified isolated; and
   - the milestone changes model routing, orchestration, research-state/evidence/provenance semantics, or repeated failures justify expensive independent review.
7. Write/update `NEXT_MILESTONE_SPEC.md`.

The specification must contain:

- objective;
- non-goals;
- current-state evidence with files/symbols;
- exact interfaces/data models/config changes;
- backward-compatibility/migration constraints;
- scientific/provenance invariants;
- required tests;
- acceptance criteria;
- model/routing implications;
- ordered implementation steps;
- any review/isolation limitations encountered.

Do not implement multiple roadmap phases in one milestone.

---

## 6. Implement the approved milestone automatically

After the milestone spec is complete, proceed directly to implementation. Do not wait for user confirmation.

Preferred implementation routing:

- main Terra/high coordinator owns integration;
- `jarvis_explorer` may gather targeted read-only evidence;
- `jarvis_implementer` handles bounded code changes;
- Honey may be active for ordinary software implementation if available.

If Honey was automatically disabled and can be safely restored using the verified mechanism, restore the original Honey state before software implementation.

If Honey cannot be restored automatically, simply continue implementation without Honey. Honey is an optimization, not a correctness requirement.

Implementation rules:

1. verify HEAD again before editing;
2. preserve existing retrieval, Dropbox, literature APIs, graph, MCP, skills, run-bundle, and computation infrastructure unless the milestone explicitly migrates them;
3. make the smallest coherent compatible change;
4. do not reintroduce document-level privacy tiers;
5. add/update tests for changed behavior;
6. run narrow tests first;
7. run the relevant broader test suite;
8. run formatting/lint/type checks that are already part of the repository's normal workflow;
9. fix failures caused by your changes;
10. do not silently weaken tests to make them pass.

If a new consequential architectural ambiguity appears during implementation:

- pause code changes;
- write/update `ARCHITECTURE_HANDOFF.md`;
- resolve it yourself using the Honey-isolation policy above;
- update `NEXT_MILESTONE_SPEC.md`;
- resume implementation;
- do not ask the user unless a genuine external credential/permission or destructive choice makes autonomous progress impossible.

---

## 7. Milestone validation

Before declaring a milestone complete:

1. inspect the diff;
2. ensure no unrelated files were modified;
3. ensure scientific/provenance invariants remain intact;
4. run the relevant tests;
5. record unresolved risks;
6. compare implementation against every acceptance criterion in `NEXT_MILESTONE_SPEC.md`.

For consequential milestones, if Honey isolation is verified, use `jarvis_critical_reviewer` for an independent review when its value justifies the cost.

If Honey isolation is not available, perform a structured parent-level adversarial review instead and record that the xhigh independent review was deferred.

---

## 8. Git discipline

Do not push directly to `master` unless the repository/user's existing workflow clearly already expects that.

If currently on `master` and no dedicated roadmap branch exists, create a sensible development branch before substantial code changes, for example:

```text
ai-physicist-roadmap
```

Do not discard existing uncommitted work.

At each successfully validated milestone:

- create a clear commit if repository permissions/workflow allow it without user interaction;
- otherwise leave a clean, reviewable working-tree diff and continue.

Never force-push.

---

## 9. Continue automatically through later milestones

The user does not want to manually advance the process after every milestone.

Therefore, after one milestone is validated:

1. update a durable progress file such as `docs/AI_PHYSICIST_PROGRESS.md`;
2. mark the completed milestone and evidence/tests;
3. identify the next coherent unmet milestone;
4. generate a fresh `NEXT_MILESTONE_SPEC.md`;
5. continue the same architecture → implementation → validation cycle.

However, do not run indefinitely without checkpoints.

After each milestone, create a durable checkpoint in the repository so work is recoverable even if the Codex session ends.

Continue until one of these stop conditions occurs:

- the current roadmap is fully implemented;
- an external credential/account/permission is genuinely required and unavailable;
- a destructive or irreversible choice cannot be made safely from repository evidence;
- the remaining step requires physical/user-only interaction;
- the environment imposes a hard execution limit.

Do **not** stop merely to ask whether to continue.

When a stop condition occurs, leave:
- the repository in the safest recoverable state possible;
- `docs/AI_PHYSICIST_PROGRESS.md` current;
- a concise `BLOCKER.md` describing exactly what remains and why it cannot be completed autonomously.

---

## 10. Do not overbuild

The roadmap is a delta from an already-functional Jarvis harness.

Do not rebuild:

- hybrid retrieval;
- Dropbox corpus sync;
- literature adapters;
- citation graph;
- MCP;
- the four foundational `.agents/skills/`;
- deterministic run bundles;
- the existing computation registry/workbench;

unless a concrete milestone requires a migration.

The central missing layer is the AI-physicist brain/orchestration/evaluation capability, not a replacement for the working harness.

---

## 11. Cost/model discipline

Optimize for verified progress per expensive-model token.

Use:

- Luna for bounded read-heavy exploration;
- Terra/high for ordinary implementation and integration;
- Sol/high only for consequential architecture when Honey is verified isolated;
- Sol/xhigh only for exceptional independent review when Honey is verified isolated.

Do not repeat satisfactory work with a stronger model merely because it is available.

Do not retry a weak approach repeatedly; escalate reasoning or change method when a real failure indicates it.

---

## 12. Start now

Do not ask the user to perform setup steps.

Begin by auditing the current repository state and determining:

1. what routing configuration is already installed;
2. what Honey-related files are stale;
3. whether Honey can be isolated automatically in this environment;
4. whether a valid `NEXT_MILESTONE_SPEC.md` already exists;
5. what the next coherent roadmap milestone is.

Then patch the stale Honey instructions, prepare the milestone spec, implement it, validate it, checkpoint progress, and continue autonomously under the rules above.

Only surface a blocker if it is genuinely impossible to proceed without external/user-only action.
