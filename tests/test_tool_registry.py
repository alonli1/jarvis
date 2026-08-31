from pathlib import Path

import pytest

from jarvis.tool_registry import (
    ToolRegistryError,
    check_templates_for_tools,
    load_tool_registry,
    select_tools,
    wolfram_package_loads,
)


def write_registry(root: Path, text: str) -> None:
    path = root / "packages" / "registry.yaml"
    path.parent.mkdir(exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_v1_registry_is_normalized_for_existing_clones(tmp_path):
    write_registry(
        tmp_path,
        """version: 1
tools:
  - id: legacy
    executable: legacy-bin
    ecosystem: legacy
""",
    )

    tool = load_tool_registry(tmp_path)[0]

    assert tool["capabilities"] == []
    assert tool["domains"] == []
    assert tool["execution"] == {"environment": "legacy"}
    assert tool["verification"] == {"strength": "unknown", "templates": []}


def test_v2_registry_requires_capability_and_verification_metadata(tmp_path):
    write_registry(
        tmp_path,
        """version: 2
tools:
  - id: complete
    executable: tool
    capabilities: [tensor_algebra]
    domains: [GR]
    execution: {environment: wolfram}
    verification: {strength: high, templates: []}
""",
    )
    assert load_tool_registry(tmp_path)[0]["capabilities"] == ["tensor_algebra"]

    write_registry(
        tmp_path,
        """version: 2
tools:
  - id: duplicate
    executable: tool
    capabilities: [tensor_algebra, tensor_algebra]
    domains: [GR]
    execution: {environment: wolfram}
    verification: {strength: high, templates: [flat_limit]}
""",
    )
    with pytest.raises(ToolRegistryError, match="repeats a capabilities"):
        load_tool_registry(tmp_path)


def test_registry_rejects_duplicate_ids(tmp_path):
    write_registry(
        tmp_path,
        """version: 1
tools:
  - id: duplicate
    executable: one
  - id: duplicate
    executable: two
""",
    )
    with pytest.raises(ToolRegistryError, match="duplicate ids"):
        load_tool_registry(tmp_path)


def test_selection_is_capability_specific_and_excludes_unavailable_tools(tmp_path):
    status = lambda _: [
        {
            "id": "xact",
            "capabilities": ["tensor_algebra", "curvature"],
            "status": "blocked-runtime",
        },
        {"id": "sympy", "capabilities": ["symbolic_algebra"], "status": "available"},
        {"id": "feyncalc", "capabilities": ["dirac_algebra"], "status": "available"},
    ]

    selected = select_tools(tmp_path, ["dirac_algebra", "symbolic_algebra"], status_provider=status)

    assert [tool["id"] for tool in selected] == ["sympy", "feyncalc"]
    assert selected[0]["matched_capabilities"] == ["symbolic_algebra"]
    assert all(tool["id"] != "xact" for tool in selected)
    assert select_tools(tmp_path, ["curvature"], status_provider=status) == []
    with pytest.raises(ValueError, match="non-empty capability"):
        select_tools(tmp_path, [], status_provider=status)


def test_declared_checks_and_wolfram_loads_are_tool_attributed():
    tool = {
        "id": "feyncalc",
        "execution": {"environment": "wolfram", "package": "FeynCalc`"},
        "verification": {"templates": ["ward_identity"]},
    }

    assert check_templates_for_tools([tool]) == [
        {
            "tool_id": "feyncalc",
            "template": "ward_identity",
            "instruction": "Check the applicable Ward identity or gauge-invariance condition.",
        }
    ]
    assert wolfram_package_loads([tool]) == ['Needs["FeynCalc`"];']
    tool["execution"]["package"] = "bad;name"
    with pytest.raises(ToolRegistryError, match="invalid Wolfram package"):
        wolfram_package_loads([tool])


def test_marker_loaded_wolfram_packages_require_an_available_marker(tmp_path):
    marker = tmp_path / "FIRE7.m"
    marker.write_text("", encoding="utf-8")
    tool = {
        "id": "fire7",
        "path": str(marker),
        "execution": {"environment": "wolfram", "package": "FIRE`", "loader": "marker"},
        "verification": {"templates": []},
    }

    assert wolfram_package_loads([tool]) == [f'Get["{marker}"];']
    marker.unlink()
    with pytest.raises(ToolRegistryError, match="available package marker"):
        wolfram_package_loads([tool])
