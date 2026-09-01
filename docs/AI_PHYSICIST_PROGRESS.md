# AI-physicist roadmap progress

## 2026-08-29 — Phase A baseline audit complete

- Baseline: `9aa8b6063798355970ee2c47991fe3ccbb36edd8` on `ai-physicist-roadmap`.
- Evidence: [AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md](AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md).
- Validation: dependency sync, 47 passing tests, 63% coverage, diagnostics, retrieval, live literature query, and explicit computation workbench execution.
- Known limitation: Ruff has 14 pre-existing findings; Semantic Scholar rate-limited the live query.
- Honey isolation: unavailable in this Codex environment; no architecture or critical-review subagent was used.

## Next milestone

Post-Phase-N acceptance evaluation: provider-backed native-vs-PhysicsIntern
runs, three source-grounded published reproductions, seeded/historical referee
cases, and comparable configured cross-provider scientific runs. These require
real evaluation inputs and are not claimed from local code alone.

## 2026-08-29 — Phase B evaluation-suite foundation complete

- Added 20 source/tool-evidence cases across retrieval, literature (including paper-reproduction prerequisites), QFT, GR, and computation.
- Added `jarvis eval run`, which produces a machine-readable report without a model call and treats case failures as report data.
- Validation: focused evaluation/CLI tests, full suite (`50 passed`), new-code Ruff check, and a real local report (`20 passed`, `0 failed`).
- Scope: this is evidence/tool availability evaluation only; it does not validate scientific answers, derivations, or claims.

## 2026-08-29 — Phase C Manifest v2 scientific result types complete

- Added provider-neutral typed evidence, claim, verification, model-usage, task, decision, and flag records.
- New runs write Manifest v2 defaults; `load_manifest()` provides a non-mutating v2-shaped view of v1 manifests.
- `human_verified` claim status requires `human_reviewed=True`; this guards data consistency but is not human-actor authorization.
- Validation: manifest/workflow tests and full suite (`54 passed`).

## 2026-08-29 — Phase D profiles and telemetry complete

- Added optional configured model profiles, structured completion telemetry, and `jarvis ask --profile`.
- Preserved the existing default model and text-only completion API; no routing or retrieval behavior changed.
- Validation: focused configuration/runtime/CLI tests and full suite (`61 passed`).

## 2026-08-29 — Phase E science-aware router v1 complete

- Added deterministic `jarvis route --dry-run` with explicit role priors, eleven bounded risk features, configurable capability tiers, reasons, and safe unavailable-profile failures.
- The router makes no provider request and cannot silently route below its computed epistemic floor.
- Validation: focused router tests, CLI smoke test, and full suite (`67 passed`).

## 2026-08-29 — Phase F preparation complete

- Added provider-neutral provisional-artifact import into Manifest v2 runs:
  contained copy, stable SHA-256 digest, source/role metadata, duplicate and
  traversal rejection, and ZIP/Markdown handoff support.
- Added optional role-tagged `ModelUsage` and run-persisted usage records.
- Validation: focused manifest/workflow tests (`9 passed`), full suite (`70
  passed`), and changed-file Ruff/format checks. Repository-wide Ruff still has
  15 pre-existing findings outside this milestone.
- Scope: no PhysicsIntern workspace, scientific agent, scientific claim, or
  known-answer investigation was run.

## 2026-08-29 — Phase F bootstrap and isolation verified; execution blocked

- Bootstrap: official upstream script with `host=codex`, PhysicsIntern commit
  `41d75f998710948e90b9254fba1cc501fe09fc84`, disposable workspace under
  `/tmp/jarvis-physicsintern-phase-f`.
- Isolation: `codex --disable plugins` sets `plugins=false`; an isolated runtime
  audit found no Honey and found all eight local PhysicsIntern skills plus seven
  local roles.
- Pilot: the free-scalar survey was produced and a separate symbolic oracle
  rejected a seeded wrong sign, but the autonomous workflow could not continue.
