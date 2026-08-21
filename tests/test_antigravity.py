import json

import pytest

from jarvis.antigravity import install_global_mcp


def test_install_global_mcp_uses_current_clone_and_preserves_servers(tmp_path, monkeypatch):
    clone = tmp_path / "a different clone" / "jarvis"
    clone.mkdir(parents=True)
    config = tmp_path / "mcp_config.json"
    config.write_text(json.dumps({"mcpServers": {"existing": {"command": "example"}}}))
    monkeypatch.setattr("jarvis.antigravity.shutil.which", lambda command: "/tools/uv")

    install_global_mcp(clone, config)

    servers = json.loads(config.read_text())["mcpServers"]
    assert servers["existing"] == {"command": "example"}
    assert servers["jarvis"]["command"] == "/tools/uv"
    assert servers["jarvis"]["args"] == [
        "run",
        "--directory",
        str(clone.resolve()),
        "jarvis-mcp",
    ]


def test_install_global_mcp_does_not_overwrite_invalid_json(tmp_path, monkeypatch):
    config = tmp_path / "mcp_config.json"
    config.write_text("not json")
    monkeypatch.setattr("jarvis.antigravity.shutil.which", lambda command: "/tools/uv")

    with pytest.raises(json.JSONDecodeError):
        install_global_mcp(tmp_path, config)

    assert config.read_text() == "not json"
