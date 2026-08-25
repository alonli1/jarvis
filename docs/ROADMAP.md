# Jarvis roadmap

This is the standing work order for AI collaborators and researchers working in this
repository. Read the current implementation and [audit](AUDIT.md) before extending it;
the roadmap records direction, while the code records reality.

Updated 2026-08-25.

## Objective

Jarvis should become the group's day-to-day research partner:

1. a persistent, cited knowledge base built from real literature and manuscripts;
2. a registry of the symbolic-computation packages the group actually uses;
3. an executable symbolic workbench with complete provenance;
4. a pipeline from symbolic EFT results to numerical predictions and comparisons;
5. a model-agnostic interface usable from the CLI, web AI providers, and IDE agents.

## Operating principles

- Read the implementation before changing it; documentation can lag code.
- Ground research answers in retrieved passages with `[S1]`, `[S2]`, ... citations.
- Treat the corpus uniformly. Jarvis has no per-document access tiers; repository,
  Dropbox, and model-account membership are the access boundaries.
- Record the package and version, exact input, command, raw output, timestamp, and Git
  commit for every symbolic result.
- Cross-check nontrivial derivations with an independent method where practical.
- Keep changes small, reviewed, tested, and understandable to physicists.
- Ask before destructive operations, directory restructuring, remote pushes, or another
  access-model change.
- Keep researchers responsible for novelty and scientific judgments.

## Current state

| Area | State |
|---|---|
| Implementation | 26 Python modules audited against the documentation |
| Verification | 28 tests pass; `jarvis doctor` passes |
| Literature | 68 papers and 7 books with metadata; 75-reference manifest |
| Shared storage | Dropbox is canonical, using `papers/`, `books/`, `notes/`, and `manuscripts/` |
| Retrieval | Local hybrid Qdrant index contains all 77 discovered sources |
| Graph | 76 nodes and 611 relationships; MCP queries and live browser application work |
| Manuscripts | Only placeholder `example_project`; no real claims yet |
| Symbolic packages | No `packages/` registry yet |
| Symbolic workbench | Not implemented |
| Predictions | Not implemented |

## Phase 0 — Audit: complete

- [x] Audit every `src/jarvis/` module against the README and architecture.
- [x] Install dependencies, run diagnostics and tests, and record results.
- [x] Fix or document mismatches in [AUDIT.md](AUDIT.md).
- [x] Expose retrieval and graph intelligence through MCP.
- [x] Add the live local graph application.

## Phase 1 — Real literature library: operational

- [x] Establish Dropbox as the canonical document store.
- [x] Implement portable pull-only synchronization without committed machine paths.
- [x] Populate Dropbox and the local corpus with 75 documents and sidecars.
- [x] Ingest the real PDFs and verify cited retrieval.
- [x] Add controlled tags, citation relationships, and literature graph views.
- [x] Remove per-document classifications by explicit group decision.
- [ ] Build a benchmark of 15–25 real group questions with expected sources/pages.
- [ ] Measure retrieval and citation quality; tune parsing, chunking, and ranking from evidence.
- [ ] Make index replacement interruption-safe and prune sources removed from the corpus.
- [ ] Pin exact retrieval-model artifact revisions.
- [ ] Validate generated LLM citation labels after completion.

The Phase 1 exit gate is a reproducible benchmark showing that real research questions
retrieve the intended literature with valid citations.

## Phase 2 — Symbolic package registry

Create `packages/registry.yaml` with one entry per tool:

- `id`
- `ecosystem` (`mathematica`, `python`, `julia`, or another runtime)
- `install_method`
- `location`
- `version`
- `purpose`
- `example_invocation`
- `related_topics` using `topics/taxonomy.yaml`
- `status` (`installed`, `not-installed`, or `broken`)

Then:

- [ ] Inventory the packages the group actually uses; do not infer availability.
- [ ] Pin versions and document installation for each ecosystem.
- [ ] Add a minimal executable smoke test for every installed package.
- [ ] Require workbench runs to reference a registry entry.

## Phase 3 — Symbolic research workbench

Create `workbench/<question-or-claim-id>/` for each research question. Each directory
must contain:

- the exact executable script or notebook;
- raw inputs and raw outputs;
- a short `README.md` describing the method and result;
- package/version, command, timestamp, and Git commit provenance;
- an independent cross-check for nontrivial results;
- a link to the relevant manuscript novelty claim when one exists.

Start with one small real derivation. Generalize the format only after that pilot exposes
the group's actual needs.

## Phase 4 — Theory to predictions

- [ ] Define the group's first concrete output: for example Wilson coefficients, PPN
  parameters, amplitudes, post-Minkowskian corrections, or cross sections.
- [ ] Add numerical evaluation of a verified symbolic result.
- [ ] Compare the prediction with bounds or data cited from the corpus.
- [ ] Generate a draft figure/table and a short, human-reviewed interpretation.

## Phase 5 — Group-scale operation

- [ ] Replace `example_project` with a real manuscript and machine-readable novelty claims.
- [ ] Exercise the novelty watch end to end with deterministic integration fixtures.
- [ ] Move Qdrant to shared server mode only when multiple researchers need one index.
- [ ] Configure authentication, TLS, backups, and administration before shared deployment.
- [ ] Confirm a fresh clone can sync Dropbox, ingest, use MCP, and reproduce a workbench run.

## Definition of done

A researcher asks a real physics question; Jarvis retrieves cited evidence from the group
corpus; the AI runs a registered symbolic tool with complete provenance; an independent
check supports the result; the novelty engine compares it with real claims and literature;
and, when relevant, a numerical prediction is compared with cited bounds. Every step is
inspectable and reproducible.

## Immediate queue

1. Create the Phase 1 retrieval benchmark from real group questions.
2. Replace the placeholder manuscript with one real project and novelty claims.
3. Inventory the group's symbolic tools and create `packages/registry.yaml`.
4. Run the first scoped symbolic workbench derivation.
