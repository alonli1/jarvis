(* Minimal real scalar EFT vertices with n[h]+n[partial] <= 9. *)
ClearAll[kappa, p, lm, m, vertexRange];
sqrtSeries = Normal[Series[Exp[1/2 Sum[(-1)^(r + 1) kappa^r p[r]/r, {r, 1, 9}]], {kappa, 0, 9}]] // Expand;
volumeVertices = Association@Table[n -> Coefficient[sqrtSeries, kappa, n], {n, 0, 9}];
wilson = <|"C0" -> m^4/(64 Pi^2) (lm - 3/2), "CR" -> -m^2/(192 Pi^2) (lm - 1), "CR2" -> lm/(3840 Pi^2), "CRicci2" -> lm/(1920 Pi^2), "C6" -> -1/(32 Pi^2 m^2)|>;
b6Quadratic = <|"(nabla R)^2" -> 17/5040, "(nabla Ricci)^2" -> -1/2520, "nabla Ricci nabla^T Ricci" -> -1/1260, "(nabla Riemann)^2" -> 1/560, "R Box R" -> 1/180, "Ricci Box Ricci" -> -1/630, "Ricci nabla nabla Ricci" -> 1/210, "Riemann Box Riemann" -> 1/420|>;
b6Cubic = <|"R^3" -> 1/1296, "R Ricci^2" -> -1/1080, "R Riemann^2" -> 1/1080, "Ricci^3" -> -13/2835, "Ricci Ricci Riemann" -> -4/945, "Ricci Riemann^2" -> -1/945, "Riemann^3_A" -> -11/11340, "Riemann^3_B" -> -1/567|>;
vertexRange[name_, derivatives_, minFields_] := <|"sector" -> name, "derivatives" -> derivatives, "h_range" -> Range[minFields, 9 - derivatives], "canonical_dimensions" -> Range[minFields + derivatives, 9]|>;
sectors = {vertexRange["C0 Sqrt[-g]", 0, 0], vertexRange["CR Sqrt[-g] R", 2, 2], vertexRange["CR2 Sqrt[-g] R^2", 4, 2], vertexRange["CRicci2 Sqrt[-g] Ricci^2", 4, 2], vertexRange["C6 P6 quadratic", 6, 2], vertexRange["C6 P6 cubic", 6, 3]};
checks = <|"volume_h0_to_h9" -> Keys[volumeVertices] === Range[0, 9], "EH_h2_to_h7" -> sectors[[2, "h_range"]] === Range[2, 7], "curvature_squared_h2_to_h5" -> sectors[[3, "h_range"]] === Range[2, 5], "P6_quadratic_h2_to_h3" -> sectors[[5, "h_range"]] === {2, 3}, "P6_cubic_h3" -> sectors[[6, "h_range"]] === {3}, "B8_first_nonboundary_dimension" -> 2 + 8 === 10|>;
If[!And @@ Values[checks], Print[checks]; Exit[1]];
result = <|"sqrt_minus_g_vertices" -> volumeVertices, "wilson" -> wilson, "sectors" -> sectors, "P6_quadratic_times_C6" -> b6Quadratic, "P6_cubic_times_C6" -> b6Cubic, "checks" -> checks|>;
Print[ToString[InputForm[result]]];
