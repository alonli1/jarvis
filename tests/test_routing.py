import pytest

from jarvis.config import ModelProfile
from jarvis.routing import TaskFeatures, route


def _profiles():
    return {
        capability: ModelProfile(capability, "test", f"test/{capability}", capability)
        for capability in ("extract", "science_fast", "science_standard", "science_deep", "science_critical")
    }


def test_role_priors_and_escalations_choose_lowest_matching_profile():
    profiles = _profiles()
    assert route(profiles, "retrieval", TaskFeatures()).profile.name == "science_fast"
    decision = route(profiles, "retrieval", TaskFeatures(novelty=2))
    assert decision.floor == "science_deep"
    assert decision.profile.name == "science_deep"
    assert "novelty>=2" in decision.reason_codes


def test_low_verification_escalates_high_consequence_without_critical_auto_selection():
    decision = route(
        _profiles(), "retrieval", TaskFeatures(consequence=2, verification_strength=1)
    )
    assert decision.floor == "science_deep"
    assert decision.profile.name == "science_deep"


def test_unavailable_or_invalid_profile_fails_safely():
    profiles = {"fast": ModelProfile("fast", "test", "test/fast", "science_fast")}
    with pytest.raises(ValueError, match="science_deep"):
        route(profiles, "retrieval", TaskFeatures(convention_sensitivity=2))
    with pytest.raises(ValueError, match="does not meet"):
        route(_profiles(), "retrieval", TaskFeatures(novelty=2), "science_fast")


def test_unknown_role_and_invalid_features_fail_clearly():
    with pytest.raises(ValueError, match="Unknown role"):
        route(_profiles(), "unknown", TaskFeatures())
    with pytest.raises(ValueError, match="novelty"):
        TaskFeatures(novelty=4)
