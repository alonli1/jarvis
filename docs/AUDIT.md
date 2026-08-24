# Jarvis implementation audit

Audited 2026-08-25 against `README.md`, `docs/ARCHITECTURE.md`, and commit
`10879cc`. This audit describes the working tree after the two Phase 0 privacy fixes listed
below. The attached roadmap's 2026-08-22 inventory is a historical snapshot, not the current
repository state.

## Verification

| Check | Result |
|---|---|
| Source review | All 26 Python modules under `src/jarvis/` read against the documentation |
| Runtime install | `uv sync` succeeds with uv 0.12.5 and Python 3.14.4 |
| Diagnostics | `uv run jarvis doctor` passes all four repository-folder checks |
| Tests | `uv sync --extra dev`; `uv run pytest -q`: 28 passed |
| Coverage | 63%; weakest areas are the live adapters, CLI, novelty orchestration, and index integration |
| Real retrieval smoke test | Existing local index returned three cited PDF passages for a gravity-EFT query |
| Lint | Not clean: 22 pre-existing Ruff findings, mainly import ordering, timezone-aware dates, Typer `B008`, and two intentional broad exception boundaries |

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
| Dropbox | No connector, canonical layout, sync script, or Dropbox metadata fields exist |
| Symbolic packages | No `packages/` registry exists |
| Symbolic execution | No `workbench/` or provenance format exists |
| Predictions | No numeric evaluation or theory-to-prediction pipeline exists |

The PDFs make this installation useful locally, but they do not satisfy Phase 1's durable,
shared-library goal. Dropbox (or another approved private store) is still needed for lawful,
portable access to non-redistributable material.

## Capability audit

| Documented capability | Status | Evidence and limits |
|---|---|---|
| PDF/TeX/Markdown/text/manifest ingestion | Implemented | Parsers, stable chunk IDs, sidecars, and per-page PDF chunks exist. PDF quality still depends on the text layer. |
| Hybrid Qdrant retrieval | Implemented and smoke-tested | Dense and sparse FastEmbed vectors are fused with RRF. Missing files are not pruned automatically from an existing index. |
| Source citations | Partially enforced | Retrieval emits stable `[S1]` records with paths/pages. LLM output is instructed, but not validated, to cite them. |
| Model selection | Implemented, not live-tested | LiteLLM receives the configured or per-command model. No provider/API call was made during this audit. |
| Web-subscription workflow | Implemented | `jarvis retrieve` produces a pasteable, cited prompt without calling an LLM. |
| Visibility policy | Implemented with Phase 0 fix | External models default to public; local prefixes may receive confidential data. Qdrant now filters visibility before ranking, and external private-context use is logged locally before transmission. Provider-specific approval policy is not implemented. |
| MCP | Implemented and tested | Retrieval plus five graph tools are exposed; workspace and global Antigravity configurations exist. |
| Literature adapters | Implemented, not integration-tested | arXiv, INSPIRE, OpenAlex, and Semantic Scholar adapters normalize records. Live services, rate limits, and API changes remain outside unit coverage. |
| Novelty triage | Implemented, placeholder-only | Claim parsing, deterministic lexical scoring, risk thresholds, optional LLM review, and reports exist. There are no real group claims to evaluate. |
| Citation graph | Implemented and tested | Direct citations, bibliographic coupling, topic similarity, manuscript relevance, MCP queries, static views, and the live local application exist. |
| Daily GitHub workflow | Defined, not run here | The workflow installs Jarvis, runs the watch, commits a report, and creates an issue. It creates new issues; it does not update an existing one. |
| Shared Qdrant | Configurable, not deployed | Server mode and Docker Compose exist. The image is `latest`, not version-pinned, and access control is not configured. |

## Documentation corrections made

- The README no longer says the workflow updates an existing GitHub issue; the workflow only
  creates one.
- The novelty description now states that the date window filters discovery while
  publication/source metadata is reported rather than included in the overlap score.

## Phase 0 fixes made

1. Visibility is now included in the Qdrant query filter. Previously Jarvis retrieved a mixed
   candidate set and removed private hits afterward. It did not return private text, but a
   private-heavy candidate set could crowd out relevant public results.
2. When an external model is explicitly allowed to receive retrieved group/confidential
   passages, Jarvis writes an append-only event to `.jarvis/privacy-audit.jsonl` before the
   model call. It records model, source paths, visibility, and timestamp, but not the prompt.
3. Regression tests cover both changes.

## Known gaps to resolve before later phases

- Retrieval model names are configured, but exact model artifact revisions are not pinned.
- Index replacement deletes a source before its replacement chunks are fully upserted, and a
  directory re-ingest does not prune records for files that disappeared.
- Sidecar visibility values are not validated during ingestion; malformed values fail later at
  query time.
- LLM answers have no post-generation citation validator.
- Network adapters and the end-to-end novelty watch lack deterministic integration fixtures.
- CI tests one runner-selected Python version rather than a declared supported-version matrix.
- The local graph server has no authentication; documentation correctly limits it to localhost.
- Qdrant server mode has no authentication/TLS configuration in this repository.

These are recorded rather than silently expanded into Phase 1+ work. The next roadmap gate is a
human decision about Dropbox access, layout, and default visibility before implementing a sync
fallback.
