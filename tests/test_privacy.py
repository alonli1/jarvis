import json
from types import SimpleNamespace

from jarvis.answering import answer_question
from jarvis.models import Chunk, SearchHit
from jarvis.privacy import log_external_private_access


def test_external_private_access_is_append_only_and_omits_prompt(tmp_path):
    path = log_external_private_access(
        tmp_path,
        "openai/example",
        [("group/manuscripts/draft.tex", "confidential")],
    )
    log_external_private_access(tmp_path, "anthropic/example", [])

    records = [json.loads(line) for line in path.read_text().splitlines()]
    assert [record["model"] for record in records] == ["openai/example", "anthropic/example"]
    assert records[0]["sources"] == [
        {"source_path": "group/manuscripts/draft.tex", "visibility": "confidential"}
    ]
    assert all("prompt" not in record for record in records)


def test_external_private_answer_is_logged_before_model_call(tmp_path, monkeypatch):
    config = SimpleNamespace(
        root=tmp_path,
        assistant=SimpleNamespace(max_context_chunks=10),
        privacy=SimpleNamespace(
            local_model_prefixes=("ollama/",),
            external_default_max_visibility="public",
            local_default_max_visibility="confidential",
        ),
    )
    hit = SearchHit(
        chunk=Chunk(
            id="private-1",
            text="private context",
            source_path="group/manuscripts/draft.tex",
            visibility="group",
        ),
        score=0.9,
    )
    monkeypatch.setattr("jarvis.answering.retrieve_hits", lambda *args, **kwargs: [hit])

    def complete(*args, **kwargs):
        assert (tmp_path / ".jarvis" / "privacy-audit.jsonl").exists()
        return "cited answer [S1]"

    monkeypatch.setattr("jarvis.answering.complete", complete)

    answer_question(config, "private question", "openai/example", allow_private=True)
