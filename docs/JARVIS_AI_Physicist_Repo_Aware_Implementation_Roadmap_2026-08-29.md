# JARVIS — Repo-Aware AI Physicist Architecture, Delta Roadmap, and Implementation Specification

**Status:** Development specification intended to be handed directly to an implementation agent  
**Date:** 2026-08-29  
**Repository:** `alonli1/jarvis`  
**Audited baseline:** `master` at commit `9aa8b6063798355970ee2c47991fe3ccbb36edd8` (`Configure shared Dropbox library`, 2026-08-29)  
**Primary scientific scope:** General Relativity (GR), Quantum Field Theory (QFT), Effective Field Theory (EFT), curved-spacetime QFT, amplitudes, functional methods, renormalization/RG, quantum gravity, symbolic and numerical theoretical physics  

---

# 0. How to Use This Document

This document **supersedes the earlier greenfield JARVIS/PhysAI roadmap**. The implementation agent must treat the live repository as the starting point and must not rebuild capabilities that already exist.

The current repository is not a toy scaffold. It already contains a substantial scientific research harness:

> **2026-08-29 baseline note:** the shared Dropbox application is now configured in `assistant.toml`, Dropbox synchronization preserves display-case for relative paths, and a regression test covers that behavior. Treat shared-library configuration as implemented infrastructure rather than Phase-A feature work.

- a shared Dropbox-backed research library;
- local deterministic ingestion;
- hybrid dense+sparse retrieval through Qdrant/FastEmbed;
- page/section-aware citation metadata;
- a literature graph and graph-query layer;
- arXiv, INSPIRE-HEP, OpenAlex, and Semantic Scholar literature adapters;
- novelty-claim YAML and overlap-risk surveillance;
- deterministic research run bundles;
- MCP retrieval/graph tools;
- browser/IDE handoff support;
- portable Agent Skills;
- reproducible Python/Wolfram computation workbenches;
- a registered scientific tool catalog including xAct, FeynCalc, Matchete, FIRE7, Wolfram, and Python/SymPy;
- CI/tests and historical implementation auditing.

Therefore the next engineering objective is **not** “build a scientific assistant.”

The next objective is:

> **Evolve the existing provider-neutral research harness into an efficient, auditable AI physicist without sacrificing the deterministic infrastructure that already works.**

Whenever this document conflicts with an older development plan, **this document wins**.

---

# 1. Product Vision

JARVIS should eventually behave as an **AI physicist** proficient in QFT, GR, and quantum gravity.

A mature JARVIS should be able to:

1. answer advanced technical questions with correct citations and clearly stated assumptions;
2. understand the canonical literature in its configured scientific domains;
3. search and understand current literature;
4. know the research group's papers, manuscripts, calculations, notes, failed attempts, conventions, and open questions;
5. monitor new work continuously and detect possible relevance or novelty threats;
6. identify promising research directions grounded in literature and group capabilities;
7. create research plans;
8. derive analytic results;
9. perform symbolic and numerical computations;
10. use specialist tools such as xAct/xTensor, FeynCalc, Matchete, FIRE, Mathematica, SymPy, and future domain tools;
11. reproduce equations and results from papers;
12. translate literature methods into working scientific software;
13. implement algorithms in Python, Mathematica/Wolfram Language, Julia, C/C++, FORM, or other appropriate languages;
14. independently verify scientific claims using alternative derivations, limits, tools, numerical checks, or fresh-context reviewers;
15. act as an adversarial referee for research claims and manuscripts;
16. preserve provenance and distinguish literature fact, inference, conjecture, AI-derived result, human-verified result, and published result;
17. manage expensive model usage intelligently so that frontier models are used only when scientifically justified.

The target is **not** an LLM with a giant physics prompt. It is a system composed of:

- persistent scientific knowledge;
- deterministic retrieval and literature infrastructure;
- scientific tools;
- research-state/provenance machinery;
- a science-aware task and model router;
- a scientific orchestrator;
- independent verification policies;
- evaluation and budget-control infrastructure;
- replaceable reasoning models.

---

# 2. Core Architectural Principle

The current repository already embodies the correct foundational idea:

> **The research group's knowledge base is persistent; the reasoning model is replaceable.**

Preserve that principle.

JARVIS should not become dependent on one LLM provider, one IDE, one agent host, or one orchestration framework.

The mature architecture should look conceptually like this:

```text
                                   RESEARCHER
                                       |
                                       v
                              +------------------+
                              |  JARVIS FRONTEND |
                              | CLI / IDE / API  |
                              +---------+--------+
                                        |
                                  task classifier
                                        |
                +-----------------------+-------------------------+
                |                       |                         |
                v                       v                         v
          FAST SCIENCE            DEEP RESEARCH            SOFTWARE WORK
          retrieve/answer         investigate/derive       implementation
          literature lookup       compute/review           CI/refactor/API
          group memory            ideate/referee           package/tooling
                |                       |                         |
                |                       v                         v
                |             SCIENTIFIC ORCHESTRATOR      GENERIC CODEX
                |             + SCIENCE ROUTER             ROUTER + HONEY
                |                       |
                |          +------------+-------------+
                |          |            |             |
                |          v            v             v
                |      literature    derivation    computation
                |       specialist    physicist     physicist
                |          |            |             |
                |          +------------+-------------+
                |                       |
                |                 independent review
                |                       |
                +------------+----------+-----------+
                             |                      |
                             v                      v
                    JARVIS KNOWLEDGE          SCIENTIFIC TOOLS
                    retrieval/graph           xAct/FeynCalc/etc.
                    group memory              Python/Wolfram/etc.
                    manuscripts               generated workbenches
                    literature APIs
                             |                      |
                             +----------+-----------+
                                        |
                                        v
                              CLAIM/EVIDENCE LEDGER
                              PROVENANCE + EVALUATION
```

The key system design rule is:

> **One orchestration owner per task.**

Do not let JARVIS, PhysicsIntern, Honey, and a generic coding router all independently decompose the same scientific problem.

---

# 3. Live Repository Baseline — Preserve, Extend, Do Not Rebuild

## 3.1 Baseline commit

Development should begin from current `master`:

```text
9aa8b6063798355970ee2c47991fe3ccbb36edd8
Configure shared Dropbox library
2026-08-29
```

Before making structural changes, rerun the current tests and diagnostics because the existing `docs/AUDIT.md` is a historical audit of an earlier commit.

Required baseline commands:

```bash
uv sync --extra dev
uv run jarvis doctor
uv run pytest -q
uv run ruff check .
```

Record the results in a new dated audit file before architecture work.

Do **not** assume the historical `28 passed / 66% coverage` numbers still describe HEAD.

---

## 3.2 Existing components that should be treated as assets

### Retrieval and corpus

Preserve and improve, rather than replace:

- `src/jarvis/parsing.py`
- `src/jarvis/index.py`
- `src/jarvis/retrieval.py`
- `src/jarvis/citations.py`
- Qdrant/FastEmbed hybrid retrieval
- stable source/page/section metadata
- sidecar metadata files
- controlled scientific tags

The retrieval stack is already a major part of JARVIS's scientific memory layer.

Do not replace it with an agent-managed vector store or a provider-specific RAG feature.

### Shared library

Preserve:

- Dropbox OAuth/PKCE workflow;
- `src/jarvis/dropbox_client.py`;
- `src/jarvis/cloud_library.py`;
- `src/jarvis/library_sync.py`;
- conflict-preserving behavior;
- no automatic deletion propagation;
- ignored local `.jarvis/` state.

### Literature infrastructure

Preserve:

- arXiv adapter;
- INSPIRE-HEP adapter;
- OpenAlex adapter;
- Semantic Scholar adapter;
- literature normalization/deduplication;
- `literature/searches.yaml`;
- citation synchronization;
- relationship graph.

### Literature graph

Preserve:

- `src/jarvis/literature_graph.py`;
- `src/jarvis/graph_queries.py`;
- `src/jarvis/graph_view.py`;
- `src/jarvis/graph_server.py`;
- MCP graph tools;
- citation, bibliographic-coupling, tag-similarity, and manuscript-relevance edges.