- Blocker: every isolated `codex exec` fails on a malformed model catalog
  (`base_instructions` absent for eight models); see `BLOCKER.md`. No five-case
  evaluation, imported run, scientific claim, or Phase F acceptance decision was
  made.

## Current blocker

No active Phase F blocker remains. Under the approved normal PhysicsIntern
information-flow policy, shared-workspace filesystem visibility was not an
execution blocker; private expected-answer/oracle material remained withheld
until post-hoc validation.

## 2026-08-29 — Phase F runtime recovery and F01 complete

- Recovery: reused Antigravity's installed OpenAI Codex extension runtime
  `0.151.0-alpha.7.1` at its recorded absolute path.  It passed a
  plugin-disabled model smoke test without the old `base_instructions` failure.
- Isolation: the recovered process reported `plugins=false`; its audit found no
  Honey directive/skill and found all eight PhysicsIntern skills and seven
  PhysicsIntern roles.  No global cache, authentication, or plugin setting was
  changed.
- F01 (free scalar, QFT): PhysicsIntern's completed, reviewed derivation and
  finite-difference calculation agree with an independent deterministic oracle;
  the seeded opposite mass sign is rejected.  The disposable workspace revision
  is `baa91ee`.
- Provenance: selected F01 artifacts were imported as provisional material into
  `20260829T154526Z-literature-phase-f-f01-evidence-context-for-a-f`.  Raw
  session logs were not imported.  The runtime did not report a per-role model
  identifier, so telemetry records `not-reported-by-runtime` rather than
  inventing a model name.
- Case contract: [PHASE_F_CASES.md](PHASE_F_CASES.md) defines F01--F05, their
  literature/deterministic bases, and withheld seeded checks.

## 2026-08-29 — Phase F F02 dispatch capability blocked

- A fresh F02 EFT workspace was successfully bootstrapped and populated with
  only its bounded question and evidence pointer.
- The recovered plugin-disabled `codex exec` process reaches the model, but its
  PhysicsIntern coordinator exposes no usable fresh-context `spawn_agent`:
  the trace shows a `wait` collaboration call with no receiver at the required
  survey dispatch point.  No F02 scientific artifact was accepted or imported.
- This is a distinct external runtime-host limitation, not the repaired model
  catalog issue.  The F02 workspace is preserved pending a plugin-disabled
  invocation mode with generated-role dispatch support; see `BLOCKER.md`.

## 2026-08-29 — Process-isolated dispatch capsule blocked

- A Phase-F-only adapter under `/tmp` created fresh, plugin-disabled recovered
  Codex sessions, role/prompt hashes, staged-input manifests, stdout/stderr
  provenance, and output-contract validation.  Two non-scientific role smoke
  artifacts passed those local checks.
- The planner smoke trace could still see the parent F02 workspace through
  `../../../`, so the capsule cannot protect hidden oracles and forbidden
  reviews.  `bubblewrap` is present but non-privileged user namespaces are
  disabled by the kernel, preventing the required filesystem boundary.
- F02--F05 remain unaccepted.  This is an external OS-isolation blocker, not a
  PhysicsIntern methodology result; see `BLOCKER.md`.

## 2026-08-29 — Strict Landlock recovery stopped at Codex state dependency

- Landlock ABI 8 directly proved a fail-closed read allowlist and denied the
  F02 parent path in a launcher test.
- The recovered Codex executable then failed before a model turn because its
  app-server client needs denied global Codex IPC/state. Granting it would break
  the required dedicated-state confidentiality boundary.
- F02--F05 cannot run locally under the contract; see `BLOCKER.md`.

## 2026-08-30 — Phase F normal PhysicsIntern execution resumed

- The recovered plugin-disabled runtime was used with separate fresh role
  contexts and normal PhysicsIntern artefact flow; Honey remained disabled.
- F02 (EFT power counting) and F03 (FLRW curvature) completed in disposable
  workspaces and were post-hoc checked against private deterministic oracles.
  Selected artifacts, execution outputs, reviews, critiques, validation records,
  and truthful `not-reported-by-runtime` role telemetry were imported into
  provisional runs `20260830T035710Z-literature-phase-f-f02-eft-power-counting-calib`
  and `20260830T035720Z-literature-phase-f-f03-flrw-curvature-calibrati`.
