from __future__ import annotations

from dataclasses import asdict, dataclass

from .config import ModelProfile

CAPABILITIES = ("extract", "science_fast", "science_standard", "science_deep", "science_critical")
ROLE_FLOORS = {
    "metadata": "extract",
    "triage": "extract",
    "retrieval": "science_fast",
    "computation": "science_fast",
    "literature": "science_standard",
    "derivation": "science_standard",
    "research_planning": "science_deep",
    "review": "science_deep",
    "critical_review": "science_critical",
}


@dataclass(frozen=True)
class TaskFeatures:
    novelty: int = 0
    ambiguity: int = 0
    mathematical_depth: int = 0
    convention_sensitivity: int = 0
    tool_dependence: int = 0
    verification_strength: int = 0
    literature_uncertainty: int = 0
    coupling: int = 0
    consequence: int = 0
    context_burden: int = 0
    creative_search: int = 0

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 3:
                raise ValueError(f"{name} must be an integer from 0 to 3")


@dataclass(frozen=True)
class RouteDecision:
    profile: ModelProfile
    features: TaskFeatures
    floor: str
    reason_codes: tuple[str, ...]
    explanation: str

    def as_dict(self) -> dict:
        return {
            "explanation": self.explanation,
            "features": asdict(self.features),
            "floor": self.floor,
            "profile": {
                "capability": self.profile.capability,
                "model": self.profile.model,
                "name": self.profile.name,
                "provider": self.profile.provider,
            },
            "reason_codes": list(self.reason_codes),
        }


def _rank(capability: str) -> int:
    try:
        return CAPABILITIES.index(capability)
    except ValueError as exc:
        raise ValueError(f"Unknown capability: {capability}") from exc


def route(
    profiles: dict[str, ModelProfile], role: str, features: TaskFeatures, profile: str | None = None
) -> RouteDecision:
    if role not in ROLE_FLOORS:
        raise ValueError(f"Unknown role: {role}")
    floor = ROLE_FLOORS[role]
    reasons = [f"role:{role}"]
    deep_features = (
        ("novelty", features.novelty, 2),
        ("convention_sensitivity", features.convention_sensitivity, 2),
        ("literature_uncertainty", features.literature_uncertainty, 2),
        ("coupling", features.coupling, 2),
        ("creative_search", features.creative_search, 2),
        ("mathematical_depth", features.mathematical_depth, 3),
        ("ambiguity", features.ambiguity, 3),
    )
    escalations = [f"{name}>={minimum}" for name, value, minimum in deep_features if value >= minimum]
    if features.consequence >= 2 and features.verification_strength <= 1:
        escalations.append("consequence>=2+verification_strength<=1")
    if escalations and _rank(floor) < _rank("science_deep"):
        floor = "science_deep"
        reasons.extend(escalations)
    elif escalations:
        reasons.extend(escalations)

    if profile:
        selected = profiles.get(profile)
        if selected is None:
            raise ValueError(f"Unknown model profile: {profile}")
        if _rank(selected.capability) < _rank(floor):
            raise ValueError(f"Profile {profile!r} does not meet required capability {floor}")
        reasons.append("profile_override")
    else:
        eligible = [item for item in profiles.values() if _rank(item.capability) >= _rank(floor)]
        if not eligible:
            raise ValueError(f"No configured profile meets required capability {floor}")
        selected = min(eligible, key=lambda item: (_rank(item.capability), item.name))
    explanation = f"{role} requires {floor}; selected {selected.name} ({selected.capability})"
    return RouteDecision(selected, features, floor, tuple(reasons), explanation)
