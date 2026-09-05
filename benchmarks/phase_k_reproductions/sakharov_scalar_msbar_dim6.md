# One real scalar: exact induced-gravity EFT through \(B_6\)

## Status

This is an exact symbolic result through curvature dimension six. It is an
intermediate heat-kernel result, not itself a graviton operator-dimension
truncation. The separate `sakharov_scalar_graviton_dim9` artifact applies
\([h]=1\), \([\kappa]=-1\) and shows that \(B_8\) is not needed when
\(n_h+n_\partial\leq9\).

The reproducible Wolfram calculation is
`sakharov_scalar_msbar_dim6.wls`; its machine-readable provenance and checks
are in `sakharov_scalar_msbar_dim6.spec.json`.

## Conventions and result

\[
S_E=\frac12\int d^dx\sqrt g\,\phi(-\nabla^2+m^2+\xi R)\phi,
\qquad d=4-2\epsilon .
\]

There is one real scalar and \(m>0\). Vassilevich uses
\(L=-(\nabla^2+E)\), hence \(E=-\xi R\), \(\Omega_{\mu\nu}=0\), and
\(R^\mu{}_{\nu\rho\sigma}=\partial_\sigma\Gamma^\mu_{\nu\rho}
-\partial_\rho\Gamma^\mu_{\nu\sigma}+\cdots\), with \(R=2\) on unit
\(S^2\). The Lorentzian normalization is mostly minus,
\(g_{\mu\nu}=\eta_{\mu\nu}+\kappa h_{\mu\nu}\), \([h]=1\),
\([\kappa]=-1\). The displayed determinant is Euclidean; Lorentzian use
requires the standard Wick continuation.

With \(L_m=\log(m^2/\mu^2)\),

\[
\Gamma^{(1)}_{E,\overline{\rm MS}}
=\int d^4x\sqrt g\left[
\frac{m^4}{64\pi^2}(L_m-\tfrac32)
+\frac{m^2}{32\pi^2}(\xi-\tfrac16)(L_m-1)R
+\frac{L_m}{32\pi^2}B_4-\frac{B_6}{32\pi^2m^2}
+O(B_8/m^4)\right],
\]

\[
B_4=\frac12(\xi-\tfrac16)^2R^2
+\frac1{180}(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2)
+\left(\frac1{30}-\frac\xi6\right)\Box R .
\]

The script constructs the following unreduced local \(B_6\) coefficients
exactly (the association keys define the invariant basis):

| Invariant | Coefficient |
| --- | --- |
| \(\Box^2R\) | \(1/280-\xi/60\) |
| \((\nabla R)^2\) | \(17/5040-\xi/30+\xi^2/12\) |
| \((\nabla R_{\mu\nu})^2\), \(\nabla_\alpha R_{\mu\nu}\nabla^\nu R^{\mu\alpha}\), \((\nabla R_{\mu\nu\rho\sigma})^2\) | \(-1/2520,-1/1260,1/560\) |
| \(R\Box R,R_{\mu\nu}\Box R^{\mu\nu},R_{\mu\nu}\nabla^\nu\nabla_\rho R^{\mu\rho},R_{\mu\nu\rho\sigma}\Box R^{\mu\nu\rho\sigma},R_{\mu\nu}\nabla^\mu\nabla^\nu R\) | \(1/180-11\xi/180+\xi^2/6,-1/630,1/210,1/420,-\xi/90\) |
| \(R^3,RR_{\mu\nu}^2,RR_{\mu\nu\rho\sigma}^2\) | \(1/1296-\xi/72+\xi^2/12-\xi^3/6,-1/1080+\xi/180,1/1080-\xi/180\) |
| \(R_\mu{}^\nu R_\nu{}^\rho R_\rho{}^\mu,R_{\mu\nu}R_{\rho\sigma}R^{\mu\rho\nu\sigma},R_{\mu\nu}R^\mu{}_{\rho\sigma\tau}R^{\nu\rho\sigma\tau}\) | \(-13/2835,-4/945,-1/945\) |
| \(R_{\mu\nu\rho\sigma}R^{\mu\nu\alpha\beta}R^{\rho\sigma}{}_{\alpha\beta},R_{\mu\nu\rho\sigma}R^{\mu\alpha\rho\beta}R^\nu{}_{\alpha}{}^\sigma{}_{\beta}\) | \(-11/11340,-1/567\) |

Set \(\xi=0\) for the minimally coupled scalar. Retaining \(\xi\) exposes
the optional non-minimal curvature coupling.

## Independent symbolic check

The script specializes the general \(a_6\) source table with exact Wolfram
rationals. Independently it applies Euler--Maclaurin to the unit-\(S^4\)
scalar spectrum \(\lambda_\ell=\ell(\ell+3)+12\xi\) with degeneracy
\(d_\ell=(2\ell+3)(\ell+2)(\ell+1)/6\). Both routes give

\[
\frac{(4\pi t)^2}{\operatorname{Vol}(S^4)}\operatorname{Tr}e^{-tD_E}
=1+(2-12\xi)t+(\tfrac{29}{15}-24\xi+72\xi^2)t^2
+(\tfrac{74}{63}-\tfrac{116}{5}\xi+144\xi^2-288\xi^3)t^3+O(t^4).
\]

The \(B_6\) coefficients agree identically; the conformal \(B_2\) and
\(B_4\) checks also pass.

## Evidence and blocker

The input tables are in
`knowledge/papers/vassilevich-heat-kernel-2003__hep-th_0306138.pdf`,
electronic PDF p. 40, eqs. (4.26)--(4.29). That page refers the general
\(a_8\) result to P. Amsterdamski, A. L. Berkin, and D. J. O'Connor,
*Class. Quantum Grav.* **6** (1989) 1981--1991,
DOI 10.1088/0264-9381/6/12/024.

The local corpus does not include that \(a_8\) table, and no installed
registered tool provides a generic off-shell \(a_8\) generator or a
dimension-eight curvature-basis reducer. That blocks a curvature-dimension
eight extension, but not the canonical graviton EFT through operator dimension
nine.

## Reproduction

```bash
WolframKernel -script benchmarks/phase_k_reproductions/sakharov_scalar_msbar_dim6.wls
```

The recorded Jarvis computation is
`.jarvis/runs/20260905T105050Z-computation-independently-specialize-the-one-rea`.