- F04 (Schwarzschild entropy) has completed separate derivation and computation
  routes. The first computation review caught a real pre-repair execution defect;
  a fresh R2 review confirmed the repaired, explicitly dependency-pinned run.
  Critique, finalization, oracle validation, import, and F05 remain pending.
- Earlier capsule/Bubblewrap/Landlock findings are retained as architectural
  evidence, not as blockers under this approved normal-information-flow policy.

## 2026-08-30 — Phase F complete

- F04 and F05 completed with fresh-role derivations, computations, reviews,
  critiques, answer artifacts, and post-hoc private-oracle checks.
- F05's critique caught an initial symbolic MGF assumption; C-001 was repaired
  to integrate the normalized density directly and received a new review.
- All five cases have selected provisional imports and truthful role telemetry.
  See [PHASE_F_EVALUATION.md](PHASE_F_EVALUATION.md) for the case table and
  scope-limited acceptance decision.

## 2026-08-30 — Phase G capability registry (G1) complete

- Evolved `packages/registry.yaml` to version 2 with declared capabilities,
  domains, execution environments, verification strength, and check templates
  for the existing Wolfram/xAct/FeynCalc/Matchete/FIRE7/Python surface.
- Added a validated, v1-compatible registry loader and deterministic selector
  that returns only runtime-available tools for requested capabilities; it
  never silently substitutes an unrelated tool.
- Initial runtime evidence recorded the broken `wolframscript` launcher; see
  the 2026-08-31 recovery entry below for the current direct-kernel state.
- Validation: focused registry/workflow/evaluation/CLI tests and full suite
  (`75 passed`), plus live capability selection and `jarvis doctor`.
- Specification: [PHASE_G_CAPABILITY_REGISTRY_SPEC.md](PHASE_G_CAPABILITY_REGISTRY_SPEC.md).

## 2026-08-30 — Phase G capability workflows and benchmarks (G2) complete

- `jarvis run computation --capability CAPABILITY` now selects only available
  registered tools, persists requested/selected metadata, and renders each
  selected tool's declared scientific checks into the workbench.
- Wolfram capability workbenches load each selected package with an explicit
  `Needs[...]` directive. Unit coverage verifies the generic registered-package
  path is capability-driven; current runtime diagnostics still prevent actual
  execution rather than hiding that limitation.
- Reproducible QFT and GR calibration workbenches passed explicit execution:
  zero-dimensional Gaussian moments used direct symbolic plus independent
  high-precision numerical integration, and flat-FLRW curvature used direct
  Christoffel/Ricci plus Hubble-form checks. Both reject seeded mistakes.
- Evidence and scope: [PHASE_G_BENCHMARKS.md](PHASE_G_BENCHMARKS.md) and
  [PHASE_G_BENCHMARKS_SPEC.md](PHASE_G_BENCHMARKS_SPEC.md).
- Validation: focused capability/benchmark/CLI tests and full suite (`81
  passed`), plus explicitly executed run bundles with raw logs.

## 2026-08-30 — Phase H deterministic plan foundation (H1) complete

- Added provider-neutral `ResearchPlan` and `TaskPacket` records while keeping
  existing `ResearchTask` fields compatible.
- Plans reject duplicate/unknown/self dependencies, cycles, and leaf-task budget
  overruns before any run mutation. Plan persistence writes deterministic
  `plan.json` digests into Manifest v2 runs; packet generation emits only
  dependency-free leaves and makes no model call.
- Task-packet validation rejects absolute or parent-traversal artifact paths.
- Validation: focused planner/manifest/workflow/router tests and full suite
  (`84 passed`). Specification: [PHASE_H_PLANNER_SPEC.md](PHASE_H_PLANNER_SPEC.md).

## 2026-08-30 — Phase H dependency-ready task packets (H2) complete

