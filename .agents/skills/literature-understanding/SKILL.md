---
name: literature-understanding
description: Read, compare, synthesize, or review QFT, GR, and quantum-gravity literature using page-grounded Jarvis evidence. Use for scientific understanding and manuscript review, not speculative novelty claims or unrecorded calculations.
---

# Literature understanding

First establish the research intent: literature, computation, or both. A
literature run already selects literature; otherwise, if the user has not made
the intended mode clear, ask once rather than silently substituting a
literature answer for an independent calculation. For both, prepare
page-grounded evidence and hand the exact source formulas, conventions, and
scope to the computation workflow for independent checking.

Prepare evidence with `jarvis run literature --question "..." [--paper ID]` and read the run's
`evidence.md` and `manifest.json` before answering.

- Identify the question, conventions, assumptions, physical regime, method, principal results,
  limitations, and stated open questions.
- For comparisons, align definitions and conventions before comparing formulas or conclusions.
- Cite source path and page or section for factual claims. Label synthesis and inference.
- Do not reconstruct missing equations, tables, or figures from context. Report weak extraction.
- In manuscript-review mode, assess support for claims, missing references, conflicting results,
  and scope—not merely prose quality.

For on-demand monitoring of active manuscript claims, use the literature-surveillance mode in
[`references/literature-surveillance.md`](references/literature-surveillance.md). This mode owns
report interpretation; it does not create GitHub issues or treat provider coverage as complete.

Use the citation graph as supporting structure, not proof of scientific agreement or importance.
If the bundle is insufficient, retrieve more evidence or state the limitation.
When working in an IDE, write the cited analysis to the run's `result.md` so it can be reviewed,
exported, and reproduced.
