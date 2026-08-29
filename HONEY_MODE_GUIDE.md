# Honey-aware Jarvis Codex workflow

Honey is useful for bounded software implementation. Architecture, scientific reasoning, evidence semantics, and independent review need explicit assumptions, alternatives, provenance, and checks that Honey must not suppress.

## Autonomous isolation policy

The agent, not the user, owns Honey isolation. Before spawning architecture, critical-review, or scientific agents, inspect the installed plugin source and current runtime evidence.

If Honey exposes a supported, reversible per-user state change that is writable without approval, record the original state, apply the smallest change, verify isolation where practical, and restore the state after the architecture/science phase. Never uninstall Honey or alter workspace-wide settings.

If isolation cannot be verified or requires approval, do not block. Do not spawn `jarvis_architect`, `jarvis_critical_reviewer`, PhysicsIntern, or future scientific agents; use the main Terra/high coordinator for the smallest necessary decision, record that limitation in the milestone specification, and continue. `jarvis_explorer` remains available for bounded factual investigation.

## Implementation mode

After an implementation-ready specification exists, Honey may guide ordinary code changes by the main coordinator, `jarvis_explorer`, and `jarvis_implementer`. It is optional: inability to enable or restore Honey never blocks implementation.
