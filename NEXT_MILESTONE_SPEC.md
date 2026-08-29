# Milestone spec — Phase E science-aware router v1

## Objective

Add a deterministic, explainable `jarvis route --dry-run` that selects only configured model profiles using request features and explicit epistemic floors. It must not execute models, spawn agents, or alter `jarvis ask` defaults.

## Boundaries

- Input: request text, requested role, optional profile override.
- Output: provider-neutral `TaskFeatures` and `RouteDecision`, selected configured profile, reason codes, and an explanation.
- Deterministic role priors and explicit floor/escalation rules only. No classifier call in this milestone.
- Reuse Phase B eval infrastructure for router fixtures; do not treat evidence/tool cases as physics-answer grading.

## Deterministic policy

`TaskFeatures` contains the roadmap's eleven `0..3` dimensions: novelty, ambiguity, mathematical_depth, convention_sensitivity, tool_dependence, verification_strength, literature_uncertainty, coupling, consequence, context_burden, and creative_search. Profile capability tiers are ordered: `extract`, `science_fast`, `science_standard`, `science_deep`, `science_critical`.

Role priors are `metadata`/`triage` → extract; `retrieval`/`computation` → science_fast; `literature`/`derivation` → science_standard; `research_planning`/`review` → science_deep; `critical_review` → science_critical. Unknown roles fail clearly.

Raise the role floor to science_deep for novelty, convention sensitivity, literature uncertainty, coupling, or creative search at `>=2`; for mathematical depth or ambiguity at `>=3`; and for high consequence (`>=2`) when verification strength is `<=1`. Do not select science_critical automatically: only the critical-review role may require it. `verification_strength` follows the roadmap's stated meaning—availability of deterministic verification—so low, not high, strength is an escalation signal.

Configuration adds a required `capability` to each model profile. The router selects the lowest configured profile meeting the computed floor. If none exists, dry-run fails safely and names the unmet tier; it must not relabel a lower-capability profile.

`jarvis route --dry-run QUESTION --role ROLE` accepts every feature as an optional bounded integer and emits sorted JSON with selected profile/model, features, floor, reason codes, and explanation. An explicit `--profile` is allowed only if its configured capability satisfies the computed floor.

## Invariants/tests

- Profile override is validated and explained.
- High convention sensitivity, novelty, verification strength, or consequence cannot select below the defined floor.
- Unknown role/profile fails clearly; no provider request is made.
- Dry-run JSON is machine-readable, existing commands remain compatible, and Phase B/C/D tests remain green.

## Review limitation

Honey isolation remains unavailable. The coordinator must make the minimum routing-policy decision, record thresholds and adverse cases, and perform a parent-level adversarial review; do not spawn architecture or critical-review agents.
