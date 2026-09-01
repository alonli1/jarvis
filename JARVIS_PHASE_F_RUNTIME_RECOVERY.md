# JARVIS Phase F runtime recovery — use a compatible Codex runtime without user intervention

Continue Phase F from the existing blocker state.

The PhysicsIntern bootstrap and Honey isolation have already succeeded. Do not repeat them unless validation shows the disposable workspace is missing.

Current blocker facts:

- system/standalone `codex` reports version `0.144.1`;
- Antigravity's Codex extension previously produced rollout metadata identifying a newer runtime around `0.151.0-alpha.7.1`;
- standalone `codex exec` fails while loading `~/.codex/models_cache.json` with:
  `missing field 'base_instructions'`;
- do not hand-edit `base_instructions` into the cache;
- do not delete or overwrite user-global Codex state as the first remedy.

The goal is to resume Phase F autonomously using a compatible Codex runtime, while keeping plugins disabled for PhysicsIntern scientific runs.

## 1. Preserve current Phase F artefacts

Before recovery:

- inspect the existing PhysicsIntern workspace `/tmp/jarvis-physicsintern-phase-f` or the actual workspace path recorded by Phase F;
- preserve its `survey.md`, oracle output, bootstrap files, logs, and isolation evidence;
- preserve Jarvis-side Phase F evidence/progress files;
- do not accept/import the partial scientific result yet.

## 2. Inventory Codex runtimes

Identify all accessible Codex executables without modifying anything.

Use bounded methods such as:

```bash
command -v codex
type -a codex || true
codex --version
```

Then locate the Codex executable/runtime shipped with or used by the Antigravity/OpenAI Codex extension.

Prefer evidence from:

- the running extension process;
- Antigravity/VS Code extension installation directories;
- rollout/session metadata;
- executable paths referenced by extension logs/processes.

Do not perform an unbounded filesystem crawl.

For every candidate record:

- absolute path;
- version;
- whether it is the Antigravity/OpenAI extension runtime;
- whether it can run `features list`;
- whether it supports `--disable plugins`.

Prefer the newest trustworthy OpenAI Codex runtime already installed on the machine.

## 3. First recovery attempt: use the extension-compatible Codex executable

Do not invoke the old PATH `codex` if a newer extension-compatible executable is available.

Using the newer candidate, run a minimal plugin-disabled smoke test from the PhysicsIntern workspace.

Conceptually:

```bash
"<NEW_CODEX>" --disable plugins features list
```

Then run the smallest harmless `exec` test that verifies the model runtime can start and return a trivial response without dispatching scientific work.

Requirements:

- plugins disabled;
- use the existing authenticated user environment;
- do not modify Jarvis;
- do not modify global Codex cache/auth/config;
- capture stdout/stderr and version.

If the newer executable runs without the `base_instructions` error, designate it as `PHASE_F_CODEX` and use that exact executable for all remaining Phase F subprocesses.

Do not rely on bare `codex` afterward.

## 4. If the newer executable still conflicts with the shared cache

If the newer executable exists but the shared `~/.codex/models_cache.json` still causes a schema conflict, try an isolated temporary `CODEX_HOME` before touching global state.

Create a temporary Phase-F-only Codex home in a writable scratch location.

Populate only the minimum authentication/configuration needed to reuse the user's existing legitimate Codex authentication.

Do not copy:

- `models_cache.json`;
- plugins;
- Honey state;
- unrelated session history;
- memories;
- global logs.

Prefer read-only copying/symlinking of the minimum auth material if supported safely.

Then run:

```bash
CODEX_HOME="<PHASE_F_CODEX_HOME>" "<PHASE_F_CODEX>" --disable plugins ...
```

with an explicit model if needed.

The purpose is to force the compatible runtime to use its bundled/current model metadata instead of deserializing the incompatible shared cache.

Do not manually fabricate a models cache.

If the runtime automatically creates a fresh cache in the temporary CODEX_HOME, that is acceptable.

Record exactly what was copied and generated.

## 5. If no newer executable can be found

Only if no usable newer OpenAI Codex executable is already installed:

1. determine whether the environment permits obtaining a current official Codex CLI into a **temporary/local location** without replacing the user's global CLI;
2. prefer an official OpenAI distribution/release/package;
3. install/download locally into the Phase F scratch area;
4. verify checksum/source when practical;
5. do not replace the user's global `codex` binary;
6. use the local runtime only for Phase F.

If the environment lacks network/package tooling for this, record that as the next blocker.

## 6. Do not repair the global cache by hand

Do not add guessed `base_instructions` fields to `~/.codex/models_cache.json`.

Do not copy instruction strings from random repositories.

Do not overwrite authentication.

Do not uninstall/reinstall global Codex as the first solution.

If every isolated-compatible-runtime strategy fails and the only remaining fix is a global cache refresh, stop and report that exact situation rather than silently modifying user-global state.

## 7. Re-verify Honey isolation under the recovered runtime

Before resuming scientific work, rerun the plugin-disabled isolation audit using `PHASE_F_CODEX`.

Verify:

- plugins feature is false;
- Honey skill/directives are absent;
- PhysicsIntern workspace-local skills are visible;
- PhysicsIntern workspace-local roles are visible.

Use rollout/session JSONL or equivalent runtime evidence when available.

If Honey appears, do not proceed with scientific runs.

## 8. Resume Phase F, not restart it

Continue from the current Phase F checkpoint.

Do not repeat completed bootstrap work unless required.

The seeded free-scalar pilot that was rejected by the private symbolic oracle remains rejected; do not turn it into an accepted result.

Continue the intended five bounded known-answer investigations using the recovered `PHASE_F_CODEX`.

For every child `codex exec` or research process, call the exact recovered executable/path and keep plugins disabled.

## 9. Provider/network diagnostic

The old `codex doctor` reported provider-endpoint reachability failure from the old CLI's restricted environment.

Do not assume that means the newer extension-compatible runtime cannot reach the model service.

Test the recovered runtime directly with the harmless smoke `exec`.

If:
- model catalog/cache loading succeeds, but
- the actual model request cannot reach the provider,

then record the network/provider restriction as a separate blocker.

Do not conflate it with the `base_instructions` cache-schema failure.

## 10. Success criteria

Runtime recovery succeeds only if all are true:

1. a compatible Codex runtime starts;
2. no `missing field base_instructions` error occurs;
3. authentication works;
4. a trivial model `exec` succeeds;
5. plugins are mechanically disabled;
6. Honey is absent from runtime context;
7. PhysicsIntern local skills/roles are visible.

Once these pass, resume and complete Phase F autonomously.

## 11. Durable record

Update the Jarvis Phase F progress/evidence record with:

- old failing CLI path/version;
- recovered CLI path/version;
- whether the Antigravity extension runtime was reused;
- whether a temporary CODEX_HOME was required;
- exact Honey isolation verification;
- smoke-test result;
- any provider/network findings.

Do not ask the user for routine confirmation.

Only stop if:
- no compatible runtime is accessible/obtainable;
- authentication cannot be reused safely;
- provider network access is unavailable even in the recovered runtime;
- Honey cannot be isolated;
- the only remaining remedy requires modification of user-global Codex state.

Start recovery now.
