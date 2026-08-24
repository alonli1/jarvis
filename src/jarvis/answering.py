from __future__ import annotations

from .config import Config
from .llm import complete
from .models import Visibility
from .privacy import is_local_model, log_external_private_access, max_visibility_for_model
from .retrieval import render_retrieval_prompt, retrieve_hits

SYSTEM_PROMPT = """You are a careful scientific research assistant for theoretical physics.
Use the supplied sources as evidence. Distinguish sourced statements from your own reasoning.
Do not invent papers, equations, page numbers, or citations.
Cite retrieved sources using [S1], [S2], ...
If the sources are insufficient, say so clearly. Preserve mathematical notation where possible.
"""


def answer_question(
    config: Config,
    question: str,
    model: str,
    allow_private: bool = False,
) -> tuple[str, list]:
    max_visibility = max_visibility_for_model(model, allow_private, config)
    hits = retrieve_hits(
        config,
        question,
        limit=config.assistant.max_context_chunks,
        max_visibility=max_visibility,
    )
    private_sources = [
        (hit.chunk.source_path, hit.chunk.visibility)
        for hit in hits
        if Visibility.parse(hit.chunk.visibility) > Visibility.public
    ]
    if private_sources and not is_local_model(model, config):
        log_external_private_access(config.root, model, private_sources)
    return complete(model, SYSTEM_PROMPT, render_retrieval_prompt(question, hits)), hits
