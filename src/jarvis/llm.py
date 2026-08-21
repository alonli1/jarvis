from __future__ import annotations

from litellm import completion


def complete(model: str, system: str, user: str, temperature: float = 0.1) -> str:
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
