---
name: research-ideation
description: Develop evidence-grounded, testable research directions from the Jarvis corpus and literature graph. Use for gaps, tensions, bridge opportunities, and project directions; do not present corpus-relative ideas as proven global novelty.
---

# Research ideation

First establish whether the user wants a literature-only map of the field, a
computation-led research direction, or both. If this is not clear, ask once.
For both, distinguish reported literature gaps from hypotheses that need a new
derivation or computation.

Start with `jarvis run ideation --topic "..." [--project PATH]`. Use its evidence and graph
summary to generate candidate directions.

For each direction record:

- the supporting results and exact gap, tension, disconnected methods, or unexplored regime;
- the assumptions that make the idea plausible;
- a concrete observable, derivation, or computation that could test it;
- possible falsifiers and the cheapest decisive check;
- required expertise, software, data, and likely failure modes;
- novelty status: `relative to local corpus`, `externally searched`, or `unverified`.

Rank candidates by scientific value, tractability, distinctiveness, and falsifiability. Prefer a
small number of well-supported hypotheses over long speculative lists. Never turn absence from
retrieval into evidence that no prior work exists.
Write the ranked directions and their evidence/check plans to the run's `result.md`.
