from jarvis.calibration import CalibrationCase, calibrate_profiles
from jarvis.config import ModelProfile


def test_compatible_profiles_can_be_swapped_across_providers_without_run_state():
    profiles = {
        "provider-a": ModelProfile(
            "provider-a", "provider-a", "provider-a/model", "science_standard"
        ),
        "provider-b": ModelProfile("provider-b", "provider-b", "provider-b/model", "science_deep"),
    }

    results = calibrate_profiles(profiles, [CalibrationCase("case", "science_standard")])

    assert {(result.provider, result.compatible) for result in results} == {
        ("provider-a", True),
        ("provider-b", True),
    }
