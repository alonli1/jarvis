from jarvis.referee import RefereeFinding, RefereeReport, ResearchIdea, render_referee_report


def test_referee_report_and_idea_keep_evidence_and_novelty_scope_explicit():
    report = RefereeReport(
        manuscript="draft.tex",
        findings=[
            RefereeFinding(
                id="F1",
                severity="warning",
                observation="Convention unspecified.",
                evidence=["draft.tex: Eq. 2"],
                recommendation="State signature.",
            )
        ],
        limitations=["No external novelty search was performed."],
    )
    idea = ResearchIdea(
        id="I1",
        title="Check a tension",
        evidence=["knowledge/paper.pdf p. 3"],
        gap="Unresolved convention",
        falsifier="Counterexample",
        cheapest_decisive_test="Symbolic check",
        novelty_scope="Corpus-relative only",
    )

    assert "draft.tex: Eq. 2" in render_referee_report(report)
    assert idea.novelty_scope == "Corpus-relative only"
