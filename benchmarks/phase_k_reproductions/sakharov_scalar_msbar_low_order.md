# One real scalar: low-order induced-gravity EFT

## Scope

This is a reproducible, two-source calculation and validation report for one
real scalar on smooth compact Euclidean backgrounds. It derives the local
threshold through curvature-squared order from a general heat-kernel formula,
then checks it using spectra that are not a transcription of the local
coefficient. It does not claim an expanded \(B_6\) or \(B_8\) basis.

The source is Vassilevich,
knowledge/papers/vassilevich-heat-kernel-2003__hep-th_0306138.pdf,
electronic PDF p. 40, eqs. (4.26)--(4.28).

The scalar spherical-harmonic input used below follows directly by restricting
harmonic homogeneous polynomials in \(\mathbb R^{n+1}\) to \(S^n\). For
reference, the \(S^4\) eigenvalue and degeneracy are also stated in
H. Casini, *Lectures on entanglement in quantum field theory*, exercise 3,
p. 42, https://inspirehep.net/files/19a199a6a26b5847549045339dba86ee.

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

## Independent computation and validation

The Python artifact does more than print these expressions.

1. It encodes Vassilevich's general \(a_2,a_4\) coefficient tables,
   including \(E,\nabla^2E,RE,E^2,\Omega^2\), and performs exact rational
   substitution \(E=-\xi R,\ \Omega=0\). The displayed scalar coefficients
   are generated output of that substitution.
2. It evaluates the regulated proper-time Gamma integrals at two nonzero
   \(\epsilon\) values, subtracts the \(\overline{\rm MS}\) pole
   \(1/\epsilon-\gamma+\ln4\pi\), and Richardson-extrapolates their finite
   parts. At \(m=2.7,\mu=1.3\), the absolute disagreements with the analytic
   \(B_0,B_2,B_4\) threshold factors are below
   \(9.0\times10^{-9},2.1\times10^{-10},3.3\times10^{-13}\), respectively.
3. It computes spectral heat traces rather than inserting \(B_2,B_4\):
   \[
   \operatorname{Tr}e^{-t(-\Delta+\xi R)}
   =\sum_{\ell\geq0}\frac{(2\ell+3)(\ell+2)(\ell+1)}6
   e^{-t[\ell(\ell+3)+12\xi]}
   \quad(S^4).
   \]
   On \(S^2(A)\times S^2(B)\), it instead uses the product of the two
   sums with eigenvalues \(A\ell(\ell+1)\) and degeneracies \(2\ell+1\).
   A ninth-order forward Lagrange stencil extracts the small-\(t\)
   coefficients of the normalized traces. The \(S^4\), \(S^2(1)\times
   S^2(1)\), and \(S^2(1)\times S^2(2)\) results form an invertible
   three-background linear system for the local \(R^2\),
   \(R_{\mu\nu}^2\), and \(R_{\mu\nu\rho\sigma}^2\) coefficients.

For \(\xi=0\) and \(0.23\), the recovered three local coefficients agree
with the exact specialization to better than \(1.6\times10^{-7}\) and
\(2.6\times10^{-8}\), respectively. This is an independent numerical
validation of the non-total-derivative \(B_4\) terms. It cannot test the
\(\Box R\) coefficient: its integral vanishes on every closed background
used here. That term remains a source-specialization result, explicitly
labeled as such rather than silently treated as spectrally checked.

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

The script is standard-library only. Its JSON output contains the source table,
specialized coefficients, raw spectral reconstructions, numerical errors,
regulated Gamma-integral values, and all pass/fail checks. The literature
bundle is .jarvis/runs/20260901T211018Z-literature-extract-the-general-scalar-laplace-t/.
The computation execution bundle is recorded with the validation command.
