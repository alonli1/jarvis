from pathlib import Path

import pytest
import yaml

from jarvis.library_sync import sync_library


def write_document(root: Path, relative: str, content: bytes) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_sync_maps_categories_and_writes_portable_metadata(tmp_path):
    repo = tmp_path / "repo"
    source = tmp_path / "provider" / "Jarvis"
    paper = write_document(source, "papers/paper.pdf", b"%PDF-test")
    paper.with_name("paper.pdf.meta.yaml").write_text(
        "title: Curved-space EFT\nauthors: [A. Researcher]\ntags: [gravity]\n"
        "dropbox_id: id:paper-1\n"
    )
    write_document(source, "notes/calculation.md", b"# Calculation\n")
    write_document(source, "manuscripts/draft.tex", b"draft\n")

    result = sync_library(repo, source, provider="dropbox")

    assert result.copied == 3
    local_paper = repo / "knowledge" / "papers" / "paper.pdf"
    note = repo / "knowledge" / "notes" / "calculation.md"
    manuscript = repo / "group" / "manuscripts" / "draft.tex"
    assert local_paper.exists() and note.exists() and manuscript.exists()
    metadata = yaml.safe_load(local_paper.with_name("paper.pdf.meta.yaml").read_text())
    assert metadata["storage_provider"] == "dropbox"
    assert metadata["storage_path"] == "papers/paper.pdf"
    assert metadata["storage_id"].startswith("sha256:")
    assert metadata["dropbox_id"] == "id:paper-1"
    manuscript_metadata = yaml.safe_load(manuscript.with_name("draft.tex.meta.yaml").read_text())
    assert "visibility" not in manuscript_metadata


def test_sync_dry_run_and_manual_conflict_are_non_destructive(tmp_path):
    repo = tmp_path / "repo"
    source = tmp_path / "provider"
    remote = write_document(source, "notes/note.md", b"remote\n")

    result = sync_library(repo, source, dry_run=True)
    destination = repo / "knowledge" / "notes" / "note.md"
    assert result.copied == 1
    assert not destination.exists()

    destination.parent.mkdir(parents=True)
    destination.write_bytes(b"local\n")
    destination.with_name("note.md.meta.yaml").write_text("title: Curated locally\n")
    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        sync_library(repo, source)
    assert destination.read_bytes() == b"local\n"
    assert remote.read_bytes() == b"remote\n"


def test_sync_rejects_invalid_pdf(tmp_path):
    repo = tmp_path / "repo"
    source = tmp_path / "provider"
    write_document(source, "papers/bad.pdf", b"not a pdf")
    with pytest.raises(ValueError, match="Invalid PDF header"):
        sync_library(repo, source)
