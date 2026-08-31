"""Reproduce the Schwarzschild entropy algebra in Kiefer, eqs. (7.23)--(7.24)."""
import json

import sympy as sp

G, M, scale = sp.symbols("G M scale", positive=True)
radius = 2 * G * M
area = 4 * sp.pi * radius**2
entropy = sp.simplify(area / (4 * G))

result = {
    "assumptions": ["c=hbar=k_B=1", "Schwarzschild radius r_s=2 G M"],
    "area": str(area),
    "entropy": str(entropy),
    "checks": {
        "source_schwarzschild_form": sp.simplify(entropy - sp.pi * radius**2 / G) == 0,
        "mass_scaling": sp.simplify(entropy.subs(M, scale * M) / entropy - scale**2) == 0,
        "positive_for_positive_mass": "G > 0 and M > 0 imply S_BH > 0",
    },
}
assert result["checks"]["source_schwarzschild_form"]
assert result["checks"]["mass_scaling"]
print(json.dumps(result, indent=2, sort_keys=True))
