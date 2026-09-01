# Task: install Jarvis project-local Codex model routing

Apply the following configuration to the current `alonli1/jarvis` repository.

## Goal

Configure Codex so daily Jarvis development uses a Terra/high parent, delegates cheap read-heavy exploration to Luna, ordinary implementation to Terra/high, consequential architecture to GPT-5.6/high, and only exceptional independent review to GPT-5.6/xhigh.

This is a **development routing layer only**. Preserve Jarvis's existing `.agents/skills/` scientific workflows exactly. Do not replace or redesign them as part of this task. Honey is currently installed/active; also install the Honey runtime boundary from `HONEY_MODE_GUIDE.md` and `AGENTS_ROUTING_APPEND.md`.

## Required steps

1. Read the current root `AGENTS.md` and check whether a `.codex/` directory already exists.
2. Do not overwrite unrelated existing Codex settings. If `.codex/config.toml` already exists, merge the settings below conservatively and report any conflict.
3. Create these project-scoped custom agents under `.codex/agents/`:
   - `jarvis-explorer.toml`
   - `jarvis-implementer.toml`
   - `jarvis-architect.toml`
   - `jarvis-critical-reviewer.toml`
4. Merge the section in `AGENTS_ROUTING_APPEND.md` into root `AGENTS.md` exactly once under the heading `## Codex development routing`.
5. Do not modify `.agents/skills/`, scientific workflow semantics, Jarvis source code, Dropbox configuration, or the AI-physicist roadmap in this setup task.
6. Validate that all TOML files parse successfully.
7. Show the resulting diff and summarize the model assigned to each custom agent.
8. Verify that the merged `AGENTS.md` contains the Honey runtime boundary: Honey ON permits only the main coordinator, `jarvis_explorer`, and `jarvis_implementer`; Honey OFF is required for architect/reviewer/scientific agents.
9. Stop after the routing setup. Do not begin implementing the AI-physicist roadmap in the same session.

## Desired `.codex/config.toml`

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[agents]
enabled = true
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

## `jarvis_explorer`

Use model `gpt-5.6-luna`, reasoning `medium`, sandbox `read-only`. It must only gather repository evidence and never edit files or perform scientific derivations.

## `jarvis_implementer`

Use model `gpt-5.6-terra`, reasoning `high`, sandbox `workspace-write`. It is the default bounded implementation worker and must preserve scientific validation/provenance requirements.

## `jarvis_architect`

Use model `gpt-5.6`, reasoning `high`, sandbox `read-only`. It handles consequential AI-physicist architecture, routing, scientific-state/evidence semantics, cross-cutting interfaces, and hard ambiguous failures. It should recommend rather than edit.

## `jarvis_critical_reviewer`

Use model `gpt-5.6`, reasoning `xhigh`, sandbox `read-only`. It is an expensive independent reviewer used only for high-consequence changes, repeated failures, or scientific/epistemic correctness risks.

The complete intended developer instructions for all four agents are available in the accompanying `.codex/agents/*.toml` files. If those files are present in the working tree, use them as the exact source of truth rather than paraphrasing them.

## Important

Project `.codex/` configuration is loaded for trusted projects. After this setup is complete, I will start a **new Codex session** so the new project-local config and custom agents are loaded cleanly.
