(*
  Canonical, self-contained symbolic source for the one-real-minimal-scalar
  induced-gravity EFT, retaining graviton vertices with n[h]+n[derivatives]<=9.

  Conventions: Euclidean heat kernel for D=-nabla^2+m^2, then Wick continue
  to mostly-minus Lorentzian signature. g=eta+kappa h, [h]=1, [kappa]=-1,
  Lm=Log[m^2/mu^2], and xi=0. Curvature signs are those of Vassilevich,
  hep-th/0306138, electronic PDF p. 40, eqs. (4.26)-(4.29).

  This file is the only mathematical source of truth for this dim-9 artifact:
  it contains the B4 reduction, every retained P6 coefficient, the vertex
  selection, the exact volume expansion, and the independent S4 spectral check.
*)

ClearAll[kappa, p, m, mu, Lm, t, x, xi, delta, riem, vertexRange];

(* Published heat-kernel inputs, specialized exactly to one real scalar at xi=0. *)
b4Source = <|"R^2" -> 1/72, "Ricci^2" -> -1/180,
  "Riemann^2" -> 1/180, "Box R" -> 1/30|>;
eulerDensity = "E4 = Riemann^2 - 4 Ricci^2 + R^2";
b4Bulk = <|"R^2" -> Simplify[b4Source["R^2"] - b4Source["Riemann^2"]],
  "Ricci^2" -> Simplify[b4Source["Ricci^2"] + 4 b4Source["Riemann^2"]]|>;

(* P6 is modulo the pure total derivative Box Box R. The named contractions
   fix the basis; all entries below are coefficients inside B6, before C6. *)
p6Quadratic = <|
  "(nabla R)^2" -> 17/5040,
  "(nabla_a R_mn)^2" -> -1/2520,
  "nabla_a R_mn nabla_n R_ma" -> -1/1260,
  "(nabla_a R_mnrs)^2" -> 1/560,
  "R Box R" -> 1/180,
  "R_mn Box R_mn" -> -1/630,
  "R_mn nabla_n nabla_r R_mr" -> 1/210,
  "R_mnrs Box R_mnrs" -> 1/420|>;
p6Cubic = <|
  "R^3" -> 1/1296,
  "R R_mn R_mn" -> -1/1080,
  "R R_mnrs R_mnrs" -> 1/1080,
  "R_mn R_np R_pm" -> -13/2835,
  "R_mn R_rs R_mrns" -> -4/945,
  "R_mn R_mrst R_nrst" -> -1/945,
  "R_mnrs R_mnpq R_rspq" -> -11/11340,
  "R_mnrs R_mprq R_npsq" -> -1/567|>;

Lm = Log[m^2/mu^2];
wilson = <|
  "C0" -> m^4 (Lm - 3/2)/(64 Pi^2),
  "CR" -> -m^2 (Lm - 1)/(192 Pi^2),
  "CR2" -> Lm/(3840 Pi^2),
  "CRicci2" -> Lm/(1920 Pi^2),
  "C6" -> -1/(32 Pi^2 m^2)|>;
