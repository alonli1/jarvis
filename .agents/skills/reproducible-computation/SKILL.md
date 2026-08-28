---
name: reproducible-computation
description: Prepare, execute, and verify reproducible QFT, GR, or quantum-gravity calculations with Python or Wolfram tools. Use when a research result depends on symbolic or numerical computation.
---

# Reproducible computation

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
