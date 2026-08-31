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

The `wolframscript` launcher exited with status 255, but the direct
`/usr/local/bin/WolframKernel` runtime was recovered and explicitly executed
through a Jarvis workbench on 2026-08-31. xAct, FeynCalc, and Matchete now pass
package-context smoke checks. The FIRE7 7.1 installation was completed from
the official upstream source revision `d132e5365dd2a13db9cd9dbaf5c200b53d489cfd`:
only the absent `mm/` modules were added, without replacing the local launcher,
binaries, or Wolfram configuration. `20260831T183504Z-computation-fire7-package-load-smoke`
records successful marker loading and explicit execution. This package-load
smoke is not an IBP reduction benchmark; package-specific scientific workflows
remain distinct from these Python calibrations and must retain their own checks.
