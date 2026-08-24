from pathlib import Path

import pytest
import yaml

from jarvis.library_sync import sync_library


def write_document(root: Path, relative: str, content: bytes) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_sync_maps_visibility_and_writes_portable_metadata(tmp_path):
    repo = tmp_path / "repo"
    source = tmp_path / "provider" / "Jarvis"
    paper = write_document(source, "public/papers/paper.pdf", b"%PDF-test")
    paper.with_name("paper.pdf.meta.yaml").write_text(
        "title: Curved-space EFT\nauthors: [A. Researcher]\ntags: [gravity]\n"
        "visibility: public\ndropbox_id: id:paper-1\n"
    )
    write_document(source, "group/notes/calculation.md", b"# Group calculation\n")
    write_document(source, "confidential/manuscripts/draft.tex", b"secret draft\n")

    result = sync_library(repo, source, provider="dropbox")

    assert result.copied == 3
    public = repo / "knowledge" / "library" / "public" / "papers" / "paper.pdf"
    group = repo / "group" / "library" / "group" / "notes" / "calculation.md"
    private = (
        repo / "group" / "library" / "confidential" / "manuscripts" / "draft.tex"
    )
    assert public.exists() and group.exists() and private.exists()
    metadata = yaml.safe_load(public.with_name("paper.pdf.meta.yaml").read_text())
    assert metadata["visibility"] == "public"
    assert metadata["storage_provider"] == "dropbox"
    assert metadata["storage_path"] == "public/papers/paper.pdf"
    assert metadata["storage_id"].startswith("sha256:")
    assert metadata["dropbox_id"] == "id:paper-1"
    private_metadata = yaml.safe_load(
        private.with_name("draft.tex.meta.yaml").read_text()
    )
    assert private_metadata["visibility"] == "confidential"


def test_sync_dry_run_and_manual_conflict_are_non_destructive(tmp_path):
    repo = tmp_path / "repo"
    source = tmp_path / "provider"
    remote = write_document(source, "public/notes/note.md", b"remote\n")

    result = sync_library(repo, source, dry_run=True)
    destination = repo / "knowledge" / "library" / "public" / "notes" / "note.md"
    assert result.copied == 1
    assert not destination.exists()

    destination.parent.mkdir(parents=True)
    destination.write_bytes(b"local\n")
    destination.with_name("note.md.meta.yaml").write_text("title: Curated locally\n")
    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        sync_library(repo, source)
    assert destination.read_bytes() == b"local\n"
    assert remote.read_bytes() == b"remote\n"


def test_sync_rejects_invalid_pdf_and_visibility_mismatch(tmp_path):
    repo = tmp_path / "repo"
    source = tmp_path / "provider"
    paper = write_document(source, "public/papers/bad.pdf", b"not a pdf")
    with pytest.raises(ValueError, match="Invalid PDF header"):
        sync_library(repo, source)

    paper.write_bytes(b"%PDF-valid")
    paper.with_name("bad.pdf.meta.yaml").write_text("visibility: confidential\n")
    with pytest.raises(ValueError, match="Visibility mismatch"):
        sync_library(repo, source)
