"""Phase G GR calibration: flat-FLRW curvature with mostly-plus signature."""

import json

import sympy as sp

t, x, y, z, h = sp.symbols("t x y z H", real=True)
coordinates = (t, x, y, z)
scale_factor = sp.exp(h * t)
metric = sp.diag(-1, scale_factor**2, scale_factor**2, scale_factor**2)
inverse_metric = metric.inv()
dimension = len(coordinates)


def derivative(expression, coordinate_index):
    return sp.diff(expression, coordinates[coordinate_index])


christoffel = {}
for upper in range(dimension):
    for left in range(dimension):
        for right in range(dimension):
            christoffel[upper, left, right] = sp.simplify(
                sum(
                    inverse_metric[upper, middle]
                    * (
                        derivative(metric[middle, right], left)
                        + derivative(metric[middle, left], right)
                        - derivative(metric[left, right], middle)
                    )
                    / 2
                    for middle in range(dimension)
                )
            )

ricci = {}
for left in range(dimension):
    for right in range(dimension):
        ricci[left, right] = sp.simplify(
            sum(
                derivative(christoffel[upper, left, right], upper)
                - derivative(christoffel[upper, left, upper], right)
                + sum(
                    christoffel[upper, left, right] * christoffel[lower, upper, lower]
                    - christoffel[lower, left, upper] * christoffel[upper, right, lower]
                    for lower in range(dimension)
                )
                for upper in range(dimension)
            )
        )
direct_ricci_scalar = sp.simplify(
    sum(
        inverse_metric[left, right] * ricci[left, right]
        for left in range(dimension)
        for right in range(dimension)
    )
)
hubble = sp.simplify(sp.diff(scale_factor, t) / scale_factor)
hubble_form = sp.simplify(6 * (sp.diff(hubble, t) + 2 * hubble**2))

assert direct_ricci_scalar == 12 * h**2
assert hubble_form == 12 * h**2
assert sp.simplify(direct_ricci_scalar - hubble_form) == 0
assert sp.simplify(direct_ricci_scalar + 12 * h**2) != 0

print(
    json.dumps(
        {
            "benchmark": "gr_flat_flrw_curvature",
            "direct_ricci_scalar": str(direct_ricci_scalar),
            "hubble_form_ricci_scalar": str(hubble_form),
            "seeded_opposite_sign_rejected": True,
        },
        sort_keys=True,
    )
)
