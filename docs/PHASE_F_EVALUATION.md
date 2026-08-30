# Phase F evaluation — PhysicsIntern calibration cases

## Scope and method

Phase F is a methodology calibration, not a novelty evaluation. F01--F05 ran
in disposable PhysicsIntern workspaces using the recovered Codex runtime with
`--disable plugins`. Substantive roles used fresh contexts, and prompts excluded
private expected answers, evaluator verdicts, and oracle material. Deterministic
oracles ran only after workspace finalization.

## Results

| Case | Target | Post-hoc oracle result | Provisional run |
| --- | --- | --- | --- |
| F01 | Free-scalar KG sign | Correct EOM; wrong sign rejected | `20260829T154526Z-literature-phase-f-f01-evidence-context-for-a-f` |
| F02 | EFT dimensions | `[phi]=1`, `[C6]=-2`; false coefficient rejected | `20260830T035710Z-literature-phase-f-f02-eft-power-counting-calib` |
| F03 | FLRW curvature | `R=6(dot H+2H^2)`; opposite sign rejected | `20260830T035720Z-literature-phase-f-f03-flrw-curvature-calibrati` |
| F04 | Schwarzschild entropy | `A=16 pi G^2 M^2`, `S=4 pi G M^2`; false denominator rejected | `20260830T172605Z-literature-phase-f-f04-schwarzschild-entropy-ca` |
| F05 | Gaussian moments | `sigma^2`, `3 sigma^4`, connected fourth `0`; missing pairing rejected | `20260830T172819Z-literature-phase-f-f05-zero-dimensional-gaussia` |

Each import contains selected answer, derivation, computation, review, critique,
execution/validation artifacts, and role-tagged telemetry. The runtime did not
report per-role model IDs, so telemetry truthfully records
`not-reported-by-runtime`; raw session transcripts were not imported.

## Methodology findings

- Fresh roles exposed material execution/provenance issues in F04 and F05;
  repairs received new independent reviews.
- F04's first-law route is conditional on the supplied Hawking temperature and
  does not independently establish the entropy coefficient or constant.
- F05's critique caught an initial symbolic MGF assumption; the repaired C-001
  directly integrates the normalized density and was reviewed again.
- The cases demonstrate workflow and provenance behavior only. They do not
  demonstrate novelty, open-problem research quality, or human acceptance.

## Acceptance decision

Phase F is complete for the five specified calibration cases. Its artifacts are
provisional research material with deterministic post-hoc checks, not a
substitute for researcher review in future science.
