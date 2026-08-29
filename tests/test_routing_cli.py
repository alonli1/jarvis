import json

from typer.testing import CliRunner

from jarvis import cli
from jarvis.config import ModelProfile


def test_route_dry_run_emits_sorted_json_without_model_call(monkeypatch):
    config = type(
        "Config",
        (),
        {
            "assistant": type(
                "Assistant",
                (),
                {
                    "profiles": {
                        "fast": ModelProfile("fast", "openai", "openai/gpt", "science_fast"),
                        "deep": ModelProfile("deep", "openai", "openai/gpt", "science_deep"),
                    }
                },
            )
        },
    )()
    monkeypatch.setattr(cli, "load_config", lambda: config)

    result = CliRunner().invoke(
        cli.app, ["route", "question", "--role", "retrieval", "--novelty", "2", "--dry-run"]
    )

    assert result.exit_code == 0
    assert result.output == json.dumps(json.loads(result.output), sort_keys=True) + "\n"
    assert json.loads(result.output)["profile"]["name"] == "deep"


def test_route_rejects_unknown_profile(monkeypatch):
    config = type("Config", (), {"assistant": type("Assistant", (), {"profiles": {}})})()
    monkeypatch.setattr(cli, "load_config", lambda: config)

    result = CliRunner().invoke(cli.app, ["route", "question", "--role", "retrieval", "--profile", "missing", "--dry-run"])

    assert result.exit_code != 0
    assert "Unknown model profile: missing" in result.output
