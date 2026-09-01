# One real scalar: low-order induced-gravity EFT

## Scope

This is a reproducible normalization report for one real scalar on a smooth,
compact, boundaryless Euclidean background. It verifies the local threshold
through curvature-squared order; it does not claim an expanded \(B_6\) or
\(B_8\) basis.

The source is Vassilevich,
knowledge/papers/vassilevich-heat-kernel-2003__hep-th_0306138.pdf,
electronic PDF p. 40, eqs. (4.26)--(4.28).

## Conventions

\[
S_E=\frac12\int d^4x\sqrt g\,\phi D_E\phi,\qquad
D_E=-\nabla^2+m^2+\xi R.
\]

There is one real scalar, \(m>0\), \(d=4-2\epsilon\), and
\(\overline{\mathrm{MS}}\) subtraction. In Vassilevich's convention,
\(L=-(\nabla^2+E)\), so \(E=-\xi R\) and \(\Omega_{\mu\nu}=0\).

For the mostly-minus Lorentzian convention,
\[
g_{\mu\nu}=\eta_{\mu\nu}+\kappa h_{\mu\nu},\qquad
[h_{\mu\nu}]=1,\qquad[\kappa]=-1.
\]
Thus \([\kappa h]=0\), \(R\sim\kappa\partial^2h+\cdots\) has dimension two,
and \(B_6/m^2\) and \(B_8/m^4\) both have Lagrangian dimension four.

## Result

With \(L_m=\ln(m^2/\mu^2)\),
\[
\Gamma_{E,\overline{\mathrm{MS}}}^{(1)}
=\int d^4x\sqrt g\left[
\frac{m^4}{64\pi^2}(L_m-\tfrac32)
+\frac{m^2}{32\pi^2}(\xi-\tfrac16)(L_m-1)R
+\frac{L_m}{32\pi^2}B_4
+O(\mathcal R^3/m^2)\right],
\]
\[
B_2=(\tfrac16-\xi)R,
\]
\[
B_4=\frac12(\xi-\tfrac16)^2R^2
+\frac1{180}(R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
-R_{\mu\nu}R^{\mu\nu})
+\left(\frac1{30}-\frac{\xi}{6}\right)\Box R.
\]

At \(\xi=1/6\), \(B_2\) and the \(R^2\) coefficient in \(B_4\) vanish.
Finite local gravitational counterterms remain freely adjustable, so these are
scalar-determinant threshold contributions, not absolute gravitational
couplings.

For a parity-even scalar determinant on a boundaryless background, the local
metric expansion has canonical curvature dimensions \(0,2,4,6,8,\ldots\);
there is no dimension-nine term. The next terms have prefactors
\(-B_6/(32\pi^2m^2)\) and \(-B_8/(32\pi^2m^4)\), but their expanded operator
tables require a separately declared dimension-six/eight invariant basis.

## Reproduction

Run python3 benchmarks/phase_k_reproductions/sakharov_scalar_msbar_low_order.py.

The script is standard-library only. It checks exact rational coefficients,
the conformal limit, and the \(g=\eta+\kappa h\) dimensional normalization.
The run-bundle copy, raw output, conventions, and explicit execution record
are under .jarvis/runs/20260901T113846Z-computation-independently-verify-the-one-real-sc/.