The graph should become a major input to research ideation and literature intelligence.

### Deterministic research workflows

`src/jarvis/workflows.py` is a particularly important foundation.

It already provides:

- `RunBundle`;
- unique run directories under `.jarvis/runs/`;
- `manifest.json`;
- `evidence.md`;
- `result.md`;
- corpus revision fingerprints;
- citation manifests;
- deterministic literature runs;
- deterministic ideation runs;
- computation workbenches;
- explicit execution rather than hidden execution;
- tool/version recording;
- raw output capture.

This should become the persistence substrate for the native AI-physicist orchestrator.

**Do not create a second incompatible run format.**

Instead, evolve the current manifest format from `version: 1` to a backward-compatible research-state schema.

### Existing scientific Skills

Preserve the current decision that there are exactly four foundational portable skills:

1. `library-management`
2. `literature-understanding`
3. `research-ideation`
4. `reproducible-computation`

Do not explode the repository into dozens of auto-triggering foundational Skills.

Future scientific specialization should normally be implemented as:

- modes;
- references;
- role prompts;
- tool adapters;
- orchestrator policies;
- domain profiles;

rather than a large catalog of overlapping Skills.

### Existing computation registry

`packages/registry.yaml` already registers:

- Wolfram;
- xAct/xTensor;
- FeynCalc;
- Matchete;
- FIRE7;
- Python/SymPy.

Treat this as the first version of a **scientific capability registry**.

Do not replace it with hard-coded package checks scattered across agent prompts.

### Existing model abstraction

Current `src/jarvis/llm.py` is intentionally simple: a thin LiteLLM wrapper.

Current `src/jarvis/answering.py` is also intentionally simple: retrieve evidence, call one model, return answer + hits.

These are the correct places to extend upward.

The next system should preserve a simple fast path while introducing a more sophisticated optional routed path.

---

# 4. Privacy and Access Model — Deliberate Decision

## 4.1 Do not reintroduce document-level privacy tiers

The repository intentionally removed per-document privacy classifications.

This was a deliberate product decision and must be treated as such.

**Do not add fields such as:**

```text
privacy_class
visibility: public/group/confidential
default_privacy
per-document model permission
```

unless a future explicit product decision reverses this architecture.

All indexed documents are treated uniformly by JARVIS.

## 4.2 Access control boundary

Access is controlled at coarser system boundaries:

- repository access;
- shared Dropbox/library access;
- local machine access;
- IDE/model account access;
- provider credentials/account membership.

Researchers must understand that if a model is allowed to query the corpus, retrieved passages from the corpus may be sent to that model provider.

This is an operational/account boundary rather than a per-document filtering engine.

## 4.3 If stronger isolation is needed later

Prefer separate corpora/workspaces/repositories or separate JARVIS deployments over silently rebuilding complex document-level policy into the retrieval layer.

Examples:

```text
jarvis-public/
jarvis-group/
jarvis-project-secret/
```

or separately configured Dropbox libraries.

Do not solve a deployment/isolation problem by defaulting back to hidden document-level routing rules.

---

# 5. Preserve the Deterministic Harness as a First-Class Product

The AI-physicist layer must be **additive**, not destructive.

Even after native orchestration is implemented, all of the following should continue to work without any model API:

```bash
jarvis ingest
jarvis retrieve "..."
jarvis literature "..."
jarvis citations-sync
jarvis graph-build
jarvis graph ...
jarvis run literature ...
jarvis run ideation ...
jarvis run computation ...
jarvis compute execute ...
jarvis handoff ...
jarvis novelty ...
jarvis watch ...
```

Why this matters:

1. deterministic workflows are reproducible;
2. they are debuggable without an LLM;
3. researchers can use web subscriptions or local models;
4. they make model comparisons possible;
5. they provide evaluation fixtures;
6. they prevent orchestration logic from becoming the only way to access data;
7. they preserve provider neutrality.

The native physicist should consume these capabilities rather than subsume them into opaque agent behavior.

---

# 6. Target Operating Modes

JARVIS should expose several modes with very different cost and orchestration behavior.

## 6.1 Mode A — Retrieval / factual lookup

Examples:

- “Which paper in our corpus derives this coefficient?”
- “Where did we calculate this determinant?”
- “Find papers mentioning non-minimal scalar coupling to curvature.”

Pipeline:

```text
query
 -> deterministic retrieval/graph
 -> optional low-cost synthesis
 -> cited answer
```

No multi-agent research process.

Target default model profile: `extract` or `science_standard` depending on synthesis depth.

---

## 6.2 Mode B — Literature synthesis

Examples:

- “Compare functional and diagrammatic matching.”
- “What is the state of asymptotic-safety black-hole phenomenology?”
- “How do different authors define this curvature convention?”

Pipeline:

```text
query expansion
 -> local corpus retrieval
 -> external literature search if requested/needed
 -> citation graph expansion
 -> reranking
 -> synthesis
 -> contradiction/coverage check
```

Usually one capable synthesis model plus deterministic search is enough.

Avoid spawning many agents unless independent source interpretation is genuinely needed.

---

## 6.3 Mode C — Deep scientific investigation

Examples:

- “Derive the one-loop effective action for this field content.”
- “Check whether this modified-gravity solution is consistent.”
- “Determine whether a candidate UV model produces this EFT.”

Pipeline:

```text
classify scientific problem
 -> plan
 -> evidence acquisition
 -> analytic derivation and/or computation
 -> independent verification
 -> adversarial review
 -> claim promotion
 -> persistent research result
```

This is the main target of the native scientific orchestrator.

---

## 6.4 Mode D — Research ideation

Examples:

- “Find unexplored ways to combine automated EFT matching with asymptotic safety.”
- “Which gaps in our literature graph are scientifically meaningful?”

Pipeline:

```text
group capabilities
 + active manuscripts
 + literature graph
 + recent literature
 + unresolved contradictions
 + tool readiness
 -> candidate directions
 -> external novelty search
 -> cheapest decisive test
 -> ranking
```

Do not produce generic brainstorming lists.

---

## 6.5 Mode E — Referee / falsification

Examples:

- “Try to invalidate this result.”
- “Act as an adversarial referee for our paper.”

Pipeline:

```text
claim extraction
 -> assumptions/conventions map
 -> literature attack
 -> independent derivation/check
 -> edge-case tests
 -> logical-gap analysis
 -> novelty/citation attack
 -> structured referee report
```

Reviewer contexts must be independent enough to resist anchoring.

---

## 6.6 Mode F — Paper reproduction / implementation

Examples:

- “Implement this algorithm from the paper.”
- “Reproduce Figure 2.”
- “Turn Eq. 14–26 into working Mathematica and Python code.”

Pipeline:

```text
paper understanding
 -> scientific specification
 -> independent specification review
 -> software implementation
 -> paper benchmark reproduction
 -> scientific validation
 -> provenance bundle
```

Scientific interpretation and ordinary software implementation must remain separate stages.

---

## 6.7 Mode G — Ordinary software engineering

Examples:

- CI;
- packaging;
- CLI refactor;
- database/index migration;
- REST API;
- tests for non-scientific behavior;
- documentation tooling.

Use:

```text
Generic Codex model router
+
Honey for Devs
```

This is **outside** the scientific router.

---

# 7. Science-Aware Model Routing

This is the most important new efficiency subsystem.

The system must avoid two failure modes:

1. using Sol/xhigh for almost everything and exhausting token budget;
2. using cheap models for deceptively subtle scientific work.

## 7.1 Route by epistemic risk, not code complexity

Scientific difficulty can be high even when the output is only one equation.

The router should evaluate at least these dimensions:

```text
novelty                  Is this known/reproduction vs genuinely new?
ambiguity                Is the question/formalism underspecified?
mathematical_depth       Algebraic vs conceptual/nontrivial derivation?
convention_sensitivity   Can signs/bases/gauges/schemes change the answer?
tool_dependence          Is the result mechanically verifiable?
verification_strength    Is there a strong deterministic test?
literature_uncertainty   Are sources missing or contradictory?
coupling                 Do subproblems strongly depend on each other?
consequence              Would an error influence a paper/claim/design?
context_burden           How much evidence must be jointly understood?
creative_search          Is new idea generation required?
```

