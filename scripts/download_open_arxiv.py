#!/usr/bin/env python3
"""Download official arXiv PDFs selected by the Jarvis seed manifest."""

from __future__ import annotations

import argparse
import re
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

from jarvis.taxonomy import expanded_tags, load_taxonomy

ROOT = Path(__file__).resolve().parents[1]
GENERATED_BY = "scripts/download_open_arxiv.py"


def safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value.replace("/", "_")).strip("_")


def write_sidecar(destination: Path, reference: dict, taxonomy: dict[str, dict]) -> None:
    sidecar = destination.with_name(destination.name + ".meta.yaml")
    if sidecar.exists():
        current = yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}
        if current.get("generated_by") != GENERATED_BY:
            print(f"  preserve custom metadata {sidecar.name}")
            return
    raw_tags = [str(tag) for tag in reference.get("topics", [])]
    data = {
        "generated_by": GENERATED_BY,
        "visibility": "public",
        "title": reference["title"],
        "tags": expanded_tags(
            raw_tags,
            taxonomy,
            f"{reference['title']} {reference.get('why', '')}",
        ),
        "reference_id": reference["id"],
        "tier": reference["tier"],
        "authors": reference.get("authors", []),
        "year": reference.get("year"),
        "arxiv": reference.get("arxiv"),
        "doi": reference.get("doi"),
        "url": reference.get("url"),
    }
    sidecar.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "knowledge/references.yaml")
    parser.add_argument("--out", type=Path, default=ROOT / "knowledge/papers")
    parser.add_argument("--tier", action="append", choices=["T0", "T1", "T2"])
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    data = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    tiers = set(args.tier or ["T0"])
    selected = [
        reference
        for reference in data["references"]
        if reference["tier"] in tiers
        and reference.get("arxiv")
        and reference["ingest_policy"] == "download_arxiv"
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    taxonomy = load_taxonomy(ROOT)
    print(f"Selected {len(selected)} arXiv records from {sorted(tiers)}")

    for number, reference in enumerate(selected, 1):
        arxiv_id = reference["arxiv"]
        destination = args.out / safe_filename(f"{reference['id']}__{arxiv_id}.pdf")
        if destination.exists() and not args.overwrite:
            write_sidecar(destination, reference, taxonomy)
            print(f"[{number}/{len(selected)}] skip {destination.name}")
            continue

        print(f"[{number}/{len(selected)}] {arxiv_id} -> {destination.name}")
        temporary = destination.with_suffix(".pdf.part")
        try:
            request = urllib.request.Request(
                f"https://arxiv.org/pdf/{arxiv_id}",
                headers={"User-Agent": "Jarvis-literature-seed/1.0"},
            )
            with (
                urllib.request.urlopen(request, timeout=60) as response,
                temporary.open("wb") as output,
            ):
                shutil.copyfileobj(response, output)
            with temporary.open("rb") as downloaded:
                if downloaded.read(5) != b"%PDF-":
                    raise ValueError("response is not a PDF")
            temporary.replace(destination)
            write_sidecar(destination, reference, taxonomy)
        except (OSError, ValueError, urllib.error.URLError) as exc:
            temporary.unlink(missing_ok=True)
            print(f"  ERROR: {exc}")
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
