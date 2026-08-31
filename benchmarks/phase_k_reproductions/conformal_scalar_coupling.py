"""Reproduce the conformal scalar coupling in Birrell--Davies, eqs. (3.26)--(3.27)."""
import json

import sympy as sp

n = sp.symbols("n", integer=True, positive=True)
xi = (n - 2) / (4 * (n - 1))

result = {
    "assumptions": ["massless scalar", "conformal coupling", "n=4"],
    "xi_four_dimensions": str(sp.simplify(xi.subs(n, 4))),
    "curvature_term": "(1/6) R phi",
    "checks": {
        "four_dimensional_value": sp.simplify(xi.subs(n, 4) - sp.Rational(1, 6)) == 0,
        "two_dimensional_limit": sp.simplify(xi.subs(n, 2)) == 0,
        "flat_massless_limit": "Box phi = 0",
    },
}
assert result["checks"]["four_dimensional_value"]
assert result["checks"]["two_dimensional_limit"]
print(json.dumps(result, indent=2, sort_keys=True))
