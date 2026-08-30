# Historical Phase F runtime blocker

> Phase F completed on 2026-08-30. The retained material below records the
> runtime and containment investigations that informed its eventual normal
> PhysicsIntern execution; it is not an active Phase F blocker.

Phase F cannot complete in the current Codex CLI runtime. The PhysicsIntern
bootstrap and Honey isolation succeeded, but the isolated process cannot sustain
the fresh-context research workflow.

## Completed setup evidence

- Official upstream `huggingface/physics-intern-skills` was cloned at
  `41d75f998710948e90b9254fba1cc501fe09fc84`.
- Its official `init-physics-intern.sh --host=codex` bootstrap created the
  disposable workspace `/tmp/jarvis-physicsintern-phase-f` with `AGENTS.md`,
  eight local skills, seven local roles, `.codex/config.toml`, `problem.md`,
  and `research_log.md`.
- `codex --disable plugins features list` reports `plugins ... false`.
  A plugin-disabled isolation audit found no Honey skill/directive and found
  all eight PhysicsIntern local skills and seven local roles.
- The first free-scalar pilot produced `survey.md`; its private symbolic oracle
  ran separately and rejected the seeded wrong-sign result.

## Blocking runtime evidence

- Codex CLI is `0.144.1`; authentication is configured.
- Every plugin-disabled `codex exec` attempt fails before the autonomous loop
  can integrate or dispatch its next stage with:

  ```text
  codex_models_manager::cache: failed to load models cache:
  missing field `base_instructions` at line 98 column 5
  ```

- `/home/alonli/.codex/models_cache.json` lacks `base_instructions` for
  `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-reserve`, `gpt-5.5`,
  `gpt-5.4`, `gpt-5.4-mini`, and `codex-auto-review`.
- `codex doctor` also reports provider-endpoint reachability failure from the
  CLI's own restricted environment. No global cache, authentication, or plugin
  configuration was modified.

The missing model-catalog field is an external Codex runtime defect. Continuing
would require modifying user-global Codex state or bypassing the CLI sandbox,
neither of which is authorized by the Phase F instruction. The workspace and
Jarvis evidence bundles were left intact; no scientific result was accepted,
imported, or claimed.

## Resolved by compatible extension runtime

This historical standalone-CLI blocker was resolved without modifying global
state.  The Antigravity OpenAI Codex extension executable at
`/home/alonli/.antigravity-ide/extensions/openai.chatgpt-26.825.41651-linux-x64/bin/linux-x86_64/codex`
reports `0.151.0-alpha.7.1`, starts a trivial authenticated model `exec`, and
does not emit the `base_instructions` failure.  Its `--disable plugins` feature
reports `plugins=false`; a fresh audit found no Honey directive/skill and the
expected eight PhysicsIntern skills plus seven roles.  This exact executable is
the Phase F runtime.  The old `0.144.1` PATH CLI is not used for Phase F.

F01 subsequently completed and was imported as provisional evidence; Phase F
is no longer runtime-blocked, but remains incomplete pending F02--F05.

## Current Phase F execution blocker: fresh-context dispatch unavailable

The recovered extension runtime starts models and isolates plugins correctly,
but its noninteractive `codex exec` host does not expose a usable
`spawn_agent` capability to the PhysicsIntern coordinator.  In the fresh F02
workspace, the user-invoked `autoresearch` run reached the survey dispatch and
emitted a collaboration `wait` call with no spawned receiver instead of a role
dispatch.  No F02 survey, derivation, computation, review, critique, answer,
or import was accepted.

PhysicsIntern requires fresh-context role dispatch; substituting the Honey-active
parent coordinator or manually performing scientific work would violate the
isolation and methodology contracts.  F02's prepared disposable workspace is
preserved at `/tmp/jarvis-physicsintern-phase-f02`.  The remaining requirement
is an authenticated, plugin-disabled Codex invocation mode that exposes both
`spawn_agent` and `wait_agent` to the generated local roles (or a documented
equivalent supplied by the installed runtime).  This is separate from the
resolved model-cache defect.

## Current Phase F execution blocker: process capsule filesystem escape

The Phase-F-only process dispatcher successfully created separate fresh Codex
sessions, disabled plugins, staged a harmless input, and validated the surveyor
and planner smoke artifacts.  However, a planner process could see the parent
F02 workspace through `../../../` (its own `git status` showed parent files),
so the capsule is not a mechanical information boundary.  No F02 artifact from
that workspace is accepted on this transport.

`bubblewrap 0.11.1` is installed, but its minimal namespace test fails with
`No permissions to create a new namespace, likely because the kernel does not
allow non-privileged user namespaces.`  Without a kernel-supported filesystem
namespace (or an equivalent OS-level containment mechanism), a process could
read a private oracle or forbidden review if it knew a path.  Continuing would
violate the required oracle and reviewer isolation.  The adapter and smoke
capsules remain only under `/tmp`; no Jarvis or global Codex configuration was
modified.

## Final local containment result: Landlock enforces, Codex cannot use it strictly

Kernel `Linux 7.0.0-29-generic` exposes Landlock ABI 8. The fail-closed direct
syscall probe under `/tmp/phase-f-landlock` allowed its staged directory and
denied `/etc/hostname` with `EACCES`; the launcher also denied a parent-workspace
read in a direct shell test.

The recovered Codex runtime cannot complete a model turn under that policy. An
external capsule with only the exact authentication file, binary, TLS/DNS paths,
and runtime libraries reaches Codex but fails to initialize its in-process
app-server client with `Permission denied`. Granting global `.codex` IPC/state
would violate the dedicated-state and confidentiality requirements. No global
configuration or kernel setting was changed.

F02--F05 require an isolated worker/runtime with a dedicated Codex state home
under a strict read allowlist. F01 remains valid.