Represent these explicitly rather than inferring “complexity” from prompt length.

---

## 7.2 Define provider-neutral model profiles

Add profiles conceptually like:

```yaml
profiles:
  extract:
    capability: low
    reasoning: low
    target: metadata extraction, triage, formatting

  science_fast:
    capability: medium
    reasoning: medium
    target: bounded literature understanding and standard calculations

  science_standard:
    capability: high
    reasoning: high
    target: serious but known scientific work

  science_deep:
    capability: frontier
    reasoning: high
    target: novel derivation, difficult synthesis, coupled problems

  science_critical:
    capability: frontier
    reasoning: maximum
    target: unresolved disagreement, high-consequence claim, final adversarial review
```

Provider-specific mappings live in configuration, not source code.

Example OpenAI/Codex mapping to calibrate empirically:

```text
extract            -> GPT-5.6 Luna low/medium
science_fast       -> GPT-5.6 Luna high or Terra medium
science_standard   -> GPT-5.6 Terra high
science_deep       -> GPT-5.6 Sol high
science_critical   -> GPT-5.6 Sol xhigh
```

Do not use `science_critical` by default.

---

## 7.3 Role priors

The router should not make every decision from scratch. Roles provide sensible floors.

Initial prior table:

| Task/role | Default profile | Escalation triggers |
|---|---|---|
| Metadata extraction | `extract` | malformed source |
| Paper triage | `extract` | ambiguity / contradictory abstracts |
| Local retrieval synthesis | `science_fast` | source disagreement |
| Broad literature synthesis | `science_standard` | field controversy / subtle formalism |
| Known textbook derivation | `science_standard` | convention conflict |
| Novel analytic derivation | `science_deep` | disagreement -> `science_critical` |
| Symbolic script generation | `science_fast` | difficult formalism |
| Numerical implementation | `science_fast` | instability / interpretation |
| Interpretation of anomalous numerics | `science_deep` | unresolved -> `science_critical` |
| Research planning | `science_deep` | high-stakes project direction |
| Independent scientific reviewer | `science_deep` | consequential claim -> `science_critical` |
| Final adversarial critic | `science_critical` only when justified | — |
| Bookkeeping / result formatting | `extract` | — |

---

## 7.4 Escalation policy

Escalate when any of the following occur:

- two agents disagree materially;
- analytic and computational checks disagree;
- known limits fail;
- source conventions cannot be reconciled;
- no deterministic verification exists;
- the task changes from reproduction to novel inference;
- the result would materially support a publication claim;
- an agent reports low confidence for a substantive reason;
- the result is sensitive to gauge, regulator, operator basis, boundary conditions, or field redefinitions;
- a reviewer finds a plausible fatal objection.

Escalation should usually be **local to the failing subtask**, not restart the whole project on Sol/xhigh.

---

## 7.5 De-escalation policy

Use cheaper models when:

- the task is pure extraction;
- source boundaries are already known;
- the result can be checked deterministically;
- the action is mechanical rewriting;
- a strong model has already produced a precise specification;
- the task is independent and easily testable;
- the agent only needs to inspect logs, grep files, or format structured data.

---

## 7.6 Parent/orchestrator model

The coordinator should not automatically be the strongest model.

Prefer a coordinator that mostly:

- reads task state;
- chooses next action;
- assigns bounded work;
- checks returned schemas;
- updates state;
- decides whether verification gates are satisfied.

Its role is **workflow control, not doing the derivation itself**.

A Terra-class/high-reasoning coordinator is a reasonable initial default. Evaluate whether Luna/high is sufficient for some workflows.

Use Sol for the scientific leaf that needs Sol, not because it is convenient to leave the entire conversation on Sol.

---

# 8. Budget and Token Management

The router needs an explicit budget manager rather than implicit “be efficient” instructions.

## 8.1 Track cost per research run

Extend run manifests with:

```json
{
  "model_usage": [
    {
      "role": "deriver",
      "profile": "science_deep",
      "provider": "openai",
      "model": "...",
      "reasoning_effort": "high",
      "input_tokens": 0,
      "output_tokens": 0,
      "cached_tokens": 0,
      "estimated_cost": null
    }
  ]
}
```

For subscription/Codex environments where exact monetary cost may not be exposed, at least record token counts, model tier, reasoning level, and wall time when available.

## 8.2 Budget scopes

Support:

```text
per task
per research run
per day
per project
optional weekly soft budget
```

The budget manager must support **soft limits** rather than failing important research silently.

Example behavior:

```text
80% of budget used
 -> avoid speculative branches
 -> reduce parallel fan-out
 -> prefer deterministic checks
 -> ask whether unresolved high-cost branches are worth escalation
```

## 8.3 Context minimization

Never give every agent the full corpus or full run transcript.

Each subagent should receive a **task packet**:

```yaml
task_id: ...
role: analytic_deriver
objective: ...
known_assumptions: [...]
required_conventions: [...]
source_refs: [...]
relevant_claims: [...]
artifacts_to_read: [...]
required_output_schema: ...
```

Evidence retrieval stays in JARVIS.

The agent gets the smallest evidence set sufficient for the task.

## 8.4 Reuse expensive results

Cache by:

- source IDs;
- task fingerprint;
- conventions;
- equations/input artifact hashes;
- tool versions;
- model profile;
- corpus revision.

Do not rerun Sol derivations merely because a coordinator context was restarted.

---

# 9. Native Scientific Orchestrator

## 9.1 Bootstrap with PhysicsIntern, do not permanently nest it

PhysicsIntern is useful as an immediately available research methodology because it emphasizes:

- decomposition;
- fresh-context work;
- analytic derivation;
- computation;
- independent review;
- strategic critique;
- durable artifacts.

Use it initially to learn what works on real JARVIS physics tasks.

However, the final product is JARVIS.

The desired migration is:

```text
Phase 1
JARVIS tools + PhysicsIntern research protocol

Phase 2
JARVIS controls routing/evidence/budgets
PhysicsIntern still supplies role protocol

Phase 3
JARVIS native ScientificOrchestrator implements validated protocol
PhysicsIntern becomes optional comparison backend

Phase 4
JARVIS native workflow is primary
PhysicsIntern retained only for evals or alternate workflows
```

Do not create permanent orchestration recursion:

```text
JARVIS agent
 -> PhysicsIntern agent
    -> JARVIS agent
       -> another orchestrator
```

---

## 9.2 Native orchestration roles

Start with a minimal role set.

### Coordinator

Does not perform substantive derivations unless explicitly forced by fallback.

Responsibilities:

- classify task;
- construct plan;
- route roles/models;
- manage budget;
- request evidence;
- enforce schemas;
- decide verification gates;
- update research state.

### Literature specialist

Responsibilities:

- use JARVIS retrieval + external adapters;
- identify relevant primary sources;
- extract assumptions/conventions;
- compare conflicting sources;
- report coverage gaps.

### Analytic physicist

Responsibilities:

- derive equations/results;
- state conventions and assumptions;
- identify mathematical identities used;
- record uncertainty;
- suggest independent checks.

### Computational physicist

Responsibilities:

- choose appropriate registered tools;
- produce scripts inside JARVIS run workbench;
- execute only through explicit run machinery;
- retain raw output;
- check limits/symmetries/dimensions;
- compare tools when possible.

### Scientific implementation specialist

Responsibilities:

- convert a validated scientific specification into code;
- use ordinary SWE practices;
- preserve conventions precisely;
- build regression cases from known physics.

This role may hand off actual coding to the generic SWE stack once the scientific specification is frozen.

### Independent reviewer

Fresh context where practical.

Responsibilities:

- challenge derivation;
- check assumptions;
- inspect conventions;
- reproduce critical steps independently;
- search for failure modes;
- distinguish fatal vs cosmetic issues.

### Strategic critic

Used only when needed.

Responsibilities:

