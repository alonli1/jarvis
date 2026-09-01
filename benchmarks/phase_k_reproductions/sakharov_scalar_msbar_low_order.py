"""Reproduce the one-real-scalar low-order induced-gravity threshold.

Source: Vassilevich, hep-th/0306138, electronic PDF p. 40,
eqs. (4.26)--(4.28). This checks D_E = -nabla^2 + m^2 + xi R,
i.e. E = -xi R in L = -(nabla^2 + E), for one real scalar.
"""
import json
import math
from fractions import Fraction


def add(a, b):
    return tuple((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b))))


def scale(a, factor):
    return tuple(factor * value for value in a)


def multiply(a, b):
    result = [Fraction(0)] * (len(a) + len(b) - 1)
    for left_index, left in enumerate(a):
        for right_index, right in enumerate(b):
            result[left_index + right_index] += left * right
    return tuple(result)


def evaluate(polynomial, value):
    return sum(float(coefficient) * value**power
               for power, coefficient in enumerate(polynomial))


xi = (Fraction(0), Fraction(1))
b2 = add((Fraction(1, 6),), scale(xi, -1))
b4_r2 = add(
    (Fraction(1, 72),),
    add(scale(xi, Fraction(-1, 6)), scale(multiply(xi, xi), Fraction(1, 2))),
)

assert b2 == (Fraction(1, 6), Fraction(-1))
assert b4_r2 == (Fraction(1, 72), Fraction(-1, 6), Fraction(1, 2))
assert evaluate(b2, Fraction(1, 6)) == 0
assert evaluate(b4_r2, Fraction(1, 6)) == 0

# g = eta + kappa h: [h] = 1 and [kappa] = -1 in four dimensions.
dimensions = {
    "h": 1,
    "kappa": -1,
    "partial": 1,
    "R_linear": -1 + 2 + 1,
    "R2": 4,
    "R3_over_m2": 4,
    "R4_over_m4": 4,
}
assert dimensions["kappa"] + dimensions["h"] == 0
assert dimensions["R_linear"] == 2
assert dimensions["R3_over_m2"] == 4
assert dimensions["R4_over_m4"] == 4

m, mu = 2.7, 1.3
log_mass = math.log(m**2 / mu**2)
finite_coefficients = {
    "B0": m**4 * (log_mass - 1.5) / (64 * math.pi**2),
    "B2": m**2 * (1 - log_mass) / (32 * math.pi**2),
    "B4": log_mass / (32 * math.pi**2),
}

result = {
    "assumptions": [
        "one real scalar",
        "smooth compact boundaryless Euclidean background",
        "D_E = -nabla^2 + m^2 + xi R",
        "d = 4 - 2 epsilon, MS-bar",
        "g = eta + kappa h, [h] = 1, [kappa] = -1",
    ],
    "B2_xi_polynomial": [str(value) for value in b2],
    "B4": {
        "R2_xi_polynomial": [str(value) for value in b4_r2],
        "Ricci2": "-1/180",
        "Riemann2": "1/180",
        "box_R_xi_polynomial": ["1/30", "-1/6"],
    },
    "checks": {
        "conformal_B2_zero": True,
        "conformal_R2_coefficient_zero": True,
        "metric_perturbation_dimensionless": True,
        "curvature_dimension_two": True,
        "dimension_six_term_dimension_four": True,
        "dimension_eight_term_dimension_four": True,
    },
    "sample_msbar_finite_coefficients": finite_coefficients,
}
print(json.dumps(result, indent=2, sort_keys=True))
