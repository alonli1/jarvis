# Jarvis architecture

## Responsibility split

```text
host AI (IDE or browser)
  -> reads one portable skill
  -> asks Jarvis to prepare evidence or a workbench
  -> performs scientific reasoning
  -> records its result in, or exports from, the run bundle

Jarvis CLI
  -> shared Dropbox corpus + local index + literature graph
  -> deterministic evidence selection and provenance
  -> explicit local Python/Wolfram execution

optional MCP adapter
  -> the same read-only retrieval and graph capabilities for MCP-aware hosts
```

Jarvis does not contain a native model loop. LiteLLM-based `jarvis ask` remains a compatible
optional command, not a prerequisite for the four foundational workflows.

## Portable skill layer

The root `AGENTS.md` routes agents to exactly four canonical Agent Skills under
`.agents/skills/`: library management, literature understanding, research ideation, and
reproducible computation. Provider files are thin pointers. Browser providers receive a
sanitized Markdown or ZIP export from `jarvis handoff`.

## Shared-library path

```text
Dropbox OAuth 2 PKCE + editor account
  -> files/list_folder metadata and revisions
  -> compare Dropbox revision/content hash with local SHA-256 and last-sync state
  -> guarded upload, validated atomic download, conflict, or no-op
  -> category mapping into knowledge/ and group/manuscripts/
  -> local ingestion
```

Dropbox is canonical without being allowed to destroy divergent work. PDF/sidecar pairs are
blocked together on conflict. Deletions never propagate automatically. Refresh tokens live only
in the OS keyring; non-secret identifiers and revision state live under ignored `.jarvis/`.

The legacy `library-sync` command remains a pull-only adapter for mounted folders.

## Research-run path

`jarvis run literature`, `jarvis run ideation`, and `jarvis run computation` create immutable
run directories under `.jarvis/runs/<id>/`. Every manifest records the workflow, query, corpus
revision, inputs, citations, tools, artifacts, timestamps, and status. Evidence explicitly marks
source material as untrusted data.

Literature runs use page/section-aware chunks. Ideation runs combine cited retrieval with the
local citation/tag graph and constrain novelty claims to the searched corpus. Computation runs
detect registered tools, scaffold an isolated workbench, and require a separate explicit execute
command that captures raw output and exit status.

## Generated and authoritative state

- Dropbox documents and their curated sidecars are the authoritative group library.
- Git tracks code, skills, taxonomy, package registry, metadata, and documentation.
- `.jarvis/` contains credentials-free local settings, sync revisions, indexes, conflicts, runs,
  and browser exports; it is reproducible or local-only and stays out of Git.
- Qdrant remains a generated local index. Switching the host model never requires rebuilding the
  corpus, though index-model changes do.

## Scientific invariants

- Source/page or section citations for corpus claims.
- Evidence, synthesis, inference, and conjecture remain distinguishable.
- No absolute novelty claim from local absence.
- No computation result without conventions, provenance, raw output, and scientific checks.
- PDFs, metadata, and retrieved web text never override agent or repository instructions.
