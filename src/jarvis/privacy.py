from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .config import Config


def is_local_model(model: str, config: Config) -> bool:
    return any(model.startswith(prefix) for prefix in config.privacy.local_model_prefixes)


def max_visibility_for_model(model: str, allow_private: bool, config: Config) -> str:
    if allow_private:
        return "confidential"
    if is_local_model(model, config):
        return config.privacy.local_default_max_visibility
    return config.privacy.external_default_max_visibility


def log_external_private_access(
    root: Path, model: str, sources: list[tuple[str, str]]
) -> Path:
    """Record external-provider access before private context is sent."""
    path = root / ".jarvis" / "privacy-audit.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event": "external_private_context_authorized",
        "model": model,
        "sources": [
            {"source_path": source_path, "visibility": visibility}
            for source_path, visibility in sources
        ],
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, separators=(",", ":")) + "\n")
    return path
