# Jarvis implementation audit

> Historical Phase 0 snapshot. See [ARCHITECTURE.md](ARCHITECTURE.md) and
> [ROADMAP.md](ROADMAP.md) for the current harness, Dropbox, skills, and computation design.

Audited 2026-08-25 against `README.md`, `docs/ARCHITECTURE.md`, and commit
`10879cc`. This audit describes the working tree after the Phase 0 implementation work listed
below. The attached roadmap's 2026-08-22 inventory is a historical snapshot, not the current
repository state.

## Verification

| Check | Result |
|---|---|
| Source review | All 26 Python modules under `src/jarvis/` read against the documentation |
| Runtime install | `uv sync` succeeds with uv 0.12.5 and Python 3.14.4 |
| Diagnostics | `uv run jarvis doctor` passes all four repository-folder checks |
| Tests | `uv sync --extra dev`; `uv run pytest -q`: 28 passed |
| Coverage | 66%; weakest areas are the live adapters, CLI, novelty orchestration, and index integration |
| Real retrieval smoke test | Existing local index returned three cited PDF passages for a gravity-EFT query |
| Provider sync smoke test | The Dropbox-backed UOLEA PDF was synced, indexed into 36 chunks, and retrieved with citations to pages 1 and 13 |
| Lint | Not clean: 19 pre-existing Ruff findings, mainly import ordering, timezone-aware dates, Typer `B008`, and two intentional broad exception boundaries |

`uv sync` installs runtime dependencies only because test tools are an optional `dev` extra.
Use `uv sync --extra dev` before running the test suite.

The LiteLLM import attempted to refresh its public model-price map during diagnostics; offline
fallback worked. ONNX telemetry could not persist a device identifier in the sandbox and used
an in-memory identifier. Neither warning affected the checks.

## Current repository state

| Area | Observed state |
|---|---|
| Curated manifest | 75 references in `knowledge/references.yaml` |
| Local literature | 68 paper PDFs and 7 book PDFs, each with sidecar metadata |
| Git portability | PDFs are intentionally ignored and none are tracked; a fresh clone receives metadata, not the 75 local files |
| Retrieval index | Local Qdrant index exists and answers real PDF queries |
| Citation/relationship graph | Cached graph has 76 nodes and 611 edges |
| Manuscripts | Only `example_project`; its claim is still a placeholder |
| Shared storage | Dropbox library bootstrapped with 75 documents in category-based folders |
| Symbolic packages | No `packages/` registry exists |
| Symbolic execution | No `workbench/` or provenance format exists |
| Predictions | No numeric evaluation or theory-to-prediction pipeline exists |

The 75 local documents now have canonical Dropbox copies organized by category. Dropbox client
sync status remains an external operational concern; Jarvis verified the local Dropbox tree
byte-for-byte against this clone.

## Capability audit

| Documented capability | Status | Evidence and limits |
|---|---|---|
| PDF/TeX/Markdown/text/manifest ingestion | Implemented | Parsers, stable chunk IDs, sidecars, and per-page PDF chunks exist. PDF quality still depends on the text layer. |
| Hybrid Qdrant retrieval | Implemented and smoke-tested | Dense and sparse FastEmbed vectors are fused with RRF. Missing files are not pruned automatically from an existing index. |
| Source citations | Partially enforced | Retrieval emits stable `[S1]` records with paths/pages. LLM output is instructed, but not validated, to cite them. |
| Model selection | Implemented, not live-tested | LiteLLM receives the configured or per-command model. No provider/API call was made during this audit. |
| Web-subscription workflow | Implemented | `jarvis retrieve` produces a pasteable, cited prompt without calling an LLM. |
| Uniform corpus access | Implemented | CLI models and MCP clients search the same complete corpus. Access is controlled through repository, shared-storage, and model-account membership. |
| MCP | Implemented and tested | Retrieval plus five graph tools are exposed; workspace and global Antigravity configurations exist. |
| Literature adapters | Implemented, locally tested | arXiv, INSPIRE, OpenAlex, and Semantic Scholar adapters normalize records. Live services and rate limits remain outside deterministic coverage; provider failures are reported as partial coverage. |
| Novelty triage | Implemented, placeholder-only | Claim parsing, deterministic lexical scoring, risk thresholds, optional LLM review, and reports exist. There are no real group claims to evaluate. |
| Citation graph | Implemented and tested | Direct citations, bibliographic coupling, topic similarity, manuscript relevance, MCP queries, static views, and the live local application exist. |
| Literature surveillance | Skill-owned and on demand | `literature-understanding` defines report review. A manual GitHub workflow can commit a report but never creates an issue. |
| Shared Qdrant | Configurable, not deployed | Server mode and Docker Compose exist. The image is `latest`, not version-pinned, and access control is not configured. |

## Documentation corrections made

- Literature surveillance is an on-demand `literature-understanding` mode; automatic scheduling
  and issue creation were removed.
- The novelty description now states that the date window filters discovery while
  publication/source metadata is reported rather than included in the overlap score.

## Phase 0 access decision

The group removed document access tiers. Jarvis now treats every indexed document uniformly;
there are no per-document classifications, retrieval filters, CLI overrides, or MCP environment
settings for tiered access.

## Known gaps to resolve before later phases

- Retrieval model names are configured, but exact model artifact revisions are not pinned.
- Index replacement deletes a source before its replacement chunks are fully upserted, and a
  directory re-ingest does not prune records for files that disappeared.
- LLM answers have no post-generation citation validator.
- Network adapters and the end-to-end novelty watch lack deterministic integration fixtures.
- CI tests one runner-selected Python version rather than a declared supported-version matrix.
- The local graph server has no authentication; documentation correctly limits it to localhost.
- Qdrant server mode has no authentication/TLS configuration in this repository.

These are recorded rather than silently expanded into later-phase work. Phase 1's first-paper
gate is complete; Phase 2 starts by identifying the symbolic packages the group actually uses.
