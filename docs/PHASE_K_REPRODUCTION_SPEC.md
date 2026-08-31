# Phase K milestone K1 — reproducible paper implementation contract

`PaperSpecification` records a corpus source path plus exact locator, target,
equations, conventions, and assumptions. `ImplementationSpecification` adds
engine, scripts, and required scientific checks. Reports render those fields
without interpreting unread source material or claiming reproduction success.

This is the safe foundation for paper benchmark runs. The Phase K acceptance
gate—three published results or algorithms in different categories—remains
open until source-grounded, explicitly executed workbenches are selected and
reviewed.

## K2 acceptance evidence

The gate was closed on 2026-08-31 with three bounded, source-grounded symbolic
reproductions recorded in `benchmarks/phase_k_reproductions/`:

- EFT power counting from Manohar, PDF pp. 22--24, eqs. (4.2)--(4.14);
- conformal scalar coupling from Birrell--Davies, PDF p. 54 (printed p. 44),
  eqs. (3.26)--(3.27); and
- Schwarzschild Bekenstein--Hawking entropy from Kiefer, PDF p. 232 (printed
  p. 219), eqs. (7.23)--(7.24).

Each has a validated `ImplementationSpecification`, a source/page/equation map,
a tracked SymPy script, an explicit computation run, and recorded independent
checks. These reproduce only the listed source statements; they do not establish
full-paper reproduction, novelty, or human verification.
