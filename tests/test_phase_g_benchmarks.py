import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_benchmark(name: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "benchmarks" / name)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def test_qft_gaussian_benchmark_has_independent_numeric_check_and_seed_rejection():
    result = run_benchmark("qft_zero_dimensional_gaussian.py")

    assert result["second_moment"] == "sigma**2"
    assert result["fourth_moment"] == "3*sigma**4"
    assert result["connected_fourth"] == "0"
    assert result["numerical_fourth_moment_at_sigma_2"] == "48.0"
    assert result["seeded_unpaired_fourth_rejected"] is True


def test_gr_flrw_benchmark_matches_direct_and_hubble_form_checks():
    result = run_benchmark("gr_flat_flrw_curvature.py")

    assert result["direct_ricci_scalar"] == "12*H**2"
    assert result["hubble_form_ricci_scalar"] == "12*H**2"
    assert result["seeded_opposite_sign_rejected"] is True
