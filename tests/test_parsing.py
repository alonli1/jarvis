from typing import ClassVar

from jarvis.parsing import chunk_text, discover_documents, iter_document_chunks


def test_chunk_text_overlap_and_content():
    text = "A" * 150 + ". " + "B" * 150 + ". " + "C" * 150
    chunks = chunk_text(text, size=200, overlap=30)
    assert len(chunks) >= 2
    assert all(chunks)


def test_reference_manifest_creates_one_searchable_chunk_per_reference(tmp_path):
    manifest = tmp_path / "knowledge" / "references.yaml"
    manifest.parent.mkdir()
    manifest.write_text(
        """references:
  - id: test-paper
    tier: T0
    type: paper
    title: A Test of Gravity Matching
    authors: [A. Researcher]
    year: 2026
    arxiv: "2601.00001"
    doi: null
    url: https://arxiv.org/abs/2601.00001
    topics: [gravity, matching]
    ingest_policy: download_arxiv
    why: Core test reference.
"""
    )

    assert discover_documents(tmp_path / "knowledge") == [manifest]
    chunks = list(iter_document_chunks(manifest, tmp_path, chunk_chars=100, overlap=10))
    assert len(chunks) == 1
    assert chunks[0].title == "A Test of Gravity Matching"
    assert chunks[0].tags == ["gravity", "matching"]
    assert chunks[0].metadata["tier"] == "T0"
    assert chunks[0].metadata["format"] == "reference_manifest"


def test_pdf_sidecar_metadata_is_carried_into_chunks(tmp_path, monkeypatch):
    paper = tmp_path / "knowledge" / "papers" / "paper.pdf"
    paper.parent.mkdir(parents=True)
    paper.write_bytes(b"placeholder")
    (paper.parent / "paper.pdf.meta.yaml").write_text(
        "title: Tagged paper\ntags: [gravitational_eft]\nreference_id: paper-1\n"
    )

    class Page:
        def extract_text(self):
            return "Gravity is an effective field theory."

    class Reader:
        pages: ClassVar = [Page()]

    monkeypatch.setattr("jarvis.parsing.PdfReader", lambda _: Reader())
    chunks = list(iter_document_chunks(paper, tmp_path, chunk_chars=100, overlap=10))
    assert chunks[0].tags == ["gravitational_eft"]
    assert chunks[0].metadata["reference_id"] == "paper-1"
