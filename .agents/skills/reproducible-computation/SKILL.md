---
name: reproducible-computation
description: Prepare, execute, and verify reproducible QFT, GR, or quantum-gravity calculations with Python or Wolfram tools. Use when a research result depends on symbolic or numerical computation.
---

# Reproducible computation

First establish the research intent: literature, computation, or both. A
computation workbench already selects computation; otherwise, if the user has
not made the intended mode clear, ask once rather than presenting a
literature-derived formula as an independent result. For both, create and
read a literature evidence bundle before accepting source formulas as inputs.

Default to exact symbolic output for coefficients, bases, amplitudes, and
derivations. Numerical work requires the user's explicit request. Use a
registered symbolic package when applicable: SymPy for Python algebra,
Wolfram Language for general symbolic work, xAct for tensor/curvature
algebra, FeynCalc for perturbative QFT, Matchete for EFT matching, and FIRE
for IBP reduction.

If the requested symbolic calculation is blocked, identify the precise absent
capability, unavailable package, or mathematical limitation and ask the user
how to proceed. Do not silently provide a numerical approximation or a
literature transcription as a symbolic derivation.

Create a workbench with `jarvis run computation --task "..." --engine auto|wolfram|python`.
Write scripts only inside that run's `scripts/` directory and execute them explicitly with
`jarvis compute execute RUN_ID SCRIPT`.

Before accepting a result:

- state metric, curvature, Fourier-transform, normalization, unit, and regulator conventions;
- record assumptions and the physical regime;
- use registered packages when applicable and retain exact scripts, commands, versions, raw
  output, and exit status;
- check dimensions, symmetries, known limits, signs, and simple special cases;
- make an independent symbolic, numerical, or analytic cross-check when practical;
- cite the literature inputs that justify formulas or approximations.

Generated code has the user's permissions and is not sandboxed. Inspect it before explicit
execution. A successful process exit is not scientific validation.
After checking the run, summarize the result, conventions, failures, and independent checks in
`result.md`; keep detailed output in `logs/` or `outputs/`.
