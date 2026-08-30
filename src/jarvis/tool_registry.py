from __future__ import annotations

import importlib.metadata
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

import yaml


class ToolRegistryError(ValueError):
    """Raised when the committed scientific-tool registry is malformed."""


_REGISTRY_VERSIONS = {1, 2}


def _string_list(value: object, field: str, tool_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ToolRegistryError(f"Tool {tool_id!r} requires a non-empty string list for {field}")
    if len(set(value)) != len(value):
        raise ToolRegistryError(f"Tool {tool_id!r} repeats a {field} value")
    return list(value)


def _normalize_tool(entry: object, version: int) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ToolRegistryError("Each tool registry entry must be a mapping")
    item = dict(entry)
    tool_id = item.get("id")
    if not isinstance(tool_id, str) or not tool_id:
        raise ToolRegistryError("Each tool registry entry requires a non-empty id")
    executable = item.get("executable")
    if not isinstance(executable, str) or not executable:
        raise ToolRegistryError(f"Tool {tool_id!r} requires a non-empty executable")
    if version == 1:
        item.setdefault("capabilities", [])
        item.setdefault("domains", [])
        item.setdefault("execution", {"environment": item.get("ecosystem", "unknown")})
        item.setdefault("verification", {"strength": "unknown", "templates": []})
    item["capabilities"] = _string_list(item["capabilities"], "capabilities", tool_id)
    item["domains"] = _string_list(item["domains"], "domains", tool_id)
    execution = item.get("execution")
    if not isinstance(execution, dict) or not isinstance(execution.get("environment"), str):
        raise ToolRegistryError(f"Tool {tool_id!r} requires execution.environment")
    verification = item.get("verification")
    if not isinstance(verification, dict):
        raise ToolRegistryError(f"Tool {tool_id!r} requires verification metadata")
    strength = verification.get("strength")
    if strength not in {"low", "medium", "high", "unknown"}:
        raise ToolRegistryError(f"Tool {tool_id!r} has invalid verification strength")
    templates = _string_list(verification.get("templates"), "verification.templates", tool_id)
    item["execution"] = dict(execution)
    item["verification"] = {"strength": strength, "templates": templates}
    return item


def load_tool_registry(root: Path) -> list[dict[str, Any]]:
    """Load a versioned capability registry without probing the host runtime."""
    path = root / "packages" / "registry.yaml"
    try:
        registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ToolRegistryError(f"Could not read tool registry: {path}") from exc
    if not isinstance(registry, dict) or registry.get("version") not in _REGISTRY_VERSIONS:
        raise ToolRegistryError("Tool registry requires supported integer version 1 or 2")
    entries = registry.get("tools")
    if not isinstance(entries, list):
        raise ToolRegistryError("Tool registry requires a tools list")
    tools = [_normalize_tool(entry, registry["version"]) for entry in entries]
    ids = [tool["id"] for tool in tools]
    if len(set(ids)) != len(ids):
        raise ToolRegistryError("Tool registry contains duplicate ids")
    return tools


def tool_status(root: Path) -> list[dict[str, Any]]:
    """Return package diagnostics while retaining normalized registry metadata."""
    tools = []
    application_roots = [
        Path(os.environ["JARVIS_WOLFRAM_APPLICATIONS"]).expanduser()
        if os.getenv("JARVIS_WOLFRAM_APPLICATIONS")
        else None,
        Path.home() / ".Wolfram" / "Applications",
        Path.home() / ".Mathematica" / "Applications",
    ]
    application_roots = [path for path in application_roots if path and path.is_dir()]
    wolfram_runtime_ok = False
    for entry in load_tool_registry(root):
        item = dict(entry)
        executable = "python" if entry["id"] == "python" else entry["executable"]
        item["path"] = sys.executable if executable == "python" else shutil.which(executable)
        item["status"] = "available" if item["path"] else "missing"
        if entry["id"] == "python":
            item["version"] = sys.version.split()[0]
            try:
                item["package_version"] = importlib.metadata.version(entry["package"])
            except importlib.metadata.PackageNotFoundError:
                item["status"] = "missing-package"
        elif entry.get("marker"):
            marker = next(
                (
                    base / entry["marker"]
                    for base in application_roots
                    if (base / entry["marker"]).is_file()
                ),
                None,
            )
            item["path"] = str(marker) if marker else None
            item["status"] = "available" if marker else "missing-package"
            if marker and entry.get("version_file"):
                version_file = next(
                    (
                        base / entry["version_file"]
                        for base in application_roots
                        if (base / entry["version_file"]).is_file()
                    ),
                    None,
                )
                if version_file:
                    item["version"] = version_file.read_text(encoding="utf-8").strip()
            elif marker and entry.get("version_regex"):
                match = re.search(
                    entry["version_regex"], marker.read_text(encoding="utf-8", errors="ignore")
                )
                if match:
                    item["version"] = match.group(1)
            if marker and not wolfram_runtime_ok:
                item["status"] = "blocked-runtime"
        elif item["path"] and entry.get("version_args"):
            version = subprocess.run(
                [item["path"], *entry["version_args"]],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            item["version"] = (version.stdout or version.stderr).strip()
            try:
                smoke = subprocess.run(
                    [item["path"], "-code", "Print[2+2]"],
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=False,
                )
                wolfram_runtime_ok = smoke.returncode == 0 and "4" in smoke.stdout
                diagnostic = smoke.stderr
            except subprocess.TimeoutExpired:
                diagnostic = "Wolfram kernel smoke test timed out"
            if not wolfram_runtime_ok:
                item["status"] = "broken"
                item["diagnostic"] = (diagnostic or "Wolfram kernel smoke test failed").strip()
        tools.append(item)
    return tools


def select_tools(
    root: Path,
    capabilities: Iterable[str],
    *,
    status_provider: Callable[[Path], list[dict[str, Any]]] = tool_status,
) -> list[dict[str, Any]]:
    """Select available registered tools matching any requested capability."""
    requested = list(dict.fromkeys(capabilities))
    if not requested or not all(
        isinstance(capability, str) and capability for capability in requested
    ):
        raise ValueError("At least one non-empty capability is required")
    selected = []
    for tool in status_provider(root):
        matched = [capability for capability in requested if capability in tool["capabilities"]]
        if matched and tool["status"] == "available":
            selected.append({**tool, "matched_capabilities": matched})
    return selected
