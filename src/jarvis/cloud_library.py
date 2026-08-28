from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

import yaml

from .dropbox_client import DropboxClient, RemoteFile
from .library_sync import (
    CATEGORIES,
    GENERATED_BY,
    SUPPORTED_SUFFIXES,
    _atomic_copy,
    _atomic_yaml,
    _destination,
    _digest,
    _read_metadata,
    _sidecar,
    _validate_document,
)
from .taxonomy import expanded_tags, load_taxonomy

STATE_VERSION = 1


@dataclass(frozen=True)
class SyncAction:
    relative: str
    action: str
    detail: str = ""


@dataclass(frozen=True)
class CloudSyncResult:
    actions: tuple[SyncAction, ...]
    uploaded: int
    downloaded: int
    unchanged: int
    conflicts: int
    remote_deletions: int
    changed_local: tuple[Path, ...] = ()

    @property
    def pending(self) -> int:
        return self.uploaded + self.downloaded + self.conflicts


def _state_path(root: Path) -> Path:
    return root / ".jarvis" / "library-state.json"


def _load_state(root: Path) -> dict:
    path = _state_path(root)
    if not path.exists():
        return {"version": STATE_VERSION, "files": {}}
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("version") != STATE_VERSION or not isinstance(state.get("files"), dict):
        raise ValueError(f"Unsupported library state: {path}")
    return state


