# AI-physicist baseline audit — 2026-08-29

## Baseline

- Branch: `ai-physicist-roadmap`
- HEAD: `9aa8b6063798355970ee2c47991fe3ccbb36edd8` (`Configure shared Dropbox library`)
- Python: 3.14.4
- uv: 0.12.5
- Audit scope: Phase A only; no production behavior changed.

## Verification

| Check | Result |
|---|---|
| `uv sync --extra dev` | passed; 104 packages checked |
| `uv run pytest -q` | passed: 47 tests in 3.14s |
| Coverage | passed: 47 tests, 63% total coverage |
| `uv run ruff check .` | failed: 14 existing findings; no automated fixes applied |
| `uv run jarvis doctor` | passed: repository folders, Dropbox/keyring, Python, WolframScript, xAct, FeynCalc, Matchete, and FIRE7 available |
| Local retrieval smoke | passed: `jarvis retrieve "gravity EFT" --limit 3` returned cited local PDF and manifest evidence |
| Live literature smoke | completed: `jarvis literature "effective field theory gravity" --days 7` returned arXiv/OpenAlex records; Semantic Scholar returned HTTP 429 |
| Computation workbench | passed: prepared and explicitly executed `20260829T115711Z-computation-verify-x-y-2-expansion` with exit code 0 |

## Known issues

- Ruff reports 14 pre-existing findings: `B008`, `DTZ011`, `I001`, and one `BLE001`; this milestone does not change them.
- The live literature request returned one future-dated OpenAlex record (2027-11-07) and a Semantic Scholar rate limit. These are live-provider data-quality/availability observations, not deterministic test failures.
- Overall coverage is 63%; command paths, live adapters, index integration, and novelty orchestration remain comparatively under-covered.
- The computation smoke run verifies workbench creation, explicit execution, logs, and tool detection; its generated script is intentionally a harness smoke test, not a scientific derivation.

## Preserved invariants

No document-level privacy tiers were added. Existing retrieval, Dropbox, literature, graph, MCP, skills, run-bundle, and computation behavior was not migrated or replaced.
