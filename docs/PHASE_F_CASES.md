# Phase F known-answer calibration cases

This is the Jarvis-side evaluation contract for the PhysicsIntern calibration.
It is not copied into a PhysicsIntern problem workspace.  The independent
expected-value checks below are deliberately withheld from research prompts.

| ID | Area | Bounded investigation | Known-answer basis and pass criterion | Seeded check |
| --- | --- | --- | --- | --- |
| F01 | QFT | Free real scalar in flat mostly-plus spacetime | Direct Euler--Lagrange variation and private symbolic oracle: `(Box - m^2) phi = 0`, `k^2 = -m^2`, and `omega^2 = |k|^2 + m^2`. | Opposite massive mass sign has nonzero residual. |
| F02 | EFT | Four-dimensional scalar operator power counting | Canonical dimensions from a dimensionless action: `[phi] = 1`, `[phi^6] = 6`, and the coefficient of `phi^6` has dimension `-2`.  Basis: `knowledge/papers/manohar-eft-lectures__1804.05863.pdf`, power-counting sections, plus exact dimensional algebra. | A dimensionless `phi^6` coefficient in four dimensions fails dimensional balance. |
| F03 | GR | Spatially flat FLRW curvature | With `ds^2 = -dt^2 + a(t)^2 d x^2`, `R = 6(dot(H) + 2 H^2)`; for `a = exp(H t)` with constant positive `H`, `R = 12 H^2`.  Basis: `knowledge/books/kiefer-qg-book.pdf`, Einstein--Hilbert conventions, plus a deterministic curvature check. | The opposite-sign de Sitter scalar curvature fails the declared convention/oracle. |
| F04 | Quantum gravity | Schwarzschild Bekenstein--Hawking entropy | In `c = hbar = k_B = 1`, `r_s = 2 G M`, `A = 16 pi G^2 M^2`, and `S = A/(4G) = 4 pi G M^2`.  Basis: `knowledge/books/kiefer-qg-book.pdf`, black-hole thermodynamics discussion, plus exact algebra. | Replacing `4G` by `2G` fails the independent normalization check. |
| F05 | QFT | Zero-dimensional Gaussian field moments | For a normalized Gaussian with variance `sigma^2`, `<phi^2> = sigma^2`, `<phi^4> = 3 sigma^4`, and the connected fourth moment vanishes.  Basis: free-field Gaussian/Wick structure in `knowledge/books/birrell-davies-book.pdf`, plus direct Gaussian integration/moment algebra. | The false unpaired fourth moment `<phi^4> = sigma^4` fails the moment identity. |

## Evaluation rules

- Each case gets its own disposable PhysicsIntern workspace and its own private
  deterministic oracle.  No expected answer is placed in `problem.md`, a
  dispatch brief, or a role prompt.
- A case is importable only after the plugin-disabled PhysicsIntern workflow has
  an answer, reviewed derivation/computation evidence, a critique, executable
  artifacts, and a passing Jarvis-side oracle.
- Imported artifacts remain `provisional`; no automated result becomes human
  verified.  Runtime logs are summarized as telemetry and are not copied when
  they can contain unneeded session text.
