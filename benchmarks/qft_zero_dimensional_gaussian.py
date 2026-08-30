"""Phase G QFT calibration: normalized zero-dimensional Gaussian moments."""

import json

import sympy as sp
from mpmath import mp

phi, sigma = sp.symbols("phi sigma", positive=True, real=True)
density = sp.exp(-(phi**2) / (2 * sigma**2)) / (sp.sqrt(2 * sp.pi) * sigma)
second = sp.simplify(sp.integrate(phi**2 * density, (phi, -sp.oo, sp.oo)))
fourth = sp.simplify(sp.integrate(phi**4 * density, (phi, -sp.oo, sp.oo)))
connected_fourth = sp.simplify(fourth - 3 * second**2)

mp.dps = 50
numeric_sigma = mp.mpf("2")
numeric_density = lambda value: (
    mp.exp(-(value**2) / (2 * numeric_sigma**2)) / (mp.sqrt(2 * mp.pi) * numeric_sigma)
)
numeric_fourth = mp.quad(lambda value: value**4 * numeric_density(value), [-mp.inf, mp.inf])
expected_numeric_fourth = 3 * numeric_sigma**4

assert second == sigma**2
assert fourth == 3 * sigma**4
assert connected_fourth == 0
assert sp.simplify(fourth - sigma**4) != 0
assert mp.almosteq(numeric_fourth, expected_numeric_fourth)

print(
    json.dumps(
        {
            "benchmark": "qft_zero_dimensional_gaussian",
            "second_moment": str(second),
            "fourth_moment": str(fourth),
            "connected_fourth": str(connected_fourth),
            "numerical_fourth_moment_at_sigma_2": str(numeric_fourth),
            "seeded_unpaired_fourth_rejected": True,
        },
        sort_keys=True,
    )
)
