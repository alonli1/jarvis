# Phase K bounded source-grounded reproductions

These are three narrow reproductions of published equations in distinct subject
categories. They are not novel calculations, full-paper reproductions, or human
verification. Each source locator was read in the corresponding literature bundle,
and each script was explicitly executed in the listed computation run.

| Category | Source and target | Explicit run |
| --- | --- | --- |
| EFT power counting | Manohar, PDF pp. 22--24, eqs. (4.2)--(4.14): `[C6] = -2` for `C6 phi^6` in `d = 4` | `20260831T191328Z-computation-phase-k-eft-phi-6-canonical-dimensio` |
| Curved-spacetime QFT | Birrell--Davies, PDF p. 54 (printed p. 44), eqs. (3.26)--(3.27): `xi(4) = 1/6` | `20260831T191354Z-computation-phase-k-conformal-scalar-coupling-re` |
| Black-hole thermodynamics | Kiefer, PDF p. 232 (printed p. 219), eqs. (7.23)--(7.24): `S_BH = 4 pi G M^2` | `20260831T191420Z-computation-phase-k-schwarzschild-bekenstein-haw` |

The `*.spec.json` files conform to `ImplementationSpecification`; the scripts emit
JSON containing their assumptions, target values, and independent checks.

The scalar induced-gravity entry is
sakharov_scalar_msbar_low_order.py. Its source locator is Vassilevich,
electronic PDF p. 40, eqs. (4.26)--(4.28); its explicit run is
20260901T113846Z-computation-independently-verify-the-one-real-sc. Parallel
Markdown and LaTeX reports record the \(g=\eta+\kappa h\), \([h]=1\),
\([\kappa]=-1\) normalization. It is a low-order reproduction, not an
expanded \(B_6\) or \(B_8\) coefficient table.

`sakharov_scalar_msbar_dim6.wls` is the exact symbolic successor through
\(B_6\). It specializes the full general \(a_6\) table using Wolfram rational
algebra and independently checks the result against an analytic
Euler--Maclaurin expansion of the scalar spectrum on \(S^4\). Its Markdown,
LaTeX, and JSON specification artifacts make the unresolved \(B_8\) source
and toolchain limitation explicit; it does not present a dimension-six result
as a completed dimension-nine truncation.
