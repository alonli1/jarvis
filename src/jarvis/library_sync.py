from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

from .taxonomy import expanded_tags, load_taxonomy

GENERATED_BY = "jarvis.library_sync"
CATEGORIES = ("papers", "books", "notes", "manuscripts")
SUPPORTED_SUFFIXES = {".pdf", ".tex", ".md", ".txt"}
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


@dataclass(frozen=True)
class SyncResult:
    documents: int
    copied: int
    updated: int
    unchanged: int
    sidecars_written: int
    sidecars_preserved: int


@dataclass(frozen=True)
class _Item:
    source: Path
    destination: Path
    metadata: dict
    action: str
    preserve_sidecar: bool


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sidecar(path: Path) -> Path:
    return path.with_name(path.name + ".meta.yaml")


def _read_metadata(path: Path) -> dict:
    sidecar = _sidecar(path)
    if not sidecar.exists():
        return {}
    data = yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise TypeError(f"{sidecar} must contain a mapping")
    for key in ("authors", "tags"):
        if key in data and not isinstance(data[key], list):
            raise TypeError(f"{key} in {sidecar} must be a list")
    return data


def _validate_document(path: Path, root: Path) -> None:
    path.resolve(strict=True).relative_to(root.resolve(strict=True))
    if path.stat().st_size == 0:
        raise ValueError(f"Empty library document: {path}")
    if path.suffix.lower() == ".pdf":
        with path.open("rb") as stream:
            if stream.read(5) != b"%PDF-":
                raise ValueError(f"Invalid PDF header: {path}")


def _destination(root: Path, category: str, relative: Path) -> Path:
    if category in {"papers", "books"}:
        return root / "knowledge" / category / relative
    if category == "notes":
        return root / "knowledge" / "notes" / relative
    return root / "group" / "manuscripts" / relative


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
        temporary = Path(stream.name)
    try:
        shutil.copy2(source, temporary)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _atomic_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8"
    ) as stream:
        yaml.safe_dump(data, stream, sort_keys=False, allow_unicode=True)
        temporary = Path(stream.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _plan(root: Path, source_root: Path, provider: str) -> list[_Item]:
    if not source_root.is_dir():
        raise FileNotFoundError(f"Library root does not exist: {source_root}")
    taxonomy = load_taxonomy(root)
    items: list[_Item] = []
    conflicts: list[Path] = []
    destinations: set[Path] = set()
    for category in CATEGORIES:
        folder = source_root / category
        if not folder.exists():
            continue
        if not folder.is_dir():
            raise NotADirectoryError(folder)
        for source in sorted(folder.rglob("*")):
            if not source.is_file():
                continue
            if source.name.endswith(".meta.yaml") or source.name in IGNORED_NAMES:
                continue
            if source.suffix.lower() not in SUPPORTED_SUFFIXES:
                raise ValueError(f"Unsupported library document: {source}")
            _validate_document(source, source_root)
            source_metadata = _read_metadata(source)
            relative = source.relative_to(folder)
            destination = _destination(root, category, relative)
            destination.resolve(strict=False).relative_to(root)
            if destination in destinations:
                raise ValueError(f"Multiple provider documents map to {destination}")
            destinations.add(destination)
            digest = _digest(source)
            raw_tags = [str(tag) for tag in source_metadata.get("tags", [])]
            metadata = {
                key: value
                for key, value in source_metadata.items()
                if key
                not in {
                    "generated_by",
                    "visibility",
                    "storage_provider",
                    "storage_path",
                    "storage_id",
                }
            }
            metadata.update(
                {
                    "generated_by": GENERATED_BY,
                    "title": str(source_metadata.get("title") or source.stem),
                    "authors": [str(author) for author in source_metadata.get("authors", [])],
                    "tags": expanded_tags(
                        raw_tags,
                        taxonomy,
                        f"{source_metadata.get('title', source.stem)} {' '.join(raw_tags)}",
                    ),
                    "storage_provider": provider,
                    "storage_path": str(source.relative_to(source_root)),
                    "storage_id": f"sha256:{digest}",
                }
            )
            target_sidecar = _sidecar(destination)
            current_metadata = _read_metadata(destination) if target_sidecar.exists() else {}
            preserve_sidecar = bool(
                target_sidecar.exists() and current_metadata.get("generated_by") != GENERATED_BY
            )
            if not destination.exists():
                action = "copied"
            elif not destination.is_file():
                conflicts.append(destination)
                continue
            elif _digest(destination) == digest:
                action = "unchanged"
            elif preserve_sidecar or not target_sidecar.exists():
                conflicts.append(destination)
                continue
            else:
                action = "updated"
            items.append(_Item(source, destination, metadata, action, preserve_sidecar))
    if conflicts:
        paths = "\n".join(f"- {path}" for path in conflicts)
        raise FileExistsError(f"Refusing to overwrite locally managed documents:\n{paths}")
    return items


def sync_library(
    root: Path, source_root: Path, provider: str = "synced-folder", dry_run: bool = False
) -> SyncResult:
    provider = provider.strip().lower()
    if not provider:
        raise ValueError("provider must not be empty")
    items = _plan(root.resolve(), source_root.expanduser().resolve(), provider)
    if not dry_run:
        for item in items:
            if item.action != "unchanged":
                _atomic_copy(item.source, item.destination)
            if not item.preserve_sidecar:
                _atomic_yaml(_sidecar(item.destination), item.metadata)
    return SyncResult(
        documents=len(items),
        copied=sum(item.action == "copied" for item in items),
        updated=sum(item.action == "updated" for item in items),
        unchanged=sum(item.action == "unchanged" for item in items),
        sidecars_written=sum(not item.preserve_sidecar for item in items),
        sidecars_preserved=sum(item.preserve_sidecar for item in items),
    )
