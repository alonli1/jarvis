# JARVIS Phase F continuation — process-isolated PhysicsIntern role dispatch

Continue Phase F from the current checkpoint.

Current facts:
- F01 passed independent oracle validation and was provisionally imported with sanitized artifacts.
- PhysicsIntern bootstrap succeeded in the disposable Phase F workspace.
- Honey/plugin isolation succeeded.
- The recovered Codex runtime can execute model calls.
- Native PhysicsIntern Codex dispatch through `spawn_agent` is not reliable/usable in the recovered `codex exec` host.
- F02 workspace state is preserved.
- No scientific result from F02 or later has been bypassed or accepted.

Do not restart Phase F from scratch.

## 1. Preserve the scientific methodology

PhysicsIntern requires fresh-context substantive work, independent review, durable artifacts, strict file ownership, flag disposition, and robust evidence before promotion.

Native `spawn_agent` is only the current Codex host transport. For Phase F, replace only that transport with fresh OS-process dispatch.

Do not weaken:
- fresh-context review;
- reviewer independence;
- critique independence;
- no-single-verdict promotion;
- oracle secrecy;
- main-agent integration discipline.

## 2. Do not modify upstream PhysicsIntern methodology

Do not edit the cloned upstream `huggingface/physics-intern-skills` methodology source.

Implement a Phase-F-only adapter in the disposable validation area, clearly named, e.g.:

```text
phase_f_process_dispatch.py
```

Treat it as host/evaluation glue around the rendered PhysicsIntern workspace.

## 3. Use the recovered Codex runtime exactly

Use the exact recovered Codex executable that already passed the runtime recovery smoke test.

Do not fall back to the old incompatible PATH `codex`.

Record for every dispatch:
- absolute Codex executable path;
- version;
- CODEX_HOME;
- model;
- reasoning effort;
- plugin-disable arguments;
- working directory;
- exit status.

Every scientific process must run with plugins disabled using the already-verified mechanism.

## 4. Fresh process per role

For every PhysicsIntern role invocation, launch a new `codex exec` process.

Never use:
- `spawn_agent`;
- `wait_agent`;
- session resume;
- shared conversation history;
- a prior role session ID.

Each dispatch must start from a fresh Codex context.

## 5. Source role instructions from the rendered workspace

Do not invent simplified replacement prompts.

For each role:
1. read the exact rendered role definition under `.codex/agents/<role>.toml`;
2. parse its current instructions/metadata;
3. build the process prompt from:
   - the rendered PhysicsIntern role instructions;
   - the exact dispatch brief/current task;
   - only permitted staged inputs;
   - the required artifact/output contract;
   - PhysicsIntern's standard return contract.

Preserve upstream role text as faithfully as possible.

Record a hash of the role file and final dispatch prompt.

## 6. Create an isolated role capsule for every dispatch

Create a unique temporary capsule containing only what the role is allowed to see:

```text
AGENTS.md
input/
output/
metadata.json
```

Do not copy:
- private oracle outputs;
- expected-answer files;
- other Phase F cases;
- hidden evaluator notes;
- forbidden sibling reviews;
- coordinator scratch reasoning;
- secrets;
- Honey/plugin state.

Run `codex exec` with the capsule as working directory.

Mechanical staging is preferred over prompt-only prohibitions.

## 7. Minimum visibility boundaries

Surveyor may receive the problem and permitted literature context, but not oracle/expected-answer material.

Planner may receive problem, survey, and only current PhysicsIntern-permitted planning context.

Deriver may receive problem, exact derivation brief, allowed conventions/established results; never oracle, expected answer, or steering review verdicts.

Computer may receive problem, computation brief, allowed conventions/results and necessary tools; never oracle/expected answer.

Reviewer must run in a fresh process. It may receive the target artifact plus allowed problem/convention/dependency context. It must not receive the target agent's hidden conversation, sibling reviews, oracle, expected answer, or coordinator opinion.

Critic must run fresh and receive only the current strategic context permitted by PhysicsIntern. If prior critiques are represented only by one-line summaries, enforce that mechanically.

Finalizer receives only the state/artifacts permitted by current PhysicsIntern.