- question whether the entire approach is misguided;
- check whether the result addresses the research question;
- identify missing branches or external literature;
- recommend abandonment/replanning when justified.

Do not spawn every role for every question.

---

# 10. Claim and Evidence Ledger

The existing run bundle records evidence and result artifacts but needs a richer scientific epistemic state.

Add typed claim records.

## 10.1 Claim statuses

Recommended states:

```text
candidate
source_grounded
derived_once
computed_once
independently_checked
contradicted
ai_verified
human_verified
published_or_external
retired
```

Do not overload one “established” label.

## 10.2 Example claim schema

```yaml
id: CLAIM-2026-0017
project: build
statement: >
  Integrating out the specified heavy scalar generates ...
kind: derived_result
status: independently_checked

scope:
  theory: scalar_plus_gravity
  approximation: one_loop
  regulator: dimensional_regularization
  regime: E_over_M_small

conventions:
  metric_signature: mostly_plus
  riemann: ...

support:
  sources: [paper:..., paper:...]
  derivations: [run:.../D001]
  computations: [run:.../C002]
  reviews: [run:.../R001]

known_issues: []
created_by: ai
human_reviewed: false
```

## 10.3 Promotion gates

Examples:

```text
candidate -> derived_once
  requires analytic artifact

derived_once -> independently_checked
  requires separate context/tool/method where practical

independently_checked -> ai_verified
  requires reviewer acceptance and no unresolved high-severity flags

ai_verified -> human_verified
  explicit researcher action only
```

No model can set `human_verified`.

---

# 11. Evolve Existing Run Bundles Instead of Creating New State

Current `workflows.py` manifests should be extended carefully.

## 11.1 Manifest v2

Example:

```json
{
  "version": 2,
  "id": "...",
  "workflow": "deep_research",
  "query": "...",
  "created_at": "...",
  "corpus_revision": "...",
  "status": "running",
  "plan": "plan.json",
  "tasks": [],
  "inputs": [],
  "citations": [],
  "tools": [],
  "artifacts": [],
  "claims": [],
  "model_usage": [],
  "verification": [],
  "flags": [],
  "decision_log": []
}
```

Old v1 manifests must remain readable.

## 11.2 Artifact structure

For a deep research run:

```text
.jarvis/runs/<id>/
  manifest.json
  problem.md
  plan.json
  evidence.md
  result.md
  claims.yaml
  tasks/
    T001.json
    T002.json
  derivations/
    D001.md
    D002.md
  computations/
    C001/
      scripts/
      outputs/
      logs/
      metadata.json
  reviews/
    R001.md
  decisions/
    DEC001.md
```

Keep everything tied to one run ID.

---

# 12. Model/Provider Abstraction — Refactor `llm.py`, Do Not Bypass It

The current `llm.py` is a simple LiteLLM call. Evolve it into a provider-neutral execution interface.

Suggested package:

```text
src/jarvis/models_runtime/
  __init__.py
  client.py
  profiles.py
  routing.py
  budgets.py
  telemetry.py
```

Avoid naming collision with current `src/jarvis/models.py`, which contains Pydantic data models.

## 12.1 Runtime request

```python
@dataclass
class ModelRequest:
    profile: str
    role: str
    messages: list[Message]
    structured_schema: type[BaseModel] | None
    max_output_tokens: int | None
    temperature: float | None
    task_features: TaskFeatures
```

## 12.2 Runtime result

```python
@dataclass
class ModelResult:
    content: str
    parsed: BaseModel | None
    provider: str
    model: str
    reasoning_effort: str | None
    usage: Usage
    latency_seconds: float
    routing_reason: str
```

## 12.3 Provider mappings

Keep these in config:

```toml
[models.profiles.extract]
provider = "openai"
model = "..."
reasoning = "medium"

[models.profiles.science_standard]
provider = "openai"
model = "..."
reasoning = "high"

[models.profiles.science_deep]
provider = "openai"
model = "..."
reasoning = "high"
```

A researcher can replace those mappings without rebuilding the corpus.

---

# 13. Extend Configuration Carefully

Current `assistant.toml` is intentionally simple.

Add optional sections without breaking existing configuration.

Example:

```toml
[assistant]
name = "Jarvis"
default_model = "ollama/qwen3:14b"
max_context_chunks = 10

[physicist]
enabled = false
coordinator_profile = "science_standard"
max_parallel_agents = 4
require_independent_check_for_novel_claims = true

[routing]
mode = "science-aware"
record_explanations = true

[budget]
max_agents_per_run = 12
max_frontier_calls_per_run = 6
soft_token_budget = 300000

[models.profiles.extract]
model = "..."

[models.profiles.science_standard]
model = "..."

[models.profiles.science_deep]
model = "..."

[models.profiles.science_critical]
model = "..."
```

If `[physicist]` is absent, current behavior should remain unchanged.

---

# 14. Research Planning

Planning should be structured and bounded.

## 14.1 Plan schema

```yaml
research_question: ...
success_criteria: ...

known_assumptions: [...]
conventions_to_fix: [...]

subproblems:
  - id: T001
    kind: literature
    objective: ...
    dependencies: []
    verification: source_comparison

  - id: T002
    kind: analytic_derivation
    objective: ...
    dependencies: [T001]
    verification: independent_computation

stop_conditions:
  - fatal inconsistency found
  - required literature unavailable
  - budget exceeded without justified escalation
```

## 14.2 Planning should not over-decompose

The planner must explicitly ask:

```text
Would splitting this task improve correctness or parallelism enough to justify duplicated context?
```

A one-page derivation should not become 12 agents.

---

# 15. Literature Intelligence

Most of the infrastructure already exists. Focus on scientific quality rather than new adapters for their own sake.

## 15.1 Current assets

Use:

- local curated corpus;
- arXiv;
- INSPIRE;
- OpenAlex;
- Semantic Scholar;
- exact DOI/arXiv identity;
- citation graph;
- bibliographic coupling;
- controlled tags;
- active manuscript relevance.

## 15.2 Next improvements

Prioritize:

1. equation-aware / structure-aware PDF extraction;
2. better LaTeX AST parsing;
3. GROBID/Docling integration for difficult PDFs;
4. citation completeness metrics;
5. citation-neighborhood expansion;
6. literature-query evals;
7. source authority metadata;
8. robust paper-version handling;
9. contradiction extraction between sources;
10. convention extraction.

## 15.3 Scientific source packet

When passing literature to a reasoning agent, use a structured evidence packet:

```yaml
source_id: paper:arxiv:...
title: ...
location: page 7, Eq. 19
relevance: ...
source_type: primary_paper
claims:
  - ...
conventions:
  - ...
text: ...
extraction_warning: false
```

Do not pass giant unstructured PDF dumps.

---

# 16. Research Ideation Engine

The current `research-ideation` Skill is a good seed. Extend it into a structured idea engine.

## 16.1 Candidate sources

Generate ideas from:

- disconnected literature-graph components;
- papers sharing methods but not physical systems;
- theories sharing observables but not computational methods;
- known limitations mentioned repeatedly in reviews;
- contradictions between papers;
- missing automation in high-friction calculations;
- new tools that make previously impractical calculations feasible;
- group-specific expertise and existing software;
- active manuscript follow-up questions;
- newly published papers that change feasibility;
- untested limits/regimes of established methods.

## 16.2 Candidate idea object

```yaml
id: IDEA-...
title: ...
question: ...
scientific_motivation: ...

supporting_evidence: [...]
identified_gap: ...

novelty_status: externally_searched | local_only | uncertain
closest_prior_work: [...]

feasibility:
  analytic: medium
  computation: high
  software_tools: [matchete, xact]

cheapest_decisive_test: ...
falsifiers: [...]
expected_failure_modes: [...]

scores:
  significance: 0-5
  tractability: 0-5
  distinctiveness: 0-5
  falsifiability: 0-5
  group_advantage: 0-5
```

## 16.3 Novelty discipline

Before labeling an idea “novel,” perform explicit external literature search.

Use language such as:

```text
no close overlap found in searched sources
possible prior art
strong potential overlap
unverified novelty
```

