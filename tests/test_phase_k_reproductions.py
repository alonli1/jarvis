import json
import subprocess
import sys
from pathlib import Path

from jarvis.reproduction import ImplementationSpecification

ROOT = Path(__file__).parents[1]
BENCHMARKS = ROOT / "benchmarks" / "phase_k_reproductions"


def test_phase_k_reproduction_specs_and_scripts_are_reproducible():
    expected = {
        "eft_phi6_dimensions": {"coefficient_dimension": "-2"},
        "conformal_scalar_coupling": {"xi_four_dimensions": "1/6"},
        "schwarzschild_entropy": {"entropy": "4*pi*G*M**2"},
        "sakharov_scalar_msbar_low_order": {
            "B2_xi_polynomial": ["1/6", "-1"],
        },
    }

    for name, values in expected.items():
        spec = ImplementationSpecification.model_validate_json(
            (BENCHMARKS / f"{name}.spec.json").read_text(encoding="utf-8")
        )
        completed = subprocess.run(
            [sys.executable, str(BENCHMARKS / f"{name}.py")],
            capture_output=True,
            check=True,
            text=True,
        )
        result = json.loads(completed.stdout)

        assert spec.engine == "python"
        assert result["checks"]
        assert all(value is True for value in result["checks"].values() if isinstance(value, bool))
        assert all(result[key] == value for key, value in values.items())