Use the actual rendered PhysicsIntern skills/AGENTS rules as the authority if they are stricter.

## 8. Output contract

Each role process writes exactly its owned artifact.

After exit:
1. verify exit status;
2. verify expected artifact exists;
3. verify non-empty content;
4. validate required section/schema structure;
5. verify final reply/last-message contract when applicable;
6. preserve stdout/stderr/JSONL provenance;
7. reject if artifact and return contract materially disagree.

Do not trust exit code alone.

If using `--output-last-message`, create its parent directory first and verify the output independently.

Only after validation may the coordinator copy/import the role artifact into the PhysicsIntern workspace.

## 9. Main-agent integration remains unchanged

After each validated return, perform PhysicsIntern's normal integration loop:

1. read `## Summary` / `## Result` / `## Flags`;
2. update `research_log.md`;
3. disposition every flag in `notes/flags.md`;
4. update `plan.md` only as allowed;
5. commit the logical step;
6. decide the next role dispatch.

Role processes must not edit coordinator-owned state.

## 10. Independence checks

Before accepting every role result verify:
- a new process/session was used;
- no resume ID was supplied;
- no prior role transcript was provided;
- staged-input manifest contains only permitted inputs;
- oracle/expected-answer paths are absent;
- plugins/Honey are disabled;
- role prompt hash matches the current rendered role.

Record these checks explicitly for reviewers and critics.

## 11. Private oracle stays outside the research plane

Oracle/reference validation remains evaluator-only.

No role process may know:
- intentional seeded errors;
- expected sign/value;
- oracle verdict;
- pass/fail label.

Only after PhysicsIntern has completed/integrated a case may the evaluator compare it against the oracle/reference answer.

F01 remains valid and must not be redone.

## 12. Validate the transport adapter before F02

Before resuming F02, run a non-scientific transport smoke test:

1. launch two separate role processes;
2. verify distinct fresh session/process metadata;
3. verify plugins disabled in both;
4. verify each sees only its staged inputs;
5. verify each writes only its allowed output;
6. where practical, place a harmless sentinel outside the capsule and verify it is not visible from the capsule.

Then run a tiny harmless scientific-role test.

Only after transport validation passes should F02 resume.

## 13. Resume F02 through F05

Resume from preserved F02 state.

Do not redo F01.

Run the remaining four bounded known-answer investigations with process-isolated role dispatch.

For each case record:
- case ID/problem;
- dispatch manifests;
- role prompt hashes;
- staged-input manifests;
- model/effort;
- Codex binary/version;
- plugins-disabled evidence;
- role artifacts;
- integration commits;
- review/critique outputs;
- oracle/reference evaluation;
- Jarvis import/provenance telemetry;
- pass/fail.

Scientific acceptance still requires PhysicsIntern's methodology plus independent oracle/reference validation.

## 14. Evaluate methodology separately from host transport

In the final Phase F report, distinguish:

### PhysicsIntern methodology
Did fresh-context survey/plan/derive/compute/review/critique/integration improve correctness and catch errors?

### Native Codex host
Did built-in `spawn_agent` work reliably?

### Process-isolated Codex transport
Did separate fresh `codex exec` role processes successfully preserve the methodology?

Do not conflate a Codex host bug with a methodology failure.

## 15. Jarvis design lesson

If this transport works, record this architectural lesson:

> Fresh-context scientific independence should be an execution contract, not coupled to one provider's native subagent primitive.

Jarvis's future scientific orchestrator should be able to support transports such as:

```text
native_subagent
process_isolated_model_session
external_agent_runtime
```

while keeping the same role/evidence/review contracts.

Do not productionize this abstraction unless the roadmap milestone calls for it; first use Phase F evidence.

## 16. Stop conditions

Proceed autonomously.

Only stop if:
- the recovered Codex runtime cannot execute separate fresh `codex exec` processes;
- plugins/Honey cannot remain disabled;
- capsule isolation cannot prevent oracle/forbidden-context leakage;
- role processes cannot produce required artifacts;
- provider/network authentication fails;
- continuing requires destructive or user-global modifications.

Do not stop solely because native `spawn_agent` is unavailable.

Start by implementing and validating the Phase-F-only process-isolated dispatcher, then resume F02.
