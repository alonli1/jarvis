from typer.testing import CliRunner

from jarvis import cli
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
