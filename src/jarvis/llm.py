from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from litellm import completion


@dataclass(frozen=True)
class CompletionResult:
    provider: str
    model: str
    text: str
    usage: dict[str, int] | None = None
    latency_ms: float | None = None


def _usage_values(usage: object | None) -> dict[str, int] | None:
    if usage is None:
        return None
    values = {
        key: (usage.get(key) if isinstance(usage, dict) else getattr(usage, key, None))
        for key in ("prompt_tokens", "completion_tokens", "total_tokens")
    }
    present = {key: value for key, value in values.items() if isinstance(value, int)}
    return present or None


def complete_result(
    model: str, system: str, user: str, temperature: float = 0.1
) -> CompletionResult:
    started = perf_counter()
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    response_latency = getattr(response, "response_ms", None)
    latency_ms = response_latency if isinstance(response_latency, (int, float)) else None
    if latency_ms is None:
        latency_ms = (perf_counter() - started) * 1000
    return CompletionResult(
        provider=model.split("/", 1)[0] if "/" in model else "unknown",
        model=model,
        text=response.choices[0].message.content or "",
        usage=_usage_values(getattr(response, "usage", None)),
        latency_ms=latency_ms,
    )


def complete(model: str, system: str, user: str, temperature: float = 0.1) -> str:
    return complete_result(model, system, user, temperature).text
