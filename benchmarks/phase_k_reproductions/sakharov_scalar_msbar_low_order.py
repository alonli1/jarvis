"""Independently check a one-real-scalar induced-gravity threshold.

Route A specializes the general Laplace-type heat-kernel formula from
Vassilevich, hep-th/0306138, electronic PDF p. 40, eqs. (4.26)--(4.28).
Route B extracts the same integrated B2 and B4 on the unit round S4 directly
from its scalar-Laplacian spectrum. The latter is a numerical spectral check,
not a second transcription of the local formula.
"""
import json
import math
from fractions import Fraction

XI = (Fraction(0), Fraction(1))
EULER_GAMMA = 0.5772156649015329


def add(left, right):
    """Add polynomials in xi represented by low-to-high coefficients."""
    return tuple(
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(max(len(left), len(right)))
    )


def scale(polynomial, factor):
    return tuple(factor * value for value in polynomial)


def multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


def evaluate(polynomial, value):
    return sum(
        float(coefficient) * value**power
        for power, coefficient in enumerate(polynomial)
    )


def specialize_general_heat_kernel():
    """Substitute E=-xi R and Omega=0 into the cited general formula."""
    # Source coefficients after the overall factors in eqs. (4.27)--(4.28).
    a2 = {"E": Fraction(1), "R": Fraction(1, 6)}
    a4 = {
        "box_E": Fraction(1, 6),
        "R_E": Fraction(1, 6),
        "E2": Fraction(1, 2),
        "box_R": Fraction(1, 30),
        "R2": Fraction(1, 72),
        "Ricci2": Fraction(-1, 180),
        "Riemann2": Fraction(1, 180),
        "Omega2": Fraction(1, 12),
    }
    b2 = {"R": add((a2["R"],), scale(XI, -a2["E"]))}
    b4 = {
        "R2": add(
            (a4["R2"],),
            add(
                scale(XI, -a4["R_E"]),
                scale(multiply(XI, XI), a4["E2"]),
            ),
        ),
        "Ricci2": (a4["Ricci2"],),
        "Riemann2": (a4["Riemann2"],),
        "box_R": add((a4["box_R"],), scale(XI, -a4["box_E"])),
    }
    return a2, a4, b2, b4


def s4_scalar_degeneracy(ell):
    """Dimension of degree-ell scalar harmonics on the unit S4."""
    return (2 * ell + 3) * (ell + 2) * (ell + 1) / 6


def s4_heat_trace(time, xi_value):
    """Trace exp[-t(-Delta + xi R)] from the complete scalar spectrum on S4."""
    total = 0.0
    ell = 0
    while ell < 10000:
        eigenvalue = ell * (ell + 3) + 12.0 * xi_value
        term = s4_scalar_degeneracy(ell) * math.exp(-time * eigenvalue)
        total += term
        if ell > 30 and term < 1.0e-16 * total:
            return total
        ell += 1
    raise RuntimeError("S4 spectral trace did not converge")


def normalized_s4_trace(time, xi_value):
    volume = 8.0 * math.pi**2 / 3.0
    return (4.0 * math.pi * time) ** 2 * s4_heat_trace(time, xi_value) / volume


def s2_heat_trace(time, inverse_radius_squared):
    """Scalar Laplacian heat trace on an S2 of inverse radius squared A."""
    total = 0.0
    ell = 0
    while ell < 10000:
        term = (2 * ell + 1) * math.exp(
            -time * inverse_radius_squared * ell * (ell + 1)
        )
        total += term
        if ell > 30 and term < 1.0e-16 * total:
            return total
        ell += 1
    raise RuntimeError("S2 spectral trace did not converge")


def normalized_s2xs2_trace(time, xi_value, first_curvature, second_curvature):
    """Normalized trace for S2(A) x S2(B), with A=1/r_1^2 and B=1/r_2^2."""
    scalar_curvature = 2.0 * (first_curvature + second_curvature)
    volume = 16.0 * math.pi**2 / (first_curvature * second_curvature)
    trace = (
        math.exp(-time * xi_value * scalar_curvature)
        * s2_heat_trace(time, first_curvature)
        * s2_heat_trace(time, second_curvature)
    )
    return (4.0 * math.pi * time) ** 2 * trace / volume


def polynomial_without_root(nodes, omitted):
    coefficients = [Fraction(1)]
    for node in nodes:
        if node == omitted:
            continue
        next_coefficients = [Fraction(0)] * (len(coefficients) + 1)
        for power, coefficient in enumerate(coefficients):
            next_coefficients[power] -= node * coefficient
            next_coefficients[power + 1] += coefficient
        coefficients = next_coefficients
    return coefficients


