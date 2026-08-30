# Phase G milestone G2 — registered-tool calibration benchmarks

## Objective

Exercise the Phase G capability-selected computation workbench with one bounded
QFT and one bounded GR known-answer benchmark, using the currently available
registered Python/SymPy tool and explicit independent checks.

## Scope and non-goals

- The QFT target is the normalized zero-dimensional Gaussian fourth moment.
- The GR target is the flat-FLRW Ricci scalar for exponential scale factor.
- These are calibration checks, not new results, literature review, novelty
  claims, or substitutes for package-specific xAct/FeynCalc/Matchete/FIRE
  workflows.
- The registered Wolfram packages remain execution-gated while
  `wolframscript -code 'Print[2+2]'` exits 255 without output.

## Scientific contract

- Conventions, assumptions, exact code, command, raw output, and exit status
  belong in a Jarvis computation workbench.
- The QFT script compares direct symbolic Gaussian integration to an
  independently evaluated numerical integral and rejects the unpaired fourth
  moment.
- The GR script compares the Hubble-form expression to a direct
  Christoffel/Ricci contraction under its declared mostly-plus and Riemann-sign
  conventions, then rejects the opposite scalar-curvature sign.
- The benchmark targets are the bounded known-answer cases in
  `docs/PHASE_F_CASES.md` (F05 and F03). They are not source replacements;
  future research must cite its own primary evidence with page/section.

## Interfaces and acceptance

- `jarvis run computation --capability CAPABILITY` selects only available
  registry matches, writes selected metadata to the run manifest, and adds
  relevant check instructions to `checks.md`.
- The two tracked benchmark scripts emit one JSON result each so output is
  directly machine-readable without a fragile custom parser.
- Tests execute both scripts and verify capability selection, provenance
  fields, independent-check outcomes, and rejection of seeded errors.
- Existing computation behaviour remains compatible when no capability is
  requested.

## Review limitation

No architecture or critical-review subagent is used because this coordinator
session has Honey plugin instructions. The benchmark scope is deliberately
limited to accepted, transparent calibration cases and receives deterministic
symbolic/numerical checks instead.