Never infer global novelty from local corpus absence.

---

# 17. Scientific Tool Layer

## 17.1 Preserve `packages/registry.yaml`

Evolve it into a richer capability registry.

Example future entry:

```yaml
- id: xact
  capabilities:
    - tensor_algebra
    - curvature
    - perturbation_theory
    - action_variation
  domains:
    - GR
    - gravitational_EFT
  execution:
    environment: wolfram
  verification_strength:
    symbolic: high
```

## 17.2 Initial tool priorities

Current tools:

- Wolfram;
- xAct/xTensor;
- FeynCalc;
- Matchete;
- FIRE7;
- Python/SymPy.

Next candidates should be driven by actual research use, but likely include:

- xPert / xPand;
- FeynArts / FeynHelpers;
- FORM;
- pySecDec;
- Kira;
- Cadabra;
- DoFun / DiFfRG or relevant FRG tooling;
- Julia scientific packages;
- group-developed ORBIT/BUILD tooling when stable.

## 17.3 Capability-based tool selection

Agents should request capabilities:

```text
need: tensor_variation
```

not hard-code:

```text
always use Mathematica script X
```

Then a deterministic tool selector maps capability -> available package.

---

# 18. Reproducible Computation Protocol

The existing Skill already encodes good rules. Make them machine-checkable where possible.

Every serious computation should record:

```text
problem
conventions
assumptions
physical regime
input equations
source references
package versions
exact scripts
exact commands
raw output
exit status
post-processing
checks
independent verification
interpretation
```

## 18.1 Scientific checks library

Build reusable checks:

- dimensional consistency;
- symmetry identities;
- Ward identities when applicable;
- diffeomorphism/gauge identities where applicable;
- known limits;
- decoupling limits;
- flat-space limit;
- weak-field limit;
- classical limit;
- heavy-mass expansion consistency;
- regulator/scheme cross-check where feasible;
- precision/convergence scans;
- basis-reduction equivalence;
- numerical stability;
- sign convention transformations.

## 18.2 Process success is not scientific success

A process exit code of zero means only that code executed.

Never promote a scientific result solely because:

- Mathematica returned an expression;
- Python produced a plot;
- unit tests passed;
- symbolic simplification terminated.

---

# 19. Scientific Software Implementation Workflow

This is where the scientific plane and SWE plane meet.

For paper-derived or research-derived code:

```text
scientific source / derivation
        |
        v
scientific specification
        |
        v
independent spec review
        |
        v
ordinary software implementation
(Generic Codex router + Honey allowed)
        |
        v
software tests
        |
        v
scientific regression tests
        |
        v
independent scientific review
```

## 19.1 Scientific specification must freeze

Before handing implementation to Honey/router, produce a machine-readable spec containing:

```yaml
input_objects: ...
output_objects: ...
equations: ...
conventions: ...
assumptions: ...
domain_of_validity: ...
known_test_cases: ...
required_symmetries: ...
expected_limits: ...
references: ...
```

Honey may simplify implementation but may **not** remove the validation cases in the scientific spec.

---

# 20. Honey + Generic Codex Router Boundary

Use the generic model router + Honey for **development work**, including development of JARVIS itself.

Good uses:

- refactoring Python modules;
- adding CLI commands;
- CI fixes;
- packaging;
- ordinary unit tests;
- API integration;
- code cleanup;
- documentation tooling;
- deterministic adapters after the scientific spec is fixed.

Do **not** allow Honey's minimization or subagent injection to govern:

- scientific derivations;
- literature interpretation;
- research planning;
- PhysicsIntern roles;
- scientific reviewer roles;
- evidence handoffs;
- scientific claims;
- independent scientific checks.

## 20.1 Operational recommendation

Use separate development/research modes.

### Dev mode

```text
Codex
+ generic model router
+ Honey
-> edit JARVIS source
```

### Research mode

```text
JARVIS / PhysicsIntern / scientific orchestrator
Honey disabled
Generic coding router does not classify scientific tasks
```

Do not run a global Honey hook that injects into every scientific subagent.

---

# 21. PhysicsIntern Integration Plan

## 21.1 Why use it initially

PhysicsIntern supplies a tested research-process idea that JARVIS currently lacks natively:

- planned deep investigation;
- separate roles;
- fresh contexts;
- independent checks;
- critique;
- structured research artifacts.

## 21.2 How it should consume JARVIS

PhysicsIntern should use JARVIS as the evidence/tool substrate:

```text
PhysicsIntern surveyor
 -> JARVIS retrieval/literature/graph

PhysicsIntern computer
 -> JARVIS computation workbench + registered tools

PhysicsIntern reviewer
 -> JARVIS evidence packets + run artifacts
```

Do not let PhysicsIntern maintain a second long-term corpus.

## 21.3 What to measure during bootstrap

For each PhysicsIntern-assisted run record:

- roles used;
- models used;
- token usage;
- elapsed time;
- number of useful findings;
- number of false concerns;
- whether independent checks caught errors;
- whether fresh contexts mattered;
- which role could have used a cheaper model;
- where protocol created unnecessary overhead.

Use these measurements to design JARVIS's native orchestrator.

---

# 22. Fast `jarvis ask` Must Remain Fast

Do not turn every `jarvis ask` call into a deep research project.

Current `answering.py` should evolve into a routed fast path:

```text
question
 -> lightweight task classifier
 -> retrieve
 -> choose profile
 -> answer
```

Only escalate to deep research when:

- user explicitly asks;
- task requires derivation/computation;
- source conflict cannot be resolved;
- novelty/research judgment is requested;
- classifier detects high epistemic risk.

Suggested interface:

```bash
jarvis ask "..."                  # fast path
jarvis ask "..." --deep           # force research path
jarvis ask "..." --profile ...    # override model profile
```

---

# 23. Proposed New Python Package Structure

Avoid a major rewrite of existing modules.

Add a cohesive optional subsystem:

```text
src/jarvis/
  # existing modules remain

  physicist/
    __init__.py
    types.py
    classifier.py
    routing.py
    profiles.py
    budgets.py
    planner.py
    orchestrator.py
    task_packets.py
    claims.py
    verification.py
    memory.py
    telemetry.py

    roles/
      literature.py
      derivation.py
      computation.py
      reviewer.py
      critic.py
      implementation.py

    prompts/
      coordinator.md
      literature.md
      derivation.md
      reviewer.md
      critic.md
```

Potential later refactor:

```text
src/jarvis/tools/
  registry.py
  execution.py
  adapters/
```

but do not refactor `workflows.py` merely for aesthetics before orchestration works.

---

# 24. Extend `models.py` With Scientific Data Models

Current models cover chunks, literature records, novelty claims/matches.

Add Pydantic models such as:

```text
TaskFeatures
RouteDecision
ResearchPlan
ResearchTask
TaskPacket
ScientificClaim
EvidenceReference
VerificationRecord
ScientificFlag
ModelUsage
DecisionRecord
ResearchSummary
```

Keep data models provider-neutral.

Example:

```python
class TaskFeatures(BaseModel):
    novelty: int = Field(ge=0, le=3)
    ambiguity: int = Field(ge=0, le=3)
    mathematical_depth: int = Field(ge=0, le=3)
    convention_sensitivity: int = Field(ge=0, le=3)
    verification_strength: int = Field(ge=0, le=3)
    consequence: int = Field(ge=0, le=3)
    creative_search: int = Field(ge=0, le=3)
```

---

# 25. Routing Algorithm — Initial Implementation

Do not make the first router a large agentic system.

Start with hybrid routing:

1. deterministic role priors;
2. a cheap classifier for ambiguous requests;
3. deterministic safety/epistemic floors;
4. post-task escalation signals;
5. feedback from evals.

Conceptual pseudocode:

```python
def route(task):
    features = classify(task)
    profile = role_prior(task.kind)

    if features.novelty >= 2:
        profile = max_profile(profile, "science_deep")

    if features.consequence >= 2 and features.verification_strength <= 1:
        profile = max_profile(profile, "science_deep")

    if task.kind in {"critical_review", "resolve_conflict"}:
        profile = max_profile(profile, "science_deep")

    return profile
```

