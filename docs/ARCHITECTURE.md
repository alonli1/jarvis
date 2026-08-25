# Jarvis v1 architecture

## Design invariants

1. **The corpus is independent of the LLM.** Switching the reasoning model must not require rebuilding scientific knowledge.
2. **Retrieval models are pinned.** All researchers should query the same vector/sparse representation unless the group deliberately migrates it.
3. **The corpus has one access class.** Every indexed document can be retrieved by every configured model and MCP client.
4. **Novelty monitoring operates on claims, not whole-paper similarity.** Each manuscript keeps narrow, machine-readable claims in `novelty.yaml`.
5. **Literature sources are adapters.** arXiv, INSPIRE, OpenAlex, Semantic Scholar, and future sources expose one common record type.
6. **A novelty alert is triage.** The system ranks possible overlap and explains the signal; researchers make the scientific judgment.

## Query path

```text
question
  -> dense + sparse query embeddings
  -> Qdrant RRF hybrid retrieval
  -> top-k passages with source/page metadata
  -> LiteLLM-selected reasoning model
  -> answer with [S1], [S2], ... citations
```

## Ingestion path

```text
PDF / TeX / Markdown / text
  -> sidecar metadata
  -> parser
  -> chunks
  -> pinned dense embedding
  -> pinned sparse embedding
  -> Qdrant payload + vectors
```

The source file remains authoritative. The vector database is generated state and is intentionally ignored by Git.

## Novelty-watch path

```text
novelty.yaml claim
  -> claim-specific search queries
  -> arXiv / INSPIRE / OpenAlex / Semantic Scholar
  -> source normalization + DOI/arXiv deduplication
  -> deterministic overlap score
  -> medium/high/critical candidates
  -> optional LLM adjudication for high-risk candidates
  -> Markdown report
  -> GitHub Action commit + issue
```

## Access model

Jarvis does not classify documents or filter retrieval by access tier. A model selected through
the CLI and an agent connected through MCP can receive any indexed passage. Repository membership,
the shared-storage account, and provider account settings are the access boundaries.

## Why Qdrant local mode first

Local mode makes the repository useful to a single researcher without operating infrastructure. The same application interface can move to a shared Qdrant server by changing `assistant.toml`, so the group can centralize the index later without rewriting the assistant.

## Why the deterministic novelty scorer exists even with LLMs

The literature watch should still work when:

- an API key is unavailable;
- an LLM provider is down;
- the group does not want an unpublished claim sent to an external provider;
- reproducibility matters.

The LLM judge is therefore optional and only refines already flagged candidates.

## v2 technical direction

The most important upgrades are equation-aware LaTeX parsing, structured scientific PDF ingestion, citation-neighborhood expansion, a scholarly knowledge graph, and an evaluation benchmark made from real group questions.