def forward_derivative_weights(node_count, derivative):
    """Exact Lagrange-stencil weights for f^(derivative)(0), unit spacing."""
    nodes = tuple(range(node_count))
    weights = []
    for node in nodes:
        denominator = math.prod(node - other for other in nodes if other != node)
        numerator = polynomial_without_root(nodes, node)[derivative]
        weights.append(Fraction(math.factorial(derivative) * numerator, denominator))
    return tuple(weights)


def spectral_heat_coefficients(normalized_trace, step=0.0005, node_count=9):
    """Extract B2 and B4 from a normalized small-time spectral heat trace."""
    values = [1.0]
    values.extend(
        normalized_trace(step * node)
        for node in range(1, node_count)
    )
    coefficients = {}
    for derivative, name in ((1, "B2"), (2, "B4")):
        weights = forward_derivative_weights(node_count, derivative)
        value = sum(
            float(weight) * sample for weight, sample in zip(weights, values)
        )
        coefficients[name] = value / (
            step**derivative * math.factorial(derivative)
        )
    return coefficients


def spectral_s4_coefficients(xi_value):
    return spectral_heat_coefficients(
        lambda time: normalized_s4_trace(time, xi_value)
    )


def spectral_s2xs2_coefficients(xi_value, first_curvature, second_curvature):
    return spectral_heat_coefficients(
        lambda time: normalized_s2xs2_trace(
            time, xi_value, first_curvature, second_curvature
        )
    )


def source_s4_coefficients(b2, b4, xi_value):
    """Evaluate the local specialization on R=12, Ricci2=36, Riemann2=24."""
    return {
        "B2": 12.0 * evaluate(b2["R"], xi_value),
        "B4": (
            144.0 * evaluate(b4["R2"], xi_value)
            + 36.0 * evaluate(b4["Ricci2"], xi_value)
            + 24.0 * evaluate(b4["Riemann2"], xi_value)
        ),
    }


