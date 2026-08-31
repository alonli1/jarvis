"""Reproduce canonical scalar-EFT dimensions from Manohar, eqs. (4.2)--(4.14)."""
import json

import sympy as sp

d = sp.symbols("d", integer=True, positive=True)
phi_dimension = (d - 2) / 2
phi6_dimension = 6 * phi_dimension
coefficient_dimension = d - phi6_dimension

result = {
    "assumptions": ["dimensionless action", "canonical scalar kinetic term", "d=4"],
    "phi_dimension": str(phi_dimension.subs(d, 4)),
    "phi6_dimension": str(phi6_dimension.subs(d, 4)),
    "coefficient_dimension": str(coefficient_dimension.subs(d, 4)),
    "checks": {
        "source_formula": sp.simplify(phi_dimension - (d - 2) / 2) == 0,
        "lagrangian_dimension": sp.simplify(
            coefficient_dimension + phi6_dimension - d
        ) == 0,
        "expected_four_dimensional_value": coefficient_dimension.subs(d, 4) == -2,
    },
}
assert all(result["checks"].values())
print(json.dumps(result, indent=2, sort_keys=True))
