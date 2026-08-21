from datetime import date

from jarvis.models import LiteratureRecord, NoveltyClaim
from jarvis.novelty import cosine_text, overlap_score


def test_cosine_text_identical_is_high():
    assert cosine_text("inverse EFT matching gravity", "inverse EFT matching gravity") > 0.99


def test_overlap_score_flags_keywords():
    claim = NoveltyClaim(
        id="T-1",
        claim="Automated inverse EFT matching reconstructs ultraviolet theories",
        keywords=["inverse EFT matching", "UV reconstruction", "automated matching"],
    )
    paper = LiteratureRecord(
        source="test",
        source_id="1",
        title="Automated inverse EFT matching and UV reconstruction",
        abstract="We reconstruct ultraviolet candidate theories from effective field theory data.",
        published=date.today(),
    )
    score, reasons = overlap_score(claim, paper)
    assert score > 0.4
    assert any("matched keywords" in r for r in reasons)
