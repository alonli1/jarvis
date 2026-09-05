(* Exact one-real-scalar heat-kernel specialization through B6.
   Source: Vassilevich, hep-th/0306138, electronic PDF p. 40, eq. (4.29).
   The final check independently derives the S4 heat trace by Euler--Maclaurin. *)

ClearAll[xi, t, x, delta, riem, mergeTerms];

geometryB6 = <|
  "BoxBoxR" -> 18/5040, "gradR2" -> 17/5040,
  "gradRicci2" -> -2/5040, "gradRicciMixed" -> -4/5040,
  "gradRiemann2" -> 9/5040, "RBoxR" -> 28/5040,
  "RicciBoxRicci" -> -8/5040, "RicciD2Ricci" -> 24/5040,
  "RiemannBoxRiemann" -> 12/5040, "R3" -> (35/9)/5040,
  "RRicci2" -> (-14/3)/5040, "RRiemann2" -> (14/3)/5040,
  "Ricci3" -> (-208/9)/5040, "RicciRicciRiemann" -> (-64/3)/5040,
  "RicciRiemann2" -> (-16/3)/5040, "Riemann3A" -> (-44/9)/5040,
  "Riemann3B" -> (-80/9)/5040
|>;
endomorphismB6 = <|
  "BoxBoxR" -> -xi/60, "RBoxR" -> xi^2/6 - xi/36 - xi/30,
  "gradR2" -> xi^2/12 - xi/30, "RicciD2R" -> -xi/90,
  "R3" -> -xi^3/6 + xi^2/12 - xi/72,
  "RRicci2" -> xi/180, "RRiemann2" -> -xi/180
|>;
mergeTerms[left_, right_] := Merge[{left, right}, Total // Simplify];
b2 = <|"R" -> 1/6 - xi|>;
b4 = <|"R2" -> (xi - 1/6)^2/2, "Ricci2" -> -1/180,
  "Riemann2" -> 1/180, "BoxR" -> 1/30 - xi/6|>;
b6 = mergeTerms[geometryB6, endomorphismB6];

(* Vassilevich convention: R^mu{}_{nu rho sigma}=partial_sigma Gamma^mu_{nu rho}
   -partial_rho Gamma^mu_{nu sigma}+..., so R=2 on unit S2. *)
d = 4;
delta[i_, j_] := KroneckerDelta[i, j];
riem[i_, j_, k_, l_] := -delta[i, k] delta[j, l] + delta[i, l] delta[j, k];
ricci[i_, j_] := Sum[riem[k, i, j, k], {k, d}];
scalarR = Sum[ricci[i, i], {i, d}];
ricci2 = Sum[ricci[i, j]^2, {i, d}, {j, d}];
riemann2 = Sum[riem[i, j, k, l]^2, {i, d}, {j, d}, {k, d}, {l, d}];
invariantsS4 = <|
  "R3" -> scalarR^3, "RRicci2" -> scalarR ricci2,
  "RRiemann2" -> scalarR riemann2,
  "Ricci3" -> Sum[ricci[i, j] ricci[j, k] ricci[k, i], {i, d}, {j, d}, {k, d}],
  "RicciRicciRiemann" -> Sum[ricci[i, j] ricci[k, l] riem[i, k, j, l], {i, d}, {j, d}, {k, d}, {l, d}],
  "RicciRiemann2" -> Sum[ricci[j, k] riem[j, n, l, p] riem[k, n, l, p], {j, d}, {k, d}, {n, d}, {l, d}, {p, d}],
  "Riemann3A" -> Sum[riem[i, j, k, n] riem[i, j, l, p] riem[k, n, l, p], {i, d}, {j, d}, {k, d}, {n, d}, {l, d}, {p, d}],
  "Riemann3B" -> Sum[riem[i, j, k, n] riem[i, l, k, p] riem[j, l, n, p], {i, d}, {j, d}, {k, d}, {n, d}, {l, d}, {p, d}]
|>;
b6S4FromLocal = Simplify[Total[KeyValueMap[If[KeyExistsQ[invariantsS4, #1], #2 invariantsS4[#1], 0] &, b6]]];

(* Independent exact route from lambda_l=l(l+3)+12 xi and
   d_l=(2l+3)(l+2)(l+1)/6. *)
a = 3/2;
f = (x^3 - x/4) Exp[-t x^2];
integral = Exp[-t a^2] ((a^2 - 1/4)/(2 t) + 1/(2 t^2));
emSum = integral + (f /. x -> a)/2 - Sum[BernoulliB[2 k]/(2 k)! (D[f, {x, 2 k - 1}] /. x -> a), {k, 1, 5}];
normalizedTraceS4 = Normal[Series[6 t^2 Exp[(9/4 - 12 xi) t] emSum/3, {t, 0, 3}]] // Expand;
b6S4FromSpectrum = Simplify[Coefficient[normalizedTraceS4, t, 3]];

checks = <|
  "B2_conformal_limit" -> Simplify[b2["R"] /. xi -> 1/6] === 0,
  "B4_R2_conformal_limit" -> Simplify[b4["R2"] /. xi -> 1/6] === 0,
  "S4_curvatures" -> {scalarR, ricci2, riemann2} === {12, 36, 24},
  "B6_S4_exact_spectral_agreement" -> Simplify[b6S4FromLocal - b6S4FromSpectrum] === 0,
  "dimension_B6_over_m2" -> 6 - 2 === 4
|>;
If[!And @@ Values[checks], Print[checks]; Exit[1]];
Print[InputForm[<|"B2" -> b2, "B4" -> b4, "B6" -> b6,
  "S4_trace" -> normalizedTraceS4, "checks" -> checks|>]];