p6WilsonQuadratic = Association @@ KeyValueMap[#1 -> Together[wilson["C6"] #2] &, p6Quadratic];
p6WilsonCubic = Association @@ KeyValueMap[#1 -> Together[wilson["C6"] #2] &, p6Cubic];

(* Exact trace-log computation of sqrt(-g), through h^9. *)
sqrtSeries = Normal[Series[
    Exp[1/2 Sum[(-1)^(r + 1) kappa^r p[r]/r, {r, 1, 9}]],
    {kappa, 0, 9}]] // Expand;
volumeVertices = Association@Table[n -> Coefficient[sqrtSeries, kappa, n], {n, 0, 9}];

vertexRange[name_, derivatives_, minFields_] := <|
  "sector" -> name, "derivatives" -> derivatives,
  "h_range" -> Range[minFields, 9 - derivatives],
  "canonical_dimensions" -> Range[minFields + derivatives, 9]|>;
sectors = {
  vertexRange["C0 Sqrt[-g]", 0, 0],
  vertexRange["CR Sqrt[-g] R", 2, 2],
  vertexRange["CR2 Sqrt[-g] R^2", 4, 2],
  vertexRange["CRicci2 Sqrt[-g] Ricci^2", 4, 2],
  vertexRange["C6 P6 quadratic", 6, 2],
  vertexRange["C6 P6 cubic", 6, 3]};

(* Independent check: evaluate the local B6 table on unit S4 and compare it
   to the scalar spectrum via exact Euler--Maclaurin asymptotics. *)
d = 4;
delta[i_, j_] := KroneckerDelta[i, j];
riem[i_, j_, k_, l_] := -delta[i, k] delta[j, l] + delta[i, l] delta[j, k];
ricci[i_, j_] := Sum[riem[k, i, j, k], {k, d}];
scalarR = Sum[ricci[i, i], {i, d}];
ricci2 = Sum[ricci[i, j]^2, {i, d}, {j, d}];
riemann2 = Sum[riem[i, j, k, l]^2, {i, d}, {j, d}, {k, d}, {l, d}];
invariantsS4 = <|
  "R^3" -> scalarR^3,
  "R R_mn R_mn" -> scalarR ricci2,
  "R R_mnrs R_mnrs" -> scalarR riemann2,
  "R_mn R_np R_pm" -> Sum[ricci[i, j] ricci[j, k] ricci[k, i], {i, d}, {j, d}, {k, d}],
  "R_mn R_rs R_mrns" -> Sum[ricci[i, j] ricci[k, l] riem[i, k, j, l], {i, d}, {j, d}, {k, d}, {l, d}],
  "R_mn R_mrst R_nrst" -> Sum[ricci[j, k] riem[j, n, l, q] riem[k, n, l, q], {j, d}, {k, d}, {n, d}, {l, d}, {q, d}],
  "R_mnrs R_mnpq R_rspq" -> Sum[riem[i, j, k, n] riem[i, j, l, q] riem[k, n, l, q], {i, d}, {j, d}, {k, d}, {n, d}, {l, d}, {q, d}],
  "R_mnrs R_mprq R_npsq" -> Sum[riem[i, j, k, n] riem[i, l, k, q] riem[j, l, n, q], {i, d}, {j, d}, {k, d}, {n, d}, {l, d}, {q, d}]|>;
b6S4FromLocal = Simplify[Total[KeyValueMap[#2 invariantsS4[#1] &, p6Cubic]]];
a = 3/2;
f = (x^3 - x/4) Exp[-t x^2];
integral = Exp[-t a^2] ((a^2 - 1/4)/(2 t) + 1/(2 t^2));
emSum = integral + (f /. x -> a)/2 - Sum[BernoulliB[2 k]/(2 k)! (D[f, {x, 2 k - 1}] /. x -> a), {k, 1, 5}];
normalizedTraceS4 = Normal[Series[6 t^2 Exp[(9/4 - 12 xi) t] emSum/3, {t, 0, 3}]] // Expand;
b6S4FromSpectrum = Simplify[Coefficient[normalizedTraceS4 /. xi -> 0, t, 3]];

checks = <|
  "B4_Gauss_Bonnet_reduction" -> b4Bulk === <|"R^2" -> 1/120, "Ricci^2" -> 1/60|>,
  "volume_h0_to_h9" -> Keys[volumeVertices] === Range[0, 9],
  "EH_h2_to_h7" -> sectors[[2, "h_range"]] === Range[2, 7],
  "curvature_squared_h2_to_h5" -> sectors[[3, "h_range"]] === Range[2, 5],
  "P6_quadratic_h2_to_h3" -> sectors[[5, "h_range"]] === {2, 3},
  "P6_cubic_h3" -> sectors[[6, "h_range"]] === {3},
  "B8_first_nonboundary_dimension" -> 2 + 8 === 10,
  "S4_curvatures" -> {scalarR, ricci2, riemann2} === {12, 36, 24},
  "B6_S4_exact_spectral_agreement" -> Simplify[b6S4FromLocal - b6S4FromSpectrum] === 0|>;
If[!And @@ Values[checks], Print[InputForm[checks]]; Exit[1]];

result = <|
  "conventions" -> <|"signature" -> "mostly minus after Wick continuation", "metric_split" -> "g=eta+kappa h", "h_dimension" -> 1, "kappa_dimension" -> -1, "scheme" -> "MSbar", "scalar" -> "one real, xi=0"|>,
  "source" -> <|"reference" -> "Vassilevich hep-th/0306138 eqs. (4.26)-(4.29)", "basis_relation" -> eulerDensity|>,
  "B4_source" -> b4Source, "B4_bulk_mod_E4_and_boundary" -> b4Bulk,
  "wilson" -> wilson, "P6_quadratic" -> p6Quadratic, "P6_cubic" -> p6Cubic,
  "P6_quadratic_times_C6" -> p6WilsonQuadratic, "P6_cubic_times_C6" -> p6WilsonCubic,
  "sqrt_minus_g_vertices" -> volumeVertices, "sectors" -> sectors,
  "S4_local_B6" -> b6S4FromLocal, "S4_spectral_B6" -> b6S4FromSpectrum,
  "checks" -> checks|>;
Print[ToString[InputForm[result]]];
