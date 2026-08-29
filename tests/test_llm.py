from types import SimpleNamespace

from jarvis import llm


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
