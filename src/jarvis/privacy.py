from __future__ import annotations

from .config import Config


def is_local_model(model: str, config: Config) -> bool:
    return any(model.startswith(prefix) for prefix in config.privacy.local_model_prefixes)


def max_visibility_for_model(model: str, allow_private: bool, config: Config) -> str:
    if allow_private:
        return "confidential"
    if is_local_model(model, config):
        return config.privacy.local_default_max_visibility
    return config.privacy.external_default_max_visibility
