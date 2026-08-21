from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path


def install_global_mcp(repo_root: Path, config_path: Path | None = None) -> Path:
    """Register this clone in Antigravity's global MCP configuration."""
    uv = shutil.which("uv")
    if not uv:
        raise FileNotFoundError("uv is not available in PATH")

    path = config_path or Path.home() / ".gemini" / "config" / "mcp_config.json"
    raw = path.read_text(encoding="utf-8") if path.exists() else ""
    data = json.loads(raw) if raw.strip() else {}
    if not isinstance(data, dict) or not isinstance(data.setdefault("mcpServers", {}), dict):
        raise TypeError(f"Invalid MCP configuration in {path}")

    data["mcpServers"]["jarvis"] = {
        "command": str(Path(uv).resolve()),
        "args": ["run", "--directory", str(repo_root.resolve()), "jarvis-mcp"],
        "env": {"JARVIS_MCP_MAX_VISIBILITY": "public"},
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tmp:
        json.dump(data, tmp, indent=2)
        tmp.write("\n")
        temporary_path = Path(tmp.name)
    os.replace(temporary_path, path)
    return path