def solve_linear_system(rows, values):
    """Solve a small dense linear system with Gauss-Jordan elimination."""
    augmented = [list(map(float, row)) + [float(value)] for row, value in zip(rows, values)]
    size = len(augmented)
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1.0e-14:
            raise RuntimeError("singular spectral-background system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(size)]


def spectral_local_b4_coefficients(xi_value):
    """Resolve three local curvature-squared coefficients from three spectra."""
    backgrounds = {
        "S4_unit": {
            "coefficients": spectral_s4_coefficients(xi_value),
            "invariants": (144.0, 36.0, 24.0),
        },
        "S2xS2_A1_B1": {
            "coefficients": spectral_s2xs2_coefficients(xi_value, 1.0, 1.0),
            "invariants": (16.0, 4.0, 8.0),
        },
        "S2xS2_A1_B2": {
            "coefficients": spectral_s2xs2_coefficients(xi_value, 1.0, 2.0),
            "invariants": (36.0, 10.0, 20.0),
        },
    }
    solution = solve_linear_system(
        [entry["invariants"] for entry in backgrounds.values()],
        [entry["coefficients"]["B4"] for entry in backgrounds.values()],
    )
    return backgrounds, dict(zip(("R2", "Ricci2", "Riemann2"), solution))


def gamma_residue_at_nonpositive_integer(order):
    """Residue of Gamma(order-2+epsilon) at epsilon=0 for orders 0, 1, 2."""
    pole_index = 2 - order
    return Fraction((-1) ** pole_index, math.factorial(pole_index))


def msbar_regulated_coefficient(order, mass, scale, epsilon):
    """Numerically subtract the MS-bar pole of the proper-time Gamma integral."""
    raw = (
        -0.5
        * scale ** (2.0 * epsilon)
        * (4.0 * math.pi) ** (-2.0 + epsilon)
        * mass ** (4.0 - 2.0 * order - 2.0 * epsilon)
        * math.gamma(order - 2.0 + epsilon)
    )
    pole_coefficient = (
        -0.5
        * mass ** (4.0 - 2.0 * order)
        / (4.0 * math.pi) ** 2
        * float(gamma_residue_at_nonpositive_integer(order))
    )
    return raw - pole_coefficient * (
        1.0 / epsilon - EULER_GAMMA + math.log(4.0 * math.pi)
    )


def richardson_msbar_coefficient(order, mass, scale, epsilon=0.0001):
    coarse = msbar_regulated_coefficient(order, mass, scale, epsilon)
    fine = msbar_regulated_coefficient(order, mass, scale, epsilon / 2.0)
    return 2.0 * fine - coarse


def main():
    a2, a4, b2, b4 = specialize_general_heat_kernel()
    assert b2["R"] == (Fraction(1, 6), Fraction(-1))
    assert b4["R2"] == (Fraction(1, 72), Fraction(-1, 6), Fraction(1, 2))
    assert evaluate(b2["R"], Fraction(1, 6)) == 0
    assert evaluate(b4["R2"], Fraction(1, 6)) == 0

    # g = eta + kappa h: [h] = 1 and [kappa] = -1 in four dimensions.
    dimensions = {"h": 1, "kappa": -1, "partial": 1, "mass": 1}
    curvature_dimension = (
        dimensions["kappa"] + 2 * dimensions["partial"] + dimensions["h"]
    )
    assert dimensions["kappa"] + dimensions["h"] == 0
    assert curvature_dimension == 2
    assert 3 * curvature_dimension - 2 * dimensions["mass"] == 4
    assert 4 * curvature_dimension - 4 * dimensions["mass"] == 4

    spectral_checks = {}
    for xi_value in (0.0, 0.23):
        source_s4 = source_s4_coefficients(b2, b4, xi_value)
        spectral_s4 = spectral_s4_coefficients(xi_value)
        s4_errors = {
            name: abs(spectral_s4[name] - source_s4[name])
            for name in source_s4
        }
        backgrounds, spectral_local = spectral_local_b4_coefficients(xi_value)
        source_local = {
            name: evaluate(b4[name], xi_value)
            for name in ("R2", "Ricci2", "Riemann2")
        }
        local_errors = {
            name: abs(spectral_local[name] - source_local[name])
            for name in source_local
        }
        spectral_checks[str(xi_value)] = {
            "S4": {
                "source": source_s4,
                "spectral": spectral_s4,
                "absolute_errors": s4_errors,
                "B2_agrees": s4_errors["B2"] < 2.0e-7,
                "B4_agrees": s4_errors["B4"] < 2.0e-5,
            },
            "local_B4": {
                "backgrounds": backgrounds,
                "source": source_local,
                "spectral": spectral_local,
                "absolute_errors": local_errors,
                "agrees": all(error < 3.0e-6 for error in local_errors.values()),
            },
        }

    mass, scale = 2.7, 1.3
    log_mass = math.log(mass**2 / scale**2)
    analytic_finite_coefficients = {
        "B0": mass**4 * (log_mass - 1.5) / (64.0 * math.pi**2),
        "B2": mass**2 * (1.0 - log_mass) / (32.0 * math.pi**2),
        "B4": log_mass / (32.0 * math.pi**2),
    }
    dimreg_coefficients = {
        "B0": richardson_msbar_coefficient(0, mass, scale),
        "B2": richardson_msbar_coefficient(1, mass, scale),
        "B4": richardson_msbar_coefficient(2, mass, scale),
    }
    dimreg_errors = {
        name: abs(dimreg_coefficients[name] - analytic_finite_coefficients[name])
        for name in analytic_finite_coefficients
    }

    result = {
        "assumptions": [
            "one real scalar",
            "smooth compact boundaryless Euclidean background",
            "D_E = -nabla^2 + m^2 + xi R",
            "d = 4 - 2 epsilon, MS-bar",
            "g = eta + kappa h, [h] = 1, [kappa] = -1",
            "unit round S4 spectral check: lambda_l=l(l+3), d_l=(2l+3)(l+2)(l+1)/6",
        ],
        "general_source_coefficients": {
            "a2": {name: str(value) for name, value in a2.items()},
            "a4": {name: str(value) for name, value in a4.items()},
        },
        "B2_xi_polynomial": [str(value) for value in b2["R"]],
        "B4": {
            "R2_xi_polynomial": [str(value) for value in b4["R2"]],
            "Ricci2": str(b4["Ricci2"][0]),
            "Riemann2": str(b4["Riemann2"][0]),
            "box_R_xi_polynomial": [str(value) for value in b4["box_R"]],
        },
        "spectral_S4_check": spectral_checks,
        "msbar_dimreg_check": {
            "analytic_finite_coefficients": analytic_finite_coefficients,
            "gamma_integral_coefficients": dimreg_coefficients,
            "absolute_errors": dimreg_errors,
        },
        "checks": {
            "general_formula_specialization_exact": True,
            "conformal_B2_zero": True,
            "conformal_R2_coefficient_zero": True,
            "metric_perturbation_dimensionless": True,
            "curvature_dimension_two": True,
            "dimension_six_term_dimension_four": True,
            "dimension_eight_term_dimension_four": True,
            "spectral_S4_B2_agrees": all(
                item["S4"]["B2_agrees"] for item in spectral_checks.values()
            ),
            "spectral_S4_B4_agrees": all(
                item["S4"]["B4_agrees"] for item in spectral_checks.values()
            ),
            "spectral_local_B4_terms_agree": all(
                item["local_B4"]["agrees"] for item in spectral_checks.values()
            ),
            "msbar_B0_gamma_integral_agrees": dimreg_errors["B0"] < 2.0e-7,
            "msbar_B2_gamma_integral_agrees": dimreg_errors["B2"] < 2.0e-8,
            "msbar_B4_gamma_integral_agrees": dimreg_errors["B4"] < 2.0e-8,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
