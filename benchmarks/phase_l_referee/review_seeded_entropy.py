"""Render a deterministic technical review of the seeded Phase L fixture."""
from jarvis.referee import RefereeFinding, RefereeReport, render_referee_report


def report() -> RefereeReport:
    return RefereeReport(
        manuscript="benchmarks/phase_l_referee/seeded_schwarzschild_entropy_draft.md",
        findings=[
            RefereeFinding(
                id="F-S-001",
                severity="major",
                claim_id="S-001",
                observation=(
                    "The claimed normalization A/(2G), and therefore 2 pi G M^2, "
                    "has a factor-of-two error."
                ),
                evidence=[
                    (
                        "knowledge/books/kiefer-qg-book.pdf, PDF p. 232 (printed p. 219), "
                        "eq. (7.23): S_BH = k_B A/(4 G hbar)"
                    ),
                    (
                        "knowledge/books/kiefer-qg-book.pdf, PDF p. 232 (printed p. 219), "
                        "eq. (7.24): S_BH = k_B pi r_s^2/(G hbar)"
                    ),
                ],
                recommendation=(
                    "Replace the normalization with A/(4G); after stating r_s = 2GM "
                    "and c = hbar = k_B = 1, give S_BH = 4 pi G M^2."
                ),
            ),
            RefereeFinding(
                id="F-S-002",
                severity="warning",
                claim_id="S-001",
                observation="The excerpt omits the source, unit convention, and Schwarzschild-radius relation.",
                evidence=[
                    "seeded_schwarzschild_entropy_draft.md: Claim S-001",
                    (
                        "knowledge/books/kiefer-qg-book.pdf, PDF p. 232 (printed p. 219), "
                        "eqs. (7.23)--(7.24)"
                    ),
                ],
                recommendation=(
                    "Add the source locator, c = hbar = k_B = 1 convention, and r_s = 2GM "
                    "before presenting the specialization."
                ),
            ),
        ],
        limitations=[
            "This is a deliberately seeded fixture, not a submitted or historical manuscript.",
            "The review validates structured evidence handling for the stated claim only.",
            "No novelty, completeness, or external-literature coverage judgment was made.",
        ],
    )


if __name__ == "__main__":
    print(render_referee_report(report()), end="")
