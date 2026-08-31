from __future__ import annotations

from dataclasses import dataclass

from .config import ModelProfile
from .routing import CAPABILITIES


@dataclass(frozen=True)
class CalibrationCase:
    id: str
    required_capability: str


@dataclass(frozen=True)
class ProfileCalibration:
    case_id: str
    profile: str
    provider: str
    model: str
    compatible: bool


def _rank(capability: str) -> int:
    return CAPABILITIES.index(capability)


def calibrate_profiles(
    profiles: dict[str, ModelProfile], cases: list[CalibrationCase]
) -> list[ProfileCalibration]:
    return [
        ProfileCalibration(
            case_id=case.id,
            profile=profile.name,
            provider=profile.provider,
            model=profile.model,
            compatible=_rank(profile.capability) >= _rank(case.required_capability),
        )
        for case in cases
        for profile in profiles.values()
    ]
