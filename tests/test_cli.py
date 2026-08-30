from typer.testing import CliRunner

from jarvis import answering, cli
from jarvis.config import ModelProfile
from jarvis.llm import CompletionResult
from jarvis.models import Chunk, SearchHit


def test_retrieve_command_prints_pasteable_sources(monkeypatch):
    hit = SearchHit(
        chunk=Chunk(
            id="chunk-1",
            text="Retrieved evidence.",
            source_path="knowledge/notes/example.md",
        ),
        score=0.8,
    )
    monkeypatch.setattr(cli, "retrieve_hits", lambda *args, **kwargs: [hit])
    result = CliRunner().invoke(cli.app, ["retrieve", "test question"])
    assert result.exit_code == 0
    assert "[S1] knowledge/notes/example.md" in result.stdout
    assert "INSTRUCTIONS:" in result.stdout


def test_ask_selects_profile_and_model_override(monkeypatch):
    selected = []
    profile = ModelProfile(
        name="fast", provider="openai", model="openai/gpt-5.6", capability="science_fast"
    )
    config = type(
        "Config",
        (),
        {
            "assistant": type(
                "Assistant", (), {"default_model": "default", "profiles": {"fast": profile}}
            )
        },
    )()
    monkeypatch.setattr(cli, "load_config", lambda: config)
    monkeypatch.setattr(
        answering,
        "answer_question",
        lambda _config, _question, model: (
            selected.append(model) or CompletionResult("x", model, "answer"),
            [],
        ),
    )

    runner = CliRunner()
    assert runner.invoke(cli.app, ["ask", "question", "--profile", "fast"]).exit_code == 0
    assert (
        runner.invoke(
            cli.app, ["ask", "question", "--profile", "fast", "--model", "manual/model"]
        ).exit_code
        == 0
    )
    assert selected == ["openai/gpt-5.6", "manual/model"]


def test_ask_rejects_unknown_profile(monkeypatch):
    config = type(
        "Config",
        (),
        {"assistant": type("Assistant", (), {"default_model": "default", "profiles": {}})},
    )()
    monkeypatch.setattr(cli, "load_config", lambda: config)

    result = CliRunner().invoke(cli.app, ["ask", "question", "--profile", "missing"])

    assert result.exit_code != 0
    assert "Unknown model profile: missing" in result.output


def test_computation_command_passes_requested_capabilities(monkeypatch):
    captured = {}
    bundle = type("Bundle", (), {"id": "run-1", "path": "/tmp/run-1"})()
    monkeypatch.setattr(cli, "load_config", lambda: object())
    monkeypatch.setattr(
        cli,
        "prepare_computation",
        lambda config, task, engine, capability: (
            captured.update(
                {"config": config, "task": task, "engine": engine, "capability": capability}
            )
            or bundle
        ),
    )

    result = CliRunner().invoke(
        cli.app,
        [
            "run",
            "computation",
            "--task",
            "Check a tensor identity",
            "--capability",
            "tensor_algebra",
            "--capability",
            "curvature",
        ],
    )

    assert result.exit_code == 0
    assert captured["engine"] == "auto"
    assert captured["capability"] == ["tensor_algebra", "curvature"]