- Dependent tasks receive packets only after every dependency is complete and
  each declared upstream artifact exists under the same run directory.
- Completed tasks are never re-packeted; conflicting existing packets are
  rejected rather than overwritten. Packet validation also excludes reviewer
  artifact paths.
- Validation: focused planner/manifest/workflow tests and full suite (`85
  passed`).

## 2026-08-30 — Phase I claim-promotion guard (I1) complete

- Added claim-scoped verification records and a deterministic promotion policy.
  `ai_verified` requires a passed contained artifact and an independent check
  for derivation/computation claims; contradicted, missing, failing, unrelated,
  or escaping evidence cannot promote a claim.
- Successful promotion persists the claim and a policy rationale in the Manifest
  v2 decision log. The implementation does not call a model and cannot grant
  human verification.
- Validation: focused ledger/manifest tests and full suite (`87 passed`).
  Specification: [PHASE_I_CLAIM_LEDGER_SPEC.md](PHASE_I_CLAIM_LEDGER_SPEC.md).

## 2026-08-31 — Phase I contradiction and human-review actions (I2) complete

- Verification records now persist only when their artifacts are contained in
  the run. Claim-scoped contradiction records explicitly set a claim to
  `contradicted` and record the action in the decision log.
- `human_verified` is reachable only through an explicit action with a non-empty
  human reviewer identity; the action sets `human_reviewed=True` and is not an
  AI inference.
- Validation: focused ledger/manifest tests and full suite (`88 passed`).

## 2026-08-31 — Phase I research-memory index (I3) complete

- Added a read-only index over persisted Manifest v2 claims, statuses,
  conventions, and claim-scoped verification IDs. It creates no claim and does
  not mutate source manifests.
- Validation: focused memory/ledger tests and full suite (`89 passed`).

## 2026-08-31 — Phase J deterministic scheduling boundary (J1) complete

- Added a native scheduler that materializes only ready, run-contained task
  packets and marks leaf execution as requiring a fresh context. It does not
  call a model, infer scientific success, or bypass Phase H/I provenance guards.
- Validation: focused orchestration/planning tests and full suite (`90 passed`).
  Specification: [PHASE_J_ORCHESTRATOR_SPEC.md](PHASE_J_ORCHESTRATOR_SPEC.md).
- Remaining Phase J acceptance gap: no configured pair of provider-backed native
  runs has been evaluated against PhysicsIntern, so parity is not claimed. The
  sole `ollama/qwen3:14b` profile refused the 2026-08-31 local-provider health
  check. A 2026-09-01 plugin-disabled extension-runtime audit also failed before
  isolation verification because its workspace-managed cloud config could not
  load. Phase J host-neutral dispatch is recorded separately; see `BLOCKER.md`.

## 2026-08-31 — Phase K reproduction contract (K1) complete

- Added structured paper specifications with source locators, equation and
  convention maps, implementation scripts, required checks, and a reproduction
  report generator.
- Validation: focused reproduction tests and full suite (`91 passed`).
  Specification: [PHASE_K_REPRODUCTION_SPEC.md](PHASE_K_REPRODUCTION_SPEC.md).

## 2026-08-31 — Phase L structured referee records (L1) complete

- Added evidence-attributed technical findings, report limitations, and
  research-idea records with falsifiers, cheapest decisive tests, and explicit
  corpus-relative novelty scope.
- Validation: focused referee tests and full suite (`92 passed`).
  Specification: [PHASE_L_REFEREE_SPEC.md](PHASE_L_REFEREE_SPEC.md).

## 2026-08-31 — Phase M profile-compatibility calibration (M1) complete

- Added deterministic capability compatibility records across configured model
  profiles. Compatible profiles may be swapped without changing a run, corpus,
  or Manifest v2 scientific-state format.
- Validation: focused calibration tests and full suite (`93 passed`).
  Specification: [PHASE_M_CALIBRATION_SPEC.md](PHASE_M_CALIBRATION_SPEC.md).
