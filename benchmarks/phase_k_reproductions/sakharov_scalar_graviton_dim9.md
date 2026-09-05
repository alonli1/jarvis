# Minimal real scalar: graviton EFT through canonical dimension 9

Use \(g_{\mu\nu}=\eta_{\mu\nu}+\kappa h_{\mu\nu}\), \([h]=1\), and \([\kappa]=-1\). A vertex \(\kappa^n h^n\partial^d\) has canonical operator dimension \(n+d\), so the result retains exactly those vertices with \(n+d\leq9\). It is for one minimally coupled scalar, \(\xi=0\), in \(d=4-2\epsilon\) and \(\overline{\rm MS}\). The coefficients below define the Euclidean determinant; use the declared Wick continuation for the mostly-minus Lorentzian action.

Modulo boundary terms and the four-dimensional Euler density,

\[
\Gamma_E^{(1)}=\int d^4x\sqrt g\left[C_0+C_RR+C_{R^2}R^2+C_{R_{\mu\nu}^2}R_{\mu\nu}R^{\mu\nu}+C_6\mathcal P_6+O(\partial^8)\right],
\]

\[
C_0=\frac{m^4}{64\pi^2}(L_m-\tfrac32),\quad C_R=-\frac{m^2}{192\pi^2}(L_m-1),\quad C_{R^2}=\frac{L_m}{3840\pi^2},\quad C_{R_{\mu\nu}^2}=\frac{L_m}{1920\pi^2},\quad C_6=-\frac1{32\pi^2m^2},
\]

where \(L_m=\log(m^2/\mu^2)\). The curvature-squared coefficients use \(E_4=R_{\mu\nu\rho\sigma}^2-4R_{\mu\nu}^2+R^2\): the original minimal-scalar heat-kernel result is \(R^2/120+R_{\mu\nu}^2/60\), plus \(E_4/180\) and a total derivative. The complete \(\mathcal P_6\) basis, its exact coefficients, their multiplication by \(C_6\), and the independent check are defined in this artifact's single canonical source, `sakharov_scalar_graviton_dim9.wls`; it is a vertex generator, not one operator.

For \([\sqrt{-g}\mathcal O]_{h^n}\), the term homogeneous in \(h\), the complete cutoff is

\[
\begin{aligned}
\mathcal L_{\leq9}={}&C_0\sum_{n=0}^{9}\kappa^n[\sqrt{-g}]_{h^n}+C_R\sum_{n=2}^{7}\kappa^n[\sqrt{-g}R]_{h^n}\\
&+C_{R^2}\sum_{n=2}^{5}\kappa^n[\sqrt{-g}R^2]_{h^n}+C_{R_{\mu\nu}^2}\sum_{n=2}^{5}\kappa^n[\sqrt{-g}R_{\mu\nu}^2]_{h^n}\\
&+C_6\left(\sum_{n=2}^{3}\kappa^n[\sqrt{-g}\mathcal P_6^{(2)}]_{h^n}+\kappa^3[\sqrt{-g}\mathcal P_6^{(3)}]_{h^3}\right).
\end{aligned}
\]

| Sector | Retained vertices | Dimensions |
| --- | --- | --- |
| \(C_0\sqrt{-g}\) | \(\kappa^n h^n,\ 0\le n\le9\) | 0--9 |
| \(C_R\sqrt{-g}R\) | \(\kappa^n h^n\partial^2,\ 2\le n\le7\) | 4--9 |
| curvature squared | \(\kappa^n h^n\partial^4,\ 2\le n\le5\) | 6--9 |
| \(\mathcal P_6^{(2)}\) | \(\kappa^n h^n\partial^6,\ n=2,3\) | 8, 9 |
| \(\mathcal P_6^{(3)}\) | \(\kappa^3h^3\partial^6\) | 9 |

\(\mathcal P_6^{(2)}\) comprises the quadratic derivative-curvature terms and \(\mathcal P_6^{(3)}\) the curvature-cubic terms. The Einstein linear term is a boundary term. The cosmological term has a tadpole unless a vacuum-energy counterterm is chosen to tune flat space.

The volume vertices are computed exactly from

\[
\sqrt{-g}=\exp\!\left[\frac12\sum_{r=1}^{9}\frac{(-1)^{r+1}}r\kappa^r\operatorname{tr}(\eta^{-1}h)^r\right]+O(h^{10}).
\]

For \(p_r=\operatorname{tr}(\eta^{-1}h)^r\), the first three are \(1\), \(p_1/2\), and \(p_1^2/8-p_2/4\); the executable derives all coefficients through \(h^9\).

No \(B_8\) input is required: a non-total-derivative curvature-dimension-eight invariant begins at \(h^2\partial^8\), of canonical dimension ten. A linear term such as \(\sqrt g\Box^3R\) is a boundary term.

Run `WolframKernel -script benchmarks/phase_k_reproductions/sakharov_scalar_graviton_dim9.wls`. The source heat-kernel tables are Vassilevich, `knowledge/papers/vassilevich-heat-kernel-2003__hep-th_0306138.pdf`, electronic PDF p. 40, eqs. (4.26)--(4.29). The recorded computation is `.jarvis/runs/20260905T112112Z-computation-construct-the-exact-one-real-minimal`.
