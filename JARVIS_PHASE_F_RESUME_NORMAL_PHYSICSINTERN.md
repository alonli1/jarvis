# JARVIS Phase F — Resume PhysicsIntern Evaluation Without Adversarial Filesystem Isolation

Continue Phase F from the current repository state and from commit:

```text
9f8e12b
```

Important correction to the Phase F evaluation design:

We no longer require adversarial filesystem isolation between PhysicsIntern roles.

The purpose of Phase F is to evaluate whether PhysicsIntern's scientific methodology is useful for Jarvis, not to prove that a research agent is technically incapable of searching the host filesystem for benchmark answers.

Therefore distinguish:

- **fresh-context scientific independence — REQUIRED**
- **controlled information flow / no oracle in prompts — REQUIRED**
- **OS-level filesystem confidentiality between roles — NOT REQUIRED for Phase F**

Do not continue the Landlock/container/isolated-worker work unless it becomes necessary for another reason.

---

## 1. Preserve Current Results

- F01 remains valid and must not be redone.
- F01 passed independent oracle validation and its sanitized provisional import remains valid.
- F02-F05 remain unaccepted and should now be resumed.
- Preserve all useful provenance and lessons already recorded from the failed isolation experiments.
- Do not revert or delete the blocker documentation; treat it as an architectural finding rather than a Phase F blocker.

---

## 2. PhysicsIntern Execution Model

Run PhysicsIntern according to its intended scientific methodology.

Required properties:

1. Every substantive role invocation gets a fresh model context/session.
2. A reviewer must not inherit the Deriver/Computer's hidden conversation history.
3. Reviewers must not be given sibling reviews unless PhysicsIntern's protocol explicitly permits a summarized form.
4. Critics/reviewers receive only the explicit scientific artifacts/context required by the PhysicsIntern protocol.
5. No role receives the private oracle, expected answer, evaluator verdict, seeded-error description, or benchmark pass/fail information.
6. Honey/plugins remain disabled for PhysicsIntern scientific agents using the already-working plugin-isolation mechanism.
7. The main coordinator retains ownership of research state, integration, flags, and provenance.
8. No single subagent verdict is sufficient for scientific acceptance; follow PhysicsIntern's normal review/evidence discipline.

Fresh independent `codex exec` processes are acceptable if native `spawn_agent` is unavailable, provided each role receives a new context and no previous hidden conversation is resumed.

Filesystem access to the shared PhysicsIntern research workspace is acceptable for Phase F. Do not treat the mere ability to traverse the workspace as benchmark contamination.

---

## 3. Oracle / Known-Answer Evaluation

The private oracle is an evaluation mechanism, not part of the PhysicsIntern research plane.

For F02-F05:

1. Define each known-answer problem and its validation criterion outside the research prompt.
2. Do not include the expected result or private oracle output in:
   - `problem.md`
   - role prompts
   - survey material
   - derivation briefs
   - reviewer prompts
   - critic prompts
   - PhysicsIntern research logs visible to research roles
3. Let PhysicsIntern complete the scientific investigation normally.
4. Only after the PhysicsIntern result for that case is finalized should the external Phase F evaluator compare it against the private oracle/reference answer.
5. Record the oracle comparison separately from the research artifacts.
6. Never feed an oracle verdict back into the same case and then count the corrected result as an independent success.

The relevant guarantee is:

```text
research agents are not GIVEN the answer
```

rather than:

```text
research agents are physically incapable of locating any hidden host file
```

Do not deliberately tell agents where oracle/reference files live or ask them to search for benchmark answers.

---

## 4. Resume Phase F

Resume from the preserved F02 state.

Do not redo F01.

Complete F02, F03, F04, and F05 using:

```text
fresh PhysicsIntern role contexts
+ normal PhysicsIntern information-flow discipline
+ Honey/plugins disabled
+ private oracle withheld from research inputs
+ post-hoc independent oracle/reference evaluation
+ Jarvis provenance/telemetry import
```

For every case record:

- case ID and problem
- known-answer/reference basis kept evaluator-side
- PhysicsIntern version/commit
- Codex runtime/version
- models and reasoning effort
- plugins-disabled evidence
- roles dispatched
- fresh-context evidence
- scientific artifacts
- reviewer/critic findings
- final PhysicsIntern result
- post-hoc oracle/reference comparison
- pass/fail
- token/runtime telemetry where available
- sanitized artifacts imported into Jarvis

---

## 5. Phase F Evaluation Question

The primary Phase F question is:

> Does PhysicsIntern's methodology improve the reliability and usefulness of Jarvis scientific research?

Evaluate:

- whether fresh-context reviewers catch real mistakes
- whether independent derivation/computation paths help
- whether Surveyor/Planner/Deriver/Computer/Reviewer/Critic roles add value
- which roles are worth their model/token cost
- where the methodology overcomplicates simple problems
- which protocol elements Jarvis should implement natively
- which should remain optional PhysicsIntern behavior

Do not fail PhysicsIntern merely because its normal threat model does not provide adversarial filesystem confidentiality.

---

## 6. Record the Isolation Work as a Separate Architectural Lesson

Keep the previous isolation experiments as useful Jarvis design evidence.

Record separately that:

```text
fresh_context != filesystem_isolation
```

and that stronger blinded-review workflows may eventually require:

- isolated workers
- containers/VMs
- dedicated model state
- explicit filesystem read isolation

Those are future/high-assurance Jarvis transport capabilities, not Phase F exit criteria.

---

## 7. Completion

Proceed autonomously through F02-F05.

Do not ask for routine approval or restart completed work.

Only stop for a genuine blocker that prevents the normal PhysicsIntern methodology itself from running, such as:

- model/provider failure
- inability to start fresh role contexts
- Honey cannot be kept out of scientific-agent contexts
- required scientific tools cannot execute
- artifacts cannot be produced or validated

Filesystem access to the shared research workspace by itself is no longer a blocker.

After F05:

1. complete the Phase F evaluation report;
2. update Jarvis's durable progress/roadmap state;
3. preserve the previous isolation findings as architectural evidence;
4. proceed according to the existing roadmap.
