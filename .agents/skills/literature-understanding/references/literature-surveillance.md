# Literature-surveillance mode

Use this mode when asked to check recent literature against the active claims in one or more
manuscripts. It is triage within `literature-understanding`, not a separate foundational skill.

1. Inspect each target manuscript's `novelty.yaml`; do not invent claims or search terms.
2. Run `jarvis novelty PROJECT --days N` for one project or `jarvis watch --days N` for all active
   projects. Add `--source` to restrict coverage when a provider is unavailable.
3. Read the generated Markdown report under `literature/reports/` and inspect promising primary
   sources directly before drawing a conclusion.
4. Separate found literature, overlap-score interpretation, scientific inference, and researcher
   decisions. Report novelty only relative to the sources and time window actually searched.
5. Treat source errors as partial-coverage warnings. Retry transient failures, configure the
   provider's documented API key when appropriate, or continue with named working sources. Never
   convert an incomplete search into a claim of absence.
6. Keep the report in the research workspace or cite it from a run result. Do not open a GitHub issue
   automatically; publication is an explicit researcher decision.

The repository's `on-demand-literature-watch` GitHub Action is only a manual convenience wrapper
around the same CLI command. Skill-guided local use is the default.
