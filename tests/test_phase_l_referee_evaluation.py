import runpy
from pathlib import Path

from jarvis.referee import RefereeReport, render_referee_report

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "benchmarks" / "phase_l_referee" / "review_seeded_entropy.py"


def test_seeded_phase_l_review_preserves_evidence_and_limits_scope():
    namespace = runpy.run_path(str(SCRIPT))
    report = namespace["report"]()
    rendered = render_referee_report(report)

    assert isinstance(report, RefereeReport)
    assert [finding.id for finding in report.findings] == ["F-S-001", "F-S-002"]
    assert report.findings[0].severity == "major"
    assert "A/(4G)" in report.findings[0].recommendation
    assert "PDF p. 232" in report.findings[0].evidence[0]
    assert "deliberately seeded fixture" in report.limitations[0]
    assert "F-S-001" in rendered
