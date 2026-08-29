from __future__ import annotations

from .config import Config
from .llm import CompletionResult, complete_result
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
) -> tuple[CompletionResult, list]:
    hits = retrieve_hits(
        config,
        question,
        limit=config.assistant.max_context_chunks,
    )
    return complete_result(model, SYSTEM_PROMPT, render_retrieval_prompt(question, hits)), hits