Use xhigh only through explicit escalation rules rather than thresholding a vague total score.

---

# 26. Independent Verification Strategy

The system should select a verification method matched to the claim's likely failure modes.

Examples:

| Claim | Preferred verification |
|---|---|
| Algebraic tensor identity | separate symbolic tool / independent derivation |
| Loop coefficient | known literature + alternate formalism + numerical/symbolic check |
| Numerical spectrum | convergence/precision scan + alternative solver |
| EFT basis reduction | independent basis tool / random numerical tensor test |
| GR field equation | xAct variation + independent analytic check |
| Literature claim | primary-source verification |
| Novelty claim | external multi-source literature search + human review |
| Software implementation | paper benchmark + scientific invariants + ordinary tests |

Verification is not “ask a second model if it agrees.”

A second model can be one component, but independent tools/methods are stronger.

---

# 27. Research Memory

The current repository has strong corpus memory but weak structured memory of AI research results.

Add a persistent research-result index sourced from run bundles.

The system should answer:

- “Have we derived this before?”
- “Which run checked this convention?”
- “Which failed approach used this ansatz?”
- “Which result was human verified?”
- “Which notebook/script generated this coefficient?”

Do not automatically inject AI-generated results into authoritative literature knowledge.

Maintain provenance distinctions:

```text
external published source
external preprint
internal group document
AI-derived candidate
AI independently checked
human-verified internal result
published group result
```

---

# 28. Failed Directions and Negative Results

Preserve negative research information.

Add structured records for:

```yaml
id: DEAD-...
question: ...
approach: ...
why_failed: ...
evidence: [...]
conditions_under_which_it_might_work: ...
run_id: ...
```

This prevents repeated rediscovery of failed directions and improves idea generation.

---

# 29. Manuscript and Referee Integration

Current novelty YAML should remain the structured source of manuscript claims.

Extend manuscript-aware workflows to separate:

```text
novelty surveillance
technical claim verification
citation completeness
assumption consistency
reproducibility
adversarial referee review
```

A future command:

```bash
jarvis referee PROJECT
```

should orchestrate:

1. claim extraction;
2. claim-to-source mapping;
3. literature prior-art search;
4. assumptions map;
5. independent checks for central results;
6. missing-reference search;
7. potential overclaim report;
8. technical reviewer report.

Never auto-edit a manuscript based on referee output without explicit researcher action.

---

# 30. Novelty Monitoring

The current novelty system is valuable and should remain interpretable.

Do not replace deterministic overlap scoring with a giant model call.

Pipeline should remain:

```text
claims
 -> lexical/semantic/citation search
 -> deterministic ranking
 -> threshold
 -> selective expensive adjudication
 -> human-readable report
```

The AI-physicist layer can enrich adjudication but not erase deterministic evidence.

---

# 31. Evaluation Framework — Mandatory Before Heavy Autonomy

This is critical.

A router cannot be optimized against generic software benchmarks and assumed to work for theoretical physics.

Create a JARVIS eval corpus using problems the group already understands.

## 31.1 Evaluation categories

### Retrieval

- expected source appears;
- expected page/equation appears;
- citation correctness;
- Recall@k / MRR.

### Literature understanding

- convention identification;
- equation interpretation;
- correct comparison of papers;
- hallucinated citations.

### QFT derivations

- one-loop coefficients;
- simple amplitudes;
- beta functions;
- EFT matching;
- known heat-kernel results.

### GR derivations

- curvature identities;
- variation of actions;
- Einstein equations in simple ansätze;
- perturbative identities;
- known limits.

### Scientific computation

- symbolic reproduction;
- numerical reproduction;
- cross-tool agreement.

### Research ideation

Use historical questions where later literature establishes whether the proposed direction was meaningful.

### Referee mode

Seed manuscripts/notes with known subtle errors and evaluate whether JARVIS catches them.

### Paper implementation

Select published methods with public reference implementations or known results.

---

# 32. Model Router Evaluation

For each eval task run multiple profiles:

```text
Luna-like cheap profile
Terra-like balanced profile
Sol high
Sol xhigh
```

Record:

- correctness;
- scientific completeness;
- citation correctness;
- error type;
- tool usage;
- tokens;
- wall time;
- number of retries;
- verification success.

Build a routing table from **empirical JARVIS data**.

The objective is not cheapest response.

The objective is:

> **minimum expected resource use subject to a required scientific-quality threshold.**

---

# 33. Acceptance Metric for the Router

Compare against baseline:

```text
all tasks on Sol/xhigh
```

A router release is acceptable only if it:

1. preserves or improves scientific correctness on the eval suite;
2. reduces expensive-model token usage materially;
3. does not substantially increase total task failures/retries;
4. catches underpowered routing and escalates appropriately;
5. logs enough information to explain decisions.

A useful initial goal:

```text
>= 50% reduction in frontier/xhigh usage
with statistically indistinguishable success on known-answer tasks
```

Do not hard-code this as a permanent product promise; calibrate it.

---

# 34. Research Orchestrator Evaluation

Compare:

```text
single Sol/xhigh
vs
PhysicsIntern bootstrap
vs
native JARVIS orchestration
```

Measure:

- scientific success;
- missed assumptions;
- caught errors;
- total tokens;
- frontier tokens;
- elapsed time;
- unnecessary agent fan-out;
- human corrections required.

The native orchestrator should only replace PhysicsIntern once it performs at least as well on representative group problems.

---

# 35. CLI Roadmap

Preserve existing commands.

Add incrementally:

```bash
# Explain routing without executing
jarvis route "derive the one-loop curvature-squared terms ..."

# Fast routed answer
jarvis ask "..." --auto-model

# Deep research
jarvis research start --question "..."
jarvis research status RUN_ID
jarvis research continue RUN_ID
jarvis research review RUN_ID

# Budget and telemetry
jarvis budget RUN_ID

# Evals
jarvis eval run retrieval
jarvis eval run qft
jarvis eval route

# Referee
jarvis referee PROJECT
```

Avoid creating dozens of commands before the underlying data models stabilize.

---

# 36. MCP/API Evolution

Current MCP is appropriately retrieval/graph focused.

Extend read capabilities first:

```text
search_knowledge
find_related_papers
explain_relationship
find_citation_path
find_bridge_papers
papers_relevant_to_manuscript
get_run
search_runs
get_claim
search_claims
get_tool_status
```

Be conservative about remote write/execute tools.

Explicit computation execution through CLI/workbench remains safer and more reproducible than giving every remote host a generic shell tool.

---

# 37. Phase Roadmap — Current Repo to AI Physicist

The earlier greenfield phase sequence is obsolete. Use this sequence.

---

## Phase A — Freeze and Re-Audit Current HEAD

**Goal:** create a trustworthy baseline at commit `9aa8b606` or newer.

Tasks:

1. `uv sync --extra dev`;
2. run tests;
3. run coverage;
4. run Ruff;
5. run `jarvis doctor`;
6. smoke-test retrieval;
7. smoke-test one literature query;
8. smoke-test one computation workbench;
9. verify package registry detection;
10. update `docs/AUDIT.md` with current commit.

Do not redesign architecture before this is recorded.

**Acceptance gate:** baseline behavior and failures are documented reproducibly.

---

## Phase B — Scientific Evaluation Suite

**Goal:** create known-answer benchmarks before adding complex routing.

Build 20–40 initial cases across:

- retrieval;
- literature synthesis;
- QFT;
- GR;
- computation;
- paper reproduction.

Use real group questions where possible.

Store under:

```text
evals/
  retrieval/
  qft/
  gr/
  computation/
  literature/
```

Every case should specify expected evidence and scoring criteria.

**Acceptance gate:** repeatable eval command produces machine-readable report.

---

## Phase C — Manifest v2 + Scientific Result Types

**Goal:** extend current `.jarvis/runs` rather than build new state.

Implement:

- backward-compatible manifest reader;
- claim models;
- verification records;
- model-usage records;
- task records;
- decision log;
- structured flags.

