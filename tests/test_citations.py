import httpx
import yaml

from jarvis.citations import (
    ARXIV,
    DOI,
    fetch_citations,
    manifest_identifiers,
    paper_identifier,
    sync_pdf_citations,
)


def test_identifier_prefers_arxiv_then_doi():
    assert paper_identifier({"arxiv": "2401.00001", "doi": "10.1/test"}) == "ARXIV:2401.00001"
    assert paper_identifier({"arxiv": None, "doi": "10.1/test"}) == "DOI:10.1/test"
    assert manifest_identifiers({"arxiv": "2401.00001", "doi": "10.1/Test"}) == [
        "arxiv:2401.00001",
        "doi:10.1/test",
    ]


def test_pdf_identifier_patterns():
    text = "arXiv:2401.01234 and arxiv.org/abs/hep-th/0306138 DOI:10.1000/ABC.1"
    assert {match.lower() for match in ARXIV.findall(text)} == {
        "2401.01234",
        "hep-th/0306138",
    }
    assert DOI.findall(text) == ["10.1000/ABC.1"]


def test_batch_citation_response_maps_to_internal_ids():
    def handler(request):
        assert request.url.params["fields"].endswith("references.paperId")
        return httpx.Response(
            200,
            json=[
                {
                    "paperId": "s2-a",
                    "citationCount": 12,
                    "referenceCount": 1,
                    "references": [{"paperId": "s2-b"}],
                }
            ],
        )

    references = [{"id": "a", "arxiv": "2401.00001", "doi": None}]
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        papers, unresolved = fetch_citations(references, client)
    assert papers["a"]["semantic_scholar_id"] == "s2-a"
    assert papers["a"]["references"] == ["s2:s2-b"]
    assert unresolved == []


def test_local_pdf_sync_extracts_reference_ids(tmp_path, monkeypatch):
    knowledge = tmp_path / "knowledge"
    papers = knowledge / "library" / "public" / "papers"
    books = knowledge / "books"
    papers.mkdir(parents=True)
    books.mkdir()
    (tmp_path / "literature").mkdir()
    (knowledge / "references.yaml").write_text(
        yaml.safe_dump(
            {
                "references": [
                    {"id": "source", "arxiv": "2401.00001", "doi": None},
                    {"id": "book", "arxiv": None, "doi": "10.1000/book"},
                    {"id": "target", "arxiv": "2401.00002", "doi": None},
                ]
            }
        )
    )
    pdf = papers / "source__2401.00001.pdf"
    pdf.write_bytes(b"placeholder")
    (papers / f"{pdf.name}.meta.yaml").write_text("reference_id: source\n")
    book = books / "book.pdf"
    book.write_bytes(b"placeholder")
    (books / f"{book.name}.meta.yaml").write_text("reference_id: book\n")

    class Page:
        def extract_text(self):
            return "This paper is 2401.00001; it cites arXiv:2401.00002."

    monkeypatch.setattr("jarvis.citations.PdfReader", lambda _: type("Reader", (), {"pages": [Page()]})())
    path, resolved, unresolved = sync_pdf_citations(tmp_path)
    data = yaml.safe_load(path.read_text())
    assert resolved == 2
    assert unresolved == 1
    assert data["papers"]["source"]["references"] == ["arxiv:2401.00002"]
    assert data["papers"]["book"]["identifiers"] == ["doi:10.1000/book"]
