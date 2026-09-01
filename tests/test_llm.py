from types import SimpleNamespace

from jarvis import answering, llm


def _response(text="answer", usage=None, response_ms=None):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))],
        usage=usage,
        response_ms=response_ms,
    )


def test_complete_result_collects_response_telemetry(monkeypatch):
    monkeypatch.setattr(
        llm,
        "completion",
        lambda **_: _response(
            usage=SimpleNamespace(prompt_tokens=2, completion_tokens=3, total_tokens=5),
            response_ms=12.5,
        ),
    )

    result = llm.complete_result("openai/gpt-5.6", "system", "user")

    assert result.provider == "openai"
    assert result.model == "openai/gpt-5.6"
    assert result.text == "answer"
    assert result.usage == {"prompt_tokens": 2, "completion_tokens": 3, "total_tokens": 5}
    assert result.latency_ms == 12.5


def test_complete_keeps_text_api_without_usage(monkeypatch):
    monkeypatch.setattr(llm, "completion", lambda **_: _response(usage=None))

    result = llm.complete_result("model", "system", "user")

    assert result.provider == "unknown"
    assert result.usage is None
    assert result.latency_ms is not None
    assert llm.complete("model", "system", "user") == "answer"


def test_answer_question_passes_research_intent_gate_to_model(monkeypatch):
    captured = {}
    expected = llm.CompletionResult("test", "model", "answer")

    monkeypatch.setattr(answering, "retrieve_hits", lambda *args, **kwargs: [])
    monkeypatch.setattr(
        answering,
        "complete_result",
        lambda model, system, prompt: (
            captured.update(model=model, system=system, prompt=prompt) or expected
        ),
    )

    config = SimpleNamespace(assistant=SimpleNamespace(max_context_chunks=3))
    result, hits = answering.answer_question(config, "What is the result?", "model")

    assert result is expected
    assert hits == []
    assert captured["model"] == "model"
    assert "QUESTION:\nWhat is the result?" in captured["prompt"]
    instruction = " ".join(captured["system"].split())
    assert "research intent" in instruction
    assert "do not present a source formula as independently verified" in instruction
