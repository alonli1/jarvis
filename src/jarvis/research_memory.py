from __future__ import annotations

import json
from pathlib import Path

from .workflows import load_manifest


def build_research_memory(root: Path) -> list[dict]:
    """Index persisted claim state without altering runs or inferring new claims."""
    runs = root / ".jarvis" / "runs"
    records = []
    if not runs.is_dir():
        return records
    for path in sorted(runs.iterdir()):
        manifest_path = path / "manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = load_manifest(manifest_path)
        for claim in manifest["claims"]:
            records.append(
                {
                    "run_id": manifest["id"],
                    "claim_id": claim["id"],
                    "statement": claim["statement"],
                    "status": claim["status"],
                    "kind": claim["kind"],
                    "conventions": claim.get("conventions", {}),
                    "verification_ids": [
                        record["id"]
                        for record in manifest["verification"]
                        if record.get("claim_id") == claim["id"]
                    ],
                }
            )
    return records


def write_research_memory(root: Path, output: Path | None = None) -> Path:
    target = output or root / ".jarvis" / "research-memory.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(build_research_memory(root), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return target
