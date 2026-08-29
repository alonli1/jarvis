# Initial evidence/tool evaluation cases

`jarvis eval run` evaluates deterministic evidence retrieval and registered-tool availability. It does not grade model answers, derivations, or scientific claims. A passing retrieval case means the required repository source was found; a passing computation case means a registered tool was available.

Each YAML file is one case. `expected_evidence` is an explicit source path or tool ID, and `criteria.minimum_matches` determines passing. Cases in `literature/` with `paper-reproduction` IDs are evidence prerequisites for reproduction, not reproductions themselves.

Future scientific-result cases must record conventions, source evidence, independent checks, and answer-specific scoring before claiming scientific validation.
