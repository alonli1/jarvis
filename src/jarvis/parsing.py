from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from pathlib import Path

import yaml
from pypdf import PdfReader

from .models import Chunk
from .taxonomy import expanded_tags, load_taxonomy

SUPPORTED_SUFFIXES = {".pdf", ".tex", ".md", ".txt"}
REFERENCE_MANIFEST = "references.yaml"
SECTION_HEADING = re.compile(
    r"^(?:(?:\d+(?:\.\d+)*)\s+[A-Z][^.]{2,80}|"
    r"(?i:abstract|introduction|background|methods?|formalism|setup|results?|discussion|"
    r"conclusions?|appendix(?:\s+[a-z])?|references)|[A-Z][A-Z0-9 ,:()\-]{2,80})$"
)


def load_sidecar(path: Path) -> dict:
    sidecar = path.with_name(path.name + ".meta.yaml")
    if not sidecar.exists():
        return {}
    with sidecar.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def stable_chunk_id(source_path: str, page: int | None, index: int, text: str) -> str:
    payload = f"{source_path}|{page}|{index}|{text[:250]}".encode("utf-8", errors="ignore")
    return hashlib.sha256(payload).hexdigest()


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        return []
    if len(text) <= size:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            cut = max(text.rfind("\n\n", start, end), text.rfind(". ", start, end))
            if cut > start + size // 2:
                end = cut + 1
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return [c for c in chunks if c]


def _tex_to_text(raw: str) -> str:
    raw = re.sub(r"(?<!\\)%.*", "", raw)
    raw = re.sub(r"\\(?:begin|end)\{[^}]+\}", "\n", raw)
    raw = re.sub(r"\\(?:section|subsection|subsubsection)\*?\{([^}]*)\}", r"\n\n\1\n", raw)
    raw = re.sub(r"\\cite\{([^}]*)\}", r" [cite:\1] ", raw)
    raw = re.sub(r"\\label\{([^}]*)\}", r" [label:\1] ", raw)
    return raw


def split_sections(
    text: str, current: str | None = None
) -> tuple[list[tuple[str | None, str]], str | None]:
    sections: list[tuple[str | None, str]] = []
    buffer: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        heading = bool(line and len(line) <= 100 and SECTION_HEADING.fullmatch(line))
        if heading:
            if any(part.strip() for part in buffer):
                sections.append((current, "\n".join(buffer)))
            current, buffer = line, []
        else:
            buffer.append(raw_line)
    if any(part.strip() for part in buffer):
        sections.append((current, "\n".join(buffer)))
    return sections, current


def _reference_chunks(path: Path, rel: str, repo_root: Path) -> Iterable[Chunk]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    references = data.get("references", []) if isinstance(data, dict) else data
    if not isinstance(references, list):
        raise TypeError(f"{path} must contain a references list")
    taxonomy = load_taxonomy(repo_root)

    for index, reference in enumerate(references):
        if not isinstance(reference, dict) or not reference.get("title"):
            raise ValueError(f"Invalid reference at index {index} in {path}")
        authors = reference.get("authors", [])
        topics = reference.get("topics", [])
        if not isinstance(authors, list) or not isinstance(topics, list):
            raise TypeError(f"Reference {index} in {path} must use lists for authors and topics")
        authors = [str(author) for author in authors]
        topics = [str(topic) for topic in topics]
        tags = expanded_tags(
            topics,
            taxonomy,
            f"{reference['title']} {reference.get('why', '')}",
        )
        lines = [
            str(reference["title"]),
            f"Authors: {', '.join(authors)}",
            f"Year: {reference.get('year', '')}",
            f"Topics: {', '.join(topics)}",
            f"Research tags: {', '.join(tag for tag in tags if tag not in topics)}",
            f"Corpus role: {reference.get('why', '')}",
        ]
        lines.extend(
            f"{label}: {reference[key]}"
            for key, label in (("arxiv", "arXiv"), ("doi", "DOI"), ("url", "URL"))
            if reference.get(key)
        )
        text = "\n".join(lines)
        metadata = {
            key: reference[key]
            for key in ("id", "tier", "type", "year", "arxiv", "doi", "url", "ingest_policy")
            if reference.get(key) is not None
        }
        metadata["format"] = "reference_manifest"
        yield Chunk(
            id=stable_chunk_id(rel, None, index, text),
            text=text,
            source_path=rel,
            title=str(reference["title"]),
            tags=tags,
            metadata=metadata,
        )


def iter_document_chunks(
    path: Path, repo_root: Path, chunk_chars: int, overlap: int
) -> Iterable[Chunk]:
    rel = str(path.resolve().relative_to(repo_root.resolve()))
    if path.name == REFERENCE_MANIFEST:
        yield from _reference_chunks(path, rel, repo_root)
        return

    sidecar = load_sidecar(path)
    title = sidecar.get("title", path.stem)
    tags = sidecar.get("tags", [])
    if not isinstance(tags, list):
        raise TypeError(f"tags in {path.name}.meta.yaml must be a list")
    extra_metadata = {
        key: value for key, value in sidecar.items() if key not in {"visibility", "title", "tags"}
    }

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        current_section: str | None = None
        for page_no, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            sections, current_section = split_sections(text, current_section)
            index = 0
            for section, section_text in sections:
                for piece in chunk_text(section_text, chunk_chars, overlap):
                    yield Chunk(
                        id=stable_chunk_id(rel, page_no, index, piece),
                        text=piece,
                        source_path=rel,
                        title=title,
                        page=page_no,
                        section=section,
                        tags=tags,
                        metadata={"format": "pdf", **extra_metadata},
                    )
                    index += 1
        return

    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".tex":
        raw = _tex_to_text(raw)
    for idx, piece in enumerate(chunk_text(raw, chunk_chars, overlap)):
        yield Chunk(
            id=stable_chunk_id(rel, None, idx, piece),
            text=piece,
            source_path=rel,
            title=title,
            tags=tags,
            metadata={"format": path.suffix.lower().lstrip("."), **extra_metadata},
        )


def discover_documents(path: Path) -> list[Path]:
    if path.is_file():
        return (
            [path]
            if path.suffix.lower() in SUPPORTED_SUFFIXES or path.name == REFERENCE_MANIFEST
            else []
        )
    return sorted(
        p
        for p in path.rglob("*")
        if p.is_file()
        and (p.suffix.lower() in SUPPORTED_SUFFIXES or p.name == REFERENCE_MANIFEST)
        and ".jarvis" not in p.parts
    )
