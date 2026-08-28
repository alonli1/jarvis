import hashlib
from pathlib import Path

import pytest

from jarvis.cloud_library import resolve_conflict, sync_dropbox
from jarvis.dropbox_client import RemoteFile


def content_hash(content: bytes) -> str:
    blocks = hashlib.sha256()
    for start in range(0, len(content), 4 * 1024 * 1024):
        blocks.update(hashlib.sha256(content[start : start + 4 * 1024 * 1024]).digest())
    return blocks.hexdigest()


class FakeDropbox:
    def __init__(self, files: dict[str, bytes] | None = None):
        self.data = files or {}
        self.revisions = {path: "1" for path in self.data}

    def list_files(self):
        return {
            path: RemoteFile(
                id=f"id:{path}",
                path=f"/jarvis/{path}",
                name=Path(path).name,
                rev=self.revisions[path],
                content_hash=content_hash(data),
                server_modified="2026-08-27T00:00:00Z",
            )
            for path, data in self.data.items()
        }

    def download(self, path):
        return self.data[path.removeprefix("/jarvis/")]

    def upload(self, relative, content, rev=None):
        if rev is not None:
            assert rev == self.revisions[relative]
        self.data[relative] = content
        self.revisions[relative] = str(int(self.revisions.get(relative, "0")) + 1)
        return self.list_files()[relative]


def write_pdf(root: Path, content: bytes = b"%PDF-local") -> Path:
    path = root / "knowledge" / "papers" / "paper.pdf"
    path.parent.mkdir(parents=True)
    path.write_bytes(content)
    return path


def test_local_addition_uploads_document_and_generated_sidecar(tmp_path):
    write_pdf(tmp_path)
    client = FakeDropbox()

    result = sync_dropbox(tmp_path, client)

    assert result.uploaded == 2
    assert client.data["papers/paper.pdf"] == b"%PDF-local"
    assert "papers/paper.pdf.meta.yaml" in client.data
    assert (tmp_path / ".jarvis/library-state.json").exists()


def test_remote_addition_downloads_and_conflicting_changes_are_preserved(tmp_path):
    client = FakeDropbox(
        {
            "papers/paper.pdf": b"%PDF-original",
            "papers/paper.pdf.meta.yaml": b"title: Original\ntags: []\n",
        }
    )
    first = sync_dropbox(tmp_path, client)
    assert first.downloaded == 2
    local = tmp_path / "knowledge/papers/paper.pdf"

    local.write_bytes(b"%PDF-local-edit")
    client.data["papers/paper.pdf"] = b"%PDF-remote-edit"
    client.revisions["papers/paper.pdf"] = "2"
    second = sync_dropbox(tmp_path, client)

    assert second.conflicts == 1
    assert local.read_bytes() == b"%PDF-local-edit"
    assert client.data["papers/paper.pdf"] == b"%PDF-remote-edit"
    assert list((tmp_path / ".jarvis/conflicts").glob("*.json"))


def test_fresh_clone_replaces_metadata_only_sidecar_from_canonical_pair(tmp_path):
    local_sidecar = tmp_path / "knowledge/papers/paper.pdf.meta.yaml"
    local_sidecar.parent.mkdir(parents=True)
    local_sidecar.write_bytes(b"title: Git metadata\ntags: []\n")
    client = FakeDropbox(
        {
            "papers/paper.pdf": b"%PDF-remote",
            "papers/paper.pdf.meta.yaml": b"title: Dropbox metadata\ntags: [gravity]\n",
        }
    )

    result = sync_dropbox(tmp_path, client)

    assert result.downloaded == 2
    assert (tmp_path / "knowledge/papers/paper.pdf").read_bytes() == b"%PDF-remote"
    assert local_sidecar.read_bytes() == b"title: Dropbox metadata\ntags: [gravity]\n"


def test_dropbox_deletion_is_reported_without_deleting_or_resurrecting(tmp_path):
    local = write_pdf(tmp_path, b"%PDF-shared")
    client = FakeDropbox({"papers/paper.pdf": b"%PDF-shared"})
    sync_dropbox(tmp_path, client)
    del client.data["papers/paper.pdf"]
    del client.revisions["papers/paper.pdf"]

    result = sync_dropbox(tmp_path, client)

    assert result.remote_deletions == 1
    assert local.exists()
    assert "papers/paper.pdf" not in client.data


def test_document_and_sidecar_are_blocked_as_one_conflicting_pair(tmp_path):
    local = write_pdf(tmp_path, b"%PDF-shared")
    sidecar = local.with_name("paper.pdf.meta.yaml")
    sidecar.write_bytes(b"title: Shared\ntags: []\n")
    client = FakeDropbox(
        {
            "papers/paper.pdf": local.read_bytes(),
            "papers/paper.pdf.meta.yaml": sidecar.read_bytes(),
        }
    )
    sync_dropbox(tmp_path, client)
    local.write_bytes(b"%PDF-local-edit")
    client.data["papers/paper.pdf.meta.yaml"] = b"title: Remote edit\ntags: []\n"
    client.revisions["papers/paper.pdf.meta.yaml"] = "2"

    result = sync_dropbox(tmp_path, client)

    assert result.uploaded == result.downloaded == 0
    assert result.conflicts == 2
    assert client.data["papers/paper.pdf"] == b"%PDF-shared"
    assert sidecar.read_bytes() == b"title: Shared\ntags: []\n"


def test_one_sided_changes_propagate_with_revision_guards(tmp_path):
    local = write_pdf(tmp_path, b"%PDF-shared")
    client = FakeDropbox({"papers/paper.pdf": b"%PDF-shared"})
    sync_dropbox(tmp_path, client)

    local.write_bytes(b"%PDF-local-new")
    uploaded = sync_dropbox(tmp_path, client)
    assert uploaded.uploaded == 1
    assert client.data["papers/paper.pdf"] == b"%PDF-local-new"

    client.data["papers/paper.pdf"] = b"%PDF-remote-new"
    client.revisions["papers/paper.pdf"] = "3"
    downloaded = sync_dropbox(tmp_path, client)
    assert downloaded.downloaded == 1
    assert local.read_bytes() == b"%PDF-remote-new"


def test_invalid_remote_update_cannot_replace_valid_local_document(tmp_path):
    local = write_pdf(tmp_path, b"%PDF-valid")
    client = FakeDropbox({"papers/paper.pdf": b"%PDF-valid"})
    sync_dropbox(tmp_path, client)
    client.data["papers/paper.pdf"] = b"not a pdf"
    client.revisions["papers/paper.pdf"] = "2"

    with pytest.raises(ValueError, match="Invalid Dropbox PDF header"):
        sync_dropbox(tmp_path, client)
    assert local.read_bytes() == b"%PDF-valid"


def test_dry_run_has_no_local_side_effects(tmp_path):
    local = write_pdf(tmp_path)

    result = sync_dropbox(tmp_path, FakeDropbox(), dry_run=True)

    assert result.uploaded == 1
    assert not local.with_name("paper.pdf.meta.yaml").exists()
    assert not (tmp_path / ".jarvis").exists()


def test_conflict_resolution_rejects_paths_outside_category(tmp_path):
    with pytest.raises(ValueError, match="managed document"):
        resolve_conflict(tmp_path, FakeDropbox(), "papers/../../../escape.pdf", "dropbox")