- Remaining Phase M acceptance gap: no two configured providers have completed
  comparable scientific runs, so quality/cost calibration is not claimed.

## 2026-08-31 — Phase N bounded-autonomy admission (N1) complete

- Added a deterministic admission policy for small plans with stop conditions.
  It rejects disallowed task types and publication, submission, or manuscript
  editing actions, and admission itself never executes a plan.
- Validation: focused autonomy tests and full suite (`94 passed`).
  Specification: [PHASE_N_AUTONOMY_SPEC.md](PHASE_N_AUTONOMY_SPEC.md).

## Roadmap status through Phase N

The deterministic, provider-neutral implementation surface through Phase N is
present. The following acceptance evidence remains intentionally open rather
than claimed: native-vs-PhysicsIntern provider-backed evaluations (J) and
comparable runs on two configured providers (M). Those
require real configured model/provider access and selected scientific evaluation
material; no local code-only substitute is treated as evidence.

## 2026-08-31 — Phase G Wolfram runtime recovery (G3) complete

- Jarvis now selects a healthy `WolframKernel` runtime instead of relying on
  the failing `wolframscript` launcher; explicit Wolfram workbench execution
  completed successfully.
- xAct, FeynCalc, and Matchete pass package-context smokes and are available to
  capability selection. FIRE7 stays `broken` because its installed directory
  lacks required `mm/Reconstruction.m` and `mm/LeeRule.m` files.
- Validation: focused registry/workflow tests and full suite (`94 passed`).

## 2026-08-31 — Phase G FIRE7 package recovery (G4) complete

- Recovered the incomplete local FIRE 7.1 installation from official upstream
  source revision `d132e5365dd2a13db9cd9dbaf5c200b53d489cfd`. The repair added
  only the previously absent `mm/` modules; it did not replace the local
  launcher, binaries, or Wolfram configuration.
- Registry v2 now supports an explicit Wolfram marker loader. FIRE7 loads its
  registered `FIRE7.m` entry point rather than incorrectly assuming that
  `Needs["FIRE`"]` is available on `$Path`.
- `jarvis doctor` reports FIRE7 7.1 available, and the explicit capability-
  selected smoke workbench `20260831T183504Z-computation-fire7-package-load-smoke`
  passed. This establishes package availability only, not an IBP-reduction
  result or scientific validation.

## 2026-08-31 — Phase K source-grounded reproductions (K2) complete

- Closed the Phase K acceptance gate with three bounded, explicitly executed
  reproductions in distinct categories: scalar-EFT power counting,
  curved-spacetime conformal scalar coupling, and Schwarzschild
  Bekenstein--Hawking entropy.
- The tracked artifacts in `benchmarks/phase_k_reproductions/` retain validated
  source/page/equation maps, conventions, assumptions, scripts, and independent
  checks. Their run bundles retain literature evidence and execution logs.
- Validation: focused reproduction tests plus the full suite (`96 passed`).
  These are source-statement reproductions only, not full-paper reproductions,
  novel results, or human verification.

## 2026-08-31 — Phase L seeded referee evaluation (L2) complete

- Closed the Phase L acceptance gate with a deliberately flawed, clearly labelled
  non-manuscript fixture and a deterministic structured technical review.
- The review identifies the seeded factor-of-two entropy normalization error from
  Kiefer, PDF p. 232 (printed p. 219), eqs. (7.23)--(7.24); separately records
  absent source/conventions; and preserves limitations. Its literature evidence is
  in `20260831T192115Z-literature-technical-review-evidence-for-a-seed`.
- Validation: focused referee-evaluation tests and the full suite (`97 passed`).
  This demonstrates record integrity, not human review, publication fitness, or
  a novelty assessment.

## 2026-09-01 — Phase J host-neutral dispatch (J2) complete

- Added explicit schedule, export, and provisional-import commands for IDE and
  extension hosts, including this Codex workspace. No model API or Ollama
  service is required for that transport.
