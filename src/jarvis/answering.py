from __future__ import annotations

from .config import Config
from .index import HybridIndex
from .llm import complete
from .privacy import max_visibility_for_model


SYSTEM_PROMPT = """You are a careful scientific research assistant for theoretical physics.
Use the supplied sources as evidence. Distinguish sourced statements from your own reasoning.
Do not invent papers, equations, page numbers, or citations. Cite retrieved sources using [S1], [S2], ...
If the sources are insufficient, say so clearly. Preserve mathematical notation where possible.
"""


def answer_question(
    config: Config,
    question: str,
    model: str,
    allow_private: bool = False,
) -> tuple[str, list]:
    max_visibility = max_visibility_for_model(model, allow_private, config)
    index = HybridIndex(config)
    hits = index.search(question, k=config.assistant.max_context_chunks, max_visibility=max_visibility)
    context_parts = []
    for i, hit in enumerate(hits, start=1):
        c = hit.chunk
        where = c.source_path
        if c.page:
            where += f", p. {c.page}"
        context_parts.append(f"[S{i}] {where}\n{c.text}")
    context = "\n\n".join(context_parts) if context_parts else "No local sources were retrieved."
    user = f"QUESTION:\n{question}\n\nRETRIEVED SOURCES:\n{context}"
    return complete(model, SYSTEM_PROMPT, user), hits
