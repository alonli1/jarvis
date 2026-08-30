# Phase G registered-tool benchmarks

These are bounded tool calibrations, not novelty, publication, or human-review
claims. The known-answer targets and their literature-basis references are
recorded in [PHASE_F_CASES.md](PHASE_F_CASES.md), F05 and F03 respectively.

| Domain | Registered tool | Independent checks | Reproducible run |
| --- | --- | --- | --- |
| QFT: zero-dimensional Gaussian moments | Python/SymPy | Direct normalized-density symbolic integral; high-precision numerical integral at `sigma = 2`; unpaired fourth moment rejected | `20260830T174458Z-computation-phase-g-qft-zero-dimensional-gaussia` |
| GR: spatially flat FLRW curvature | Python/SymPy | Direct Christoffel/Ricci contraction; Hubble-form expression; opposite-sign curvature rejected | `20260830T174500Z-computation-phase-g-gr-flat-flrw-curvature-bench` |

Both workbenches selected the `symbolic_algebra` capability from registry v2,
ran explicitly through `jarvis compute execute`, and retained their exact
scripts, conventions, checks, stdout/stderr logs, runtime package diagnostics,
and exit status under `.jarvis/runs/`. The tracked scripts in `benchmarks/`
emit JSON, so their output requires no fragile package-specific parser.

The installed WolframScript runtime exited with status 255 and no output during
its `Print[2+2]` smoke test. xAct, FeynCalc, Matchete, and FIRE7 therefore
remain intentionally unavailable to capability selection despite their
installed package markers. Their execution workflows are not claimed tested by
these Python calibrations.