- Packet identity and plan digests are revalidated; imports require a declared
  fresh context and cannot promote claims or complete tasks. Provider/model
  telemetry is optional and never inferred.
- Validation: focused orchestration and workflow tests. Specification:
  [PHASE_J_HOST_DISPATCH_SPEC.md](PHASE_J_HOST_DISPATCH_SPEC.md).

## 2026-09-01 — Phase J extension-runtime recovery verified

- The IDE-bundled Codex runtime `0.151.0-alpha.7.1` now completes the
  plugin-disabled feature audit (`plugins=false`) and a fresh authenticated native
  `exec` smoke (`JARVIS_NATIVE_RUNTIME_OK`; 10 output tokens).
- A second fresh read-only `exec` with only `honey@greenpt` disabled by an
  invocation-scoped configuration override completed a PhysicsIntern-context
  smoke (`PHYSICSINTERN_CONTEXT_OK`; 11 output tokens). The installed PhysicsIntern
  plugin and persistent user configuration were not changed.
- This establishes live host/runtime availability, but is not a scientific result
  or a native-versus-PhysicsIntern comparison. A fresh disposable PhysicsIntern
  workspace remains necessary; the official bootstrap was safety-gated before any
  write because its Git commit could not be mechanically confined to the requested
  `/tmp` target. No historical Phase F artifact is reused.

## 2026-09-01 — Scalar induced-gravity reproducibility artifact

- Added a tracked, standard-library reproduction of the one-real-scalar
  \(B_2,B_4\) heat-kernel specialization and low-order
  \(\overline{\rm MS}\) threshold normalization, sourced to Vassilevich,
  electronic PDF p. 40, eqs. (4.26)--(4.28).
- The artifact explicitly checks the local graviton normalization
  \(g=\eta+\kappa h\), \([h]=1\), \([\kappa]=-1\), hence \([R]=2\), as well
  as the \(\xi=1/6\) limit. Parallel Markdown and compilable LaTeX reports
  preserve conventions, scope, and the distinction between threshold and
  absolute gravitational couplings.
- Validation: explicit Jarvis computation run
  20260901T202333Z-computation-reproduce-one-real-scalar-low-order-,
  focused reproduction tests, specification validation, and a successful
  LaTeX compile. This is low-order normalization evidence, not an expanded
  dimension-six or dimension-eight coefficient table.

## 2026-09-02 — Scalar induced-gravity independent-validation upgrade

- Replaced the hand-entered low-order specialization with exact rational
  substitution of the complete general \(a_2,a_4\) Laplace-type source table
  for \(E=-\xi R\), \(\Omega_{\mu\nu}=0\).
- Added two independent computational checks: numerical
  \(\overline{\rm MS}\) finite-part extraction from regulated proper-time
  Gamma integrals, and direct spectral heat-trace extraction on \(S^4\) plus
  two \(S^2\times S^2\) backgrounds. The three-background spectral system
  resolves the \(R^2\), Ricci-squared, and Riemann-squared coefficients
  independently of their local source transcription.
- The reports now distinguish what the spectral checks establish from what
  they cannot: an integrated closed-manifold trace cannot constrain the
  total-derivative \(\Box R\) term, which remains a source-specialization
  result. This is still limited to the curvature-squared milestone; it makes
  no claim about expanded \(B_6\) or \(B_8\) bases.
- Validation: fresh literature evidence bundle
  20260901T211018Z-literature-extract-the-general-scalar-laplace-t,
  explicit artifact execution, focused reproduction tests (2 passed), and
  Ruff on the changed Python and test files.

## 2026-09-02 — Research-intent gate

- Made research intent a repository-wide host contract: before a scientific
  answer, Jarvis establishes literature, computation, or both, and asks once
  only when the user's request is ambiguous.
- Added the same gate to each foundational skill, browser-handoff-visible
  workflow instructions, and the legacy provider-backed ask prompt. The
  combined mode explicitly requires the answer to distinguish literature
  statements from independently executed checks.
- Validation: prompt-routing regression test plus the relevant skill and
  workflow test suites.