def _save_state(root: Path, state: dict) -> None:
    path = _state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(UTC).isoformat()
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")
        temporary = Path(f.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def dropbox_content_hash(path: Path) -> str:
    blocks = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            blocks.update(hashlib.sha256(block).digest())
    return blocks.hexdigest()


def _is_supported(relative: str) -> bool:
    path = PurePosixPath(relative)
    if (
        path.is_absolute()
        or len(path.parts) < 2
        or path.parts[0] not in CATEGORIES
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        return False
    name = path.name
    if name.endswith(".meta.yaml"):
        name = name.removesuffix(".meta.yaml")
    return Path(name).suffix.lower() in SUPPORTED_SUFFIXES


def _pair_key(relative: str) -> str:
    return relative.removesuffix(".meta.yaml")


def _local_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if len(path.parts) < 2 or path.parts[0] not in CATEGORIES:
        raise ValueError(f"Invalid library path: {relative}")
    category, parts = path.parts[0], path.parts[1:]
    sidecar = parts[-1].endswith(".meta.yaml")
    doc_parts = (*parts[:-1], parts[-1].removesuffix(".meta.yaml")) if sidecar else parts
    destination = _destination(root, category, Path(*doc_parts))
    return _sidecar(destination) if sidecar else destination


def _remote_relative(root: Path, local: Path) -> str:
    mappings = {
        root / "knowledge" / "papers": "papers",
        root / "knowledge" / "books": "books",
        root / "knowledge" / "notes": "notes",
        root / "group" / "manuscripts": "manuscripts",
    }
    candidate = local.resolve(strict=False)
    for folder, category in mappings.items():
        try:
            relative = candidate.relative_to(folder.resolve(strict=False))
        except ValueError:
            continue
        return str(PurePosixPath(category, *relative.parts))
    raise ValueError(f"Path is outside the managed library: {local}")


def _minimal_metadata(root: Path, document: Path, relative: str) -> dict:
    taxonomy = load_taxonomy(root)
    title = document.stem
    return {
        "generated_by": GENERATED_BY,
        "title": title,
        "authors": [],
        "tags": expanded_tags([], taxonomy, title),
        "storage_provider": "dropbox",
        "storage_path": relative,
        "storage_id": f"sha256:{_digest(document)}",
        "bibliographic_status": "needs-curation",
    }


def _ensure_sidecars(root: Path) -> list[Path]:
    written = []
    for category in CATEGORIES:
        folder = _local_path(root, f"{category}/placeholder").parent
        if not folder.exists():
            continue
        for document in sorted(folder.rglob("*")):
            if not document.is_file() or document.name.endswith(".meta.yaml"):
                continue
            if document.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue
            sidecar = _sidecar(document)
            if not sidecar.exists():
                relative = _remote_relative(root, document)
                _atomic_yaml(sidecar, _minimal_metadata(root, document, relative))
                written.append(sidecar)
    return written


def _local_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for category in CATEGORIES:
        folder = _local_path(root, f"{category}/placeholder").parent
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or ".jarvis-conflict" in path.name:
                continue
            relative = _remote_relative(root, path)
            if _is_supported(relative):
                files[relative] = path
    return files


def _remote_files(client: DropboxClient) -> dict[str, RemoteFile]:
    return {path: item for path, item in client.list_files().items() if _is_supported(path)}


def plan_sync(root: Path, client: DropboxClient) -> tuple[list[SyncAction], dict, dict, dict]:
    state = _load_state(root)
    local = _local_files(root)
    remote = _remote_files(client)
    actions: list[SyncAction] = []
    previous = state["files"]
    for relative in sorted(local.keys() | remote.keys() | previous.keys()):
        local_path, remote_file, prior = (
            local.get(relative),
            remote.get(relative),
            previous.get(relative),
        )
        if local_path and remote_file:
            sha = _digest(local_path)
            same_content = bool(remote_file.content_hash) and (
                dropbox_content_hash(local_path) == remote_file.content_hash
            )
            if same_content:
                actions.append(SyncAction(relative, "unchanged"))
                continue
            if not prior:
                document = _pair_key(relative)
                if relative.endswith(".meta.yaml") and document not in local and document in remote:
                    actions.append(SyncAction(relative, "download", "fresh-clone Dropbox pair"))
                else:
                    actions.append(SyncAction(relative, "conflict", "untracked versions differ"))
                continue
            local_changed = sha != prior.get("local_sha256")
            remote_changed = remote_file.rev != prior.get("dropbox_rev")
            if local_changed and remote_changed:
                actions.append(SyncAction(relative, "conflict", "both versions changed"))
            elif local_changed:
                actions.append(SyncAction(relative, "upload", "local version changed"))
            elif remote_changed:
                actions.append(SyncAction(relative, "download", "Dropbox version changed"))
            else:
                actions.append(
                    SyncAction(relative, "conflict", "content differs without revision change")
                )
        elif local_path:
            action = "remote-deleted" if prior else "upload"
            detail = "Dropbox deletion preserved for review" if prior else "new local file"
            actions.append(SyncAction(relative, action, detail))
        elif remote_file:
            actions.append(SyncAction(relative, "download", "local file missing"))
        else:
            actions.append(SyncAction(relative, "removed-both"))
    return actions, state, local, remote


def _record(remote: RemoteFile, local: Path) -> dict:
    return {
        "dropbox_id": remote.id,
        "dropbox_rev": remote.rev,
        "dropbox_content_hash": remote.content_hash,
        "server_modified": remote.server_modified,
        "local_sha256": _digest(local),
    }


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        stream.write(content)
        temporary = Path(stream.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _validate_download(relative: str, content: bytes) -> None:
    if not content:
        raise ValueError(f"Empty Dropbox document: {relative}")
    if relative.endswith(".meta.yaml"):
        data = yaml.safe_load(content.decode("utf-8")) or {}
        if not isinstance(data, dict):
            raise TypeError(f"Dropbox sidecar must contain a mapping: {relative}")
        for key in ("authors", "tags"):
            if key in data and not isinstance(data[key], list):
                raise TypeError(f"{key} in Dropbox sidecar must be a list: {relative}")
    elif Path(relative).suffix.lower() == ".pdf" and not content.startswith(b"%PDF-"):
        raise ValueError(f"Invalid Dropbox PDF header: {relative}")


def _write_conflicts(root: Path, actions: list[SyncAction]) -> Path | None:
    conflicts = [asdict(action) for action in actions if action.action == "conflict"]
    if not conflicts:
        return None
    folder = root / ".jarvis" / "conflicts"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%fZ')}.json"
    path.write_text(json.dumps({"conflicts": conflicts}, indent=2) + "\n", encoding="utf-8")
    return path


def sync_dropbox(root: Path, client: DropboxClient, dry_run: bool = False) -> CloudSyncResult:
    root = root.resolve()
    if not dry_run:
        _ensure_sidecars(root)
    actions, state, local, remote = plan_sync(root, client)
    directions: dict[str, set[str]] = {}
    for action in actions:
        if action.action in {"upload", "download"}:
            directions.setdefault(_pair_key(action.relative), set()).add(action.action)
    mixed_pairs = {pair for pair, values in directions.items() if len(values) > 1}
    actions = [
        SyncAction(action.relative, "conflict", "document and sidecar changed on opposite sides")
        if _pair_key(action.relative) in mixed_pairs and action.action in {"upload", "download"}
        else action
        for action in actions
    ]
    conflicted_pairs = {
        _pair_key(action.relative) for action in actions if action.action == "conflict"
    }
    actions = [
        SyncAction(action.relative, "blocked", "associated document or sidecar conflicts")
        if _pair_key(action.relative) in conflicted_pairs and action.action != "conflict"
        else action
        for action in actions
    ]
    changed: list[Path] = []
    if not dry_run:
        for action in actions:
            relative = action.relative
            if action.action == "upload":
                source = local[relative]
                uploaded = client.upload(
                    relative,
                    source.read_bytes(),
                    remote.get(relative).rev if remote.get(relative) else None,
                )
                state["files"][relative] = _record(uploaded, source)
            elif action.action == "download":
                destination = _local_path(root, relative)
                item = remote[relative]
                content = client.download(item.path)
                _validate_download(relative, content)
                _atomic_bytes(destination, content)
                if not relative.endswith(".meta.yaml"):
                    changed.append(destination)
                state["files"][relative] = _record(item, destination)
            elif action.action == "unchanged":
                state["files"][relative] = _record(remote[relative], local[relative])
            elif action.action == "removed-both":
                state["files"].pop(relative, None)
        _write_conflicts(root, actions)
        _save_state(root, state)
    return CloudSyncResult(
        actions=tuple(actions),
        uploaded=sum(a.action == "upload" for a in actions),
        downloaded=sum(a.action == "download" for a in actions),
        unchanged=sum(a.action == "unchanged" for a in actions),
        conflicts=sum(a.action == "conflict" for a in actions),
        remote_deletions=sum(a.action == "remote-deleted" for a in actions),
        changed_local=tuple(changed),
    )


def add_document(
    root: Path, source: Path, category: str, client: DropboxClient
) -> tuple[Path, CloudSyncResult]:
    if category not in CATEGORIES:
        raise ValueError(f"category must be one of: {', '.join(CATEGORIES)}")
    source = source.expanduser().resolve(strict=True)
    if not source.is_file() or source.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported library document: {source}")
    _validate_document(source, source.parent)
    _read_metadata(source)
    destination = _destination(root.resolve(), category, Path(source.name))
    if destination.exists() and _digest(destination) != _digest(source):
        raise FileExistsError(f"A different document already exists at {destination}")
    if source != destination.resolve(strict=False):
        _atomic_copy(source, destination)
    source_sidecar = _sidecar(source)
    destination_sidecar = _sidecar(destination)
    if source_sidecar.exists() and source_sidecar != destination_sidecar:
        _atomic_copy(source_sidecar, destination_sidecar)
    if not destination_sidecar.exists():
        _atomic_yaml(
            destination_sidecar,
            _minimal_metadata(root, destination, _remote_relative(root, destination)),
        )
    return destination, sync_dropbox(root, client)


def resolve_conflict(
    root: Path, client: DropboxClient, relative: str, strategy: str
) -> tuple[Path, ...]:
    relative = relative.strip("/")
    if not _is_supported(relative) or relative.endswith(".meta.yaml"):
        raise ValueError("PATH must identify a managed document, for example papers/work.pdf")
    local_doc = _local_path(root, relative)
    local_sidecar = _sidecar(local_doc)
    remote = _remote_files(client)
    selected = [relative, relative + ".meta.yaml"]
    changed: list[Path] = []
    if strategy == "local":
        for item in selected:
            path = _local_path(root, item)
            if path.exists():
                client.upload(item, path.read_bytes(), remote[item].rev if item in remote else None)
    elif strategy == "dropbox":
        for item in selected:
            if item in remote:
                path = _local_path(root, item)
                content = client.download(remote[item].path)
                _validate_download(item, content)
                _atomic_bytes(path, content)
                changed.append(path)
    elif strategy == "keep-both":
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        backup_doc = local_doc.with_name(f"{local_doc.stem}.local-{stamp}{local_doc.suffix}")
        backup_sidecar = _sidecar(backup_doc)
        if local_doc.exists():
            shutil.move(local_doc, backup_doc)
        if local_sidecar.exists():
            shutil.move(local_sidecar, backup_sidecar)
        for item in selected:
            if item in remote:
                path = _local_path(root, item)
                content = client.download(remote[item].path)
                _validate_download(item, content)
                _atomic_bytes(path, content)
                changed.append(path)
    else:
        raise ValueError("strategy must be local, dropbox, or keep-both")
    state = _load_state(root)
    refreshed = _remote_files(client)
    for item in selected:
        path = _local_path(root, item)
        if item in refreshed and path.exists():
            state["files"][item] = _record(refreshed[item], path)
    _save_state(root, state)
    return tuple(changed)