**Acceptance gate:** current v1 workflows still work; new runs can store v2 data.

---

## Phase D — Runtime Model Profiles and Telemetry

**Goal:** make `llm.py` provider-neutral but route-aware.

Implement:

- model profile configuration;
- usage telemetry;
- structured result support;
- routing explanation metadata;
- profile override CLI.

Do not implement full orchestration yet.

**Acceptance gate:** `jarvis ask` can choose configured model profiles and log usage without changing retrieval behavior.

---

## Phase E — Science-Aware Router v1

**Goal:** avoid Sol/xhigh overuse on ordinary scientific tasks.

Implement:

- `TaskFeatures`;
- deterministic role priors;
- cheap classifier;
- epistemic floors;
- escalation policy;
- dry-run `jarvis route`;
- router eval harness.

**Acceptance gate:** on known-answer evals, router materially reduces frontier calls without degrading quality.

---

## Phase F — PhysicsIntern Bootstrap Integration

**Goal:** perform real multi-step research using existing JARVIS evidence/tools.

Requirements:

- PhysicsIntern in dedicated research mode/workspace;
- JARVIS retrieval and graph used by survey role;
- JARVIS workbench used by computation role where practical;
- Honey disabled;
- generic coding router disabled for scientific classification;
- results imported into JARVIS runs as provisional artifacts;
- token/model/role telemetry recorded.

Run at least five known-answer investigations.

**Acceptance gate:** independent checks catch at least some seeded mistakes and complete artifacts are reproducible.

---

## Phase G — Tool Capability Expansion

**Goal:** make domain tools reliable enough for agent use.

Tasks:

- richer package capability registry;
- xAct workflows;
- FeynCalc workflows;
- Matchete workflow;
- FIRE workflow;
- tool smoke tests;
- output parsers where useful;
- tool-specific scientific check templates.

Add other packages only when real tasks require them.

**Acceptance gate:** at least one QFT and one GR benchmark can be independently verified by registered tools.

---

## Phase H — Native Planner + Task Packets

**Goal:** move orchestration control into JARVIS while still using PhysicsIntern as a baseline.

Implement:

- `ResearchPlan`;
- `ResearchTask`;
- dependency graph;
- task packets;
- stop conditions;
- budget allocation;
- fresh-context leaf execution.

**Acceptance gate:** planner decomposes representative tasks without runaway fan-out and produces reproducible plans.

---

## Phase I — Native Verification + Claim Ledger

**Goal:** make scientific state explicit.

Implement:

- verification-policy selector;
- claim promotion rules;
- contradiction state;
- reviewer integration;
- human verification action;
- research-memory indexing.

**Acceptance gate:** no central result can become `ai_verified` without recorded evidence satisfying policy.

---

## Phase J — Native Scientific Orchestrator

**Goal:** match or exceed PhysicsIntern while integrating directly with JARVIS.

Implement the minimal roles defined earlier.

Do not copy PhysicsIntern's exact prompt structure blindly.

Keep only protocol elements that improve JARVIS evals.

**Acceptance gate:** native JARVIS meets or exceeds PhysicsIntern on representative problems with equal or lower resource use and better provenance integration.

---

## Phase K — Paper Reproduction and Scientific Implementation

**Goal:** become capable of turning literature into code reliably.

Implement:

- paper specification extractor;
- equation/convention map;
- implementation spec;
- SWE handoff format;
- paper benchmark runner;
- scientific regression tests;
- reproduction report.

**Acceptance gate:** reproduce at least three published results/algorithms in different categories.

---

## Phase L — Referee + Research Direction Engine

**Goal:** help the group find problems and opportunities.

Implement:

- manuscript technical review;
- claim dependency graph;
- prior-art attack;
- missing-citation search;
- structured research ideas;
- external novelty checking;
- cheapest-decisive-test planning.

**Acceptance gate:** evaluated on known historical or seeded cases.

---

## Phase M — Multi-Provider Calibration

**Goal:** preserve the original provider-neutral vision.

Evaluate model profiles across at least two providers plus optionally a local model.

Route by capability profile, not provider brand.

**Acceptance gate:** same scientific run can swap compatible profiles without changing corpus or scientific state format.

---

## Phase N — Bounded Autonomy

Only after earlier phases are reliable.

Potential capabilities:

- unattended literature investigation;
- overnight known-answer reproduction;
- scheduled manuscript surveillance;
- bounded computational scans;
- research-direction triage;
- self-generated follow-up checks.

Do not allow open-ended autonomous publication/manuscript changes.

---

# 38. Exact Repository Delta Map

## Keep largely intact

```text
src/jarvis/parsing.py
src/jarvis/index.py
src/jarvis/retrieval.py
src/jarvis/citations.py
src/jarvis/literature/*
src/jarvis/literature_graph.py
src/jarvis/graph_queries.py
src/jarvis/graph_view.py
src/jarvis/graph_server.py
src/jarvis/dropbox_client.py
src/jarvis/cloud_library.py
src/jarvis/library_sync.py
.agents/skills/*
packages/registry.yaml
```

## Extend carefully

```text
src/jarvis/models.py
src/jarvis/config.py
src/jarvis/llm.py
src/jarvis/answering.py
src/jarvis/workflows.py
src/jarvis/mcp_server.py
src/jarvis/cli.py
assistant.toml
```

## Add

```text
src/jarvis/physicist/
evals/
```

Potential later addition:

```text
src/jarvis/tools/
```

Do not migrate stable code merely to satisfy the new package structure.

---

# 39. Tests to Add Early

## Routing

- trivial extraction never routes to critical profile;
- novel derivation never routes below configured floor;
- disagreement triggers escalation;
- budget pressure lowers fan-out before lowering required epistemic floor;
- user override works;
- routing explanation is deterministic enough to inspect.

## Research state

- v1 manifest loads;
- v2 manifest round-trip;
- claim promotion requires evidence;
- model cannot set human verification;
- interrupted run can resume;
- task dependencies enforced.

## Computation

- tool version recorded;
- raw output recorded;
- failed process cannot produce verified result;
- missing scientific checks block promotion when policy requires them.

## Literature

- primary source preferred over secondary where applicable;
- external-source failure marked as incomplete coverage;
- novelty wording stays qualified.

---

# 40. Failure Modes to Design Against

## Over-orchestration

Symptom:

```text
small question -> planner -> 8 agents -> reviewer -> critic -> huge bill
```

Defense:

- fast-path classifier;
- delegation benefit threshold;
- agent-count budget;
- role minimums only when needed.

## Strong-model overuse

Defense:

- role priors;
- explicit epistemic floors;
- per-run frontier-call budget;
- eval-based routing.

## Weak-model under-routing

Defense:

- consequence/novelty floors;
- automatic escalation on disagreement;
- reviewer triggers;
- eval regression tests.

## Context poisoning by too much literature

Defense:

- retrieve narrowly;
- evidence packets;
- source hierarchy;
- reranking;
- fresh contexts.

## Scientific anchoring

Defense:

- independent reviewer context;
- do not leak expected numerical result when independence matters;
- alternate method/tool.

## Hallucinated citations

Defense:

- post-generation citation validator;
- citations must map to retrieved source IDs;
- source location validation.

## Mistaking code correctness for physics correctness

Defense:

- scientific regression suite;
- known limits;
- dimensional checks;
- independent scientific review.

## Recursive framework conflict

Defense:

- one orchestration owner;
- Honey excluded from research agents;
- generic router excluded from scientific classification;
- PhysicsIntern transitional.

---

# 41. Priority Order From Today

If only one development agent is available, use this order:

```text
1. Re-audit current HEAD
2. Build scientific eval suite
3. Manifest v2 + claim/verification models
4. Model telemetry and provider-neutral profiles
5. Science-aware router v1
6. PhysicsIntern/JARVIS bootstrap experiments
7. Tool workflow validation
8. Native planner/task packets
9. Verification + claim ledger
10. Native orchestrator
11. Paper reproduction workflow
12. Research memory
13. Referee / ideation engine
14. Multi-provider calibration
15. Bounded autonomy
```

Do not prioritize UI before the scientific loop is measured and reliable.

---

# 42. First Concrete Development Sprint

The implementation agent should begin with a small, auditable sprint rather than immediately building autonomous agents.

## Sprint 1 deliverables

### 1. Current-head audit

Create:

```text
docs/AUDIT-2026-08-29-AI-PHYSICIST-BASELINE.md
```

with exact commit, tests, coverage, lint, retrieval smoke test, computation smoke test, and known issues.

### 2. Add eval skeleton

```text
evals/schema.py or equivalent
evals/cases/retrieval/*.yaml
evals/cases/qft/*.yaml
evals/cases/gr/*.yaml
```

Add a command:

```bash
jarvis eval run
```

### 3. Add runtime telemetry without changing behavior

Wrap current LiteLLM call so that provider/model/usage/latency can be recorded.

Current `jarvis ask` output should remain semantically unchanged.

### 4. Add optional model profiles

Support configuration but keep `default_model` backward compatible.

### 5. Add `jarvis route --dry-run`

For now route only among profiles. Do not spawn subagents.

### 6. Add tests

No current deterministic workflow should regress.

**Do not implement the full orchestrator in Sprint 1.**

---

# 43. Example Science-Aware Routing Scenarios

## Scenario A — Simple source lookup

User:

> Which paper in our corpus gives the scalar heat-kernel coefficient?

Route:

```text
retrieval -> extract profile
```

No planner, no Sol.

---

## Scenario B — Standard literature synthesis

User:

> Compare functional matching and diagrammatic matching at one loop.

Route:

```text
JARVIS literature retrieval
 -> science_standard synthesis
 -> no multi-agent process unless sources conflict
```

---

## Scenario C — New EFT derivation

User:

> Integrate out this heavy non-minimally coupled field and derive the curvature-squared EFT.

Route:

```text
coordinator: standard profile
literature/convention extraction: fast/standard
analytic derivation: science_deep
symbolic computation: science_fast/standard + Matchete/xAct/SymPy where appropriate
independent reviewer: science_deep
critical profile only if disagreement remains
```

This is much cheaper than running every step on Sol/xhigh.

---

## Scenario D — Mechanical implementation after derivation

User:

> Implement the verified algorithm as a Python package.

Route:

```text
freeze scientific spec
 -> generic Codex router + Honey
 -> scientific regression checks
```

---

## Scenario E — Novelty threat

User:

> Does this new paper make our result non-novel?

Route:

```text
JARVIS novelty/literature deterministic search
 -> science_standard comparison
 -> science_deep reviewer if overlap is high
 -> qualified report
 -> human decides novelty claim
```

---

# 44. Definition of a Successful AI-Physicist v1

JARVIS AI Physicist v1 should be considered successful when it can perform the following end-to-end:

1. receive a nontrivial QFT/GR research question;
2. decide whether it is fast-path or deep-research;
3. retrieve the right local and external evidence;
4. route subtasks to appropriately priced model profiles;
5. perform at least one analytic or computational step;
6. use a registered physics tool when appropriate;
7. independently check the central result;
8. record assumptions/conventions;
9. produce source-backed citations;
10. store run provenance and model usage;
11. distinguish candidate vs verified claims;
12. resume the research run after context loss;
13. use substantially fewer frontier/xhigh tokens than an all-Sol/xhigh baseline on the eval suite;
14. preserve all existing deterministic JARVIS workflows.

---

# 45. Definition of a Successful AI-Physicist v2

V2 should additionally:

- perform structured paper reproduction;
- maintain calculation/result memory;
- search failed approaches;
- propose evidence-grounded research directions;
- perform manuscript referee review;
- reason over citation/knowledge graphs;
- route across multiple providers;
- learn routing thresholds from eval results and explicit researcher feedback;
- support richer symbolic packages;
- manage longer multi-day research projects;
- perform bounded unattended research loops.

---

# 46. Definition of a Successful AI-Physicist v3

A later mature system should approach a persistent research collaborator:

- continuously aware of canonical and recent literature;
- continuously aware of active group work;
- able to reconstruct prior group calculations;
- able to identify literature changes that affect current projects;
- able to propose and test new directions;
- able to derive and compute;
- able to implement literature methods;
- able to challenge itself independently;
- able to allocate model/tool resources efficiently;
- able to explain precisely why a claim is believed and how it was verified.

The goal is not autonomous authority.

The goal is **auditable scientific competence**.

---

# 47. Non-Goals for the Near Term

Do not spend early development effort on:

- custom model fine-tuning;
- training embeddings from scratch;
- a complex web UI;
- microservices;
- a second vector database;
- replacing Qdrant without evidence;
- rewriting the Dropbox layer;
- global document privacy tiers;
- dozens of overlapping Skills;
- open-ended autonomous paper writing;
- fully automatic novelty verdicts;
- automatically publishing manuscripts;
- allowing agents to silently modify scientific source material;
- using frontier models for all work.

---

# 48. Instructions to the Development Agent

1. **Start from the live repository.**
2. **Do not rebuild existing retrieval, graph, library, novelty, workflow, MCP, or computation infrastructure.**
3. **Preserve backward compatibility for existing CLI commands.**
4. **Keep deterministic workflows operational without any LLM API.**
5. **Do not reintroduce document-level privacy tiers.**
6. **Treat `.jarvis/runs` as the base research-state substrate.**
7. **Add scientific evals before aggressive model routing.**
8. **Implement model profiles before full multi-agent orchestration.**
9. **Keep routing provider-neutral.**
10. **Use PhysicsIntern experimentally as a bootstrap protocol rather than permanent nested infrastructure.**
11. **Keep Honey and the generic coding router out of scientific subagents.**
12. **Use Honey/router for ordinary code implementation only after the scientific specification is fixed.**
13. **Require provenance for scientific computation.**
14. **Require independent verification for important novel results.**
15. **No AI action can mark a result human verified.**
16. **Prefer small, testable pull requests.**
17. **Update architecture/audit docs as behavior changes.**
18. **Every new autonomous feature must have an evaluation case and a rollback path.**

---

# 49. Immediate Agent Prompt

A development agent receiving this file should begin with the following task:

> Audit the current `alonli1/jarvis` master branch at the exact checked-out commit. Confirm the live behavior of the deterministic research harness, run the full test/lint/diagnostic suite, and create a current baseline audit. Then implement only Phase B/D groundwork: add a minimal scientific evaluation framework and model-call telemetry/profile abstractions while preserving every existing CLI and deterministic workflow. Do not build the multi-agent orchestrator yet. Do not reintroduce document-level privacy tiers. Submit the work in small commits with tests and update the audit/architecture documentation.

---

# 50. Final Architectural Summary

The system should evolve as follows:

```text
TODAY
=====

Jarvis research harness
  + shared Dropbox corpus
  + hybrid retrieval
  + literature APIs
  + citation graph
  + novelty triage
  + four portable Skills
  + deterministic run bundles
  + MCP
  + scientific tool registry/workbenches
  + simple optional LiteLLM answer path


NEXT
====

add scientific evals
  -> model telemetry
  -> provider-neutral profiles
  -> science-aware router
  -> PhysicsIntern bootstrap experiments
  -> typed claims + verification
  -> native planner
  -> native scientific orchestrator
  -> research memory
  -> paper reproduction
  -> referee + research-direction engine


SOFTWARE DEVELOPMENT PLANE
==========================

ordinary code work
  -> generic Codex router
  -> Honey
  -> tests


SCIENTIFIC RESEARCH PLANE
=========================

scientific problem
  -> JARVIS science-aware router
  -> deterministic evidence
  -> minimum necessary specialist agents
  -> registered scientific tools
  -> independent verification
  -> claim/evidence ledger
  -> human review where appropriate


EFFICIENCY TARGET
=================

Do not ask:
  "Can Sol/xhigh solve this?"

Ask:
  "What is the cheapest combination of evidence, tools, models, and independent checks
   that reaches the required scientific confidence?"
```

That question should guide the implementation of JARVIS as an AI physicist.
