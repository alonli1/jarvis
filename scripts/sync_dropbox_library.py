"""Sync a mounted Dropbox-compatible Jarvis library into the local clone."""

from __future__ import annotations

import argparse
from pathlib import Path

from jarvis.library_sync import sync_library

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--provider", default="dropbox")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = sync_library(ROOT, args.source, provider=args.provider, dry_run=args.dry_run)
    print(
        f"Synced {result.documents} documents: {result.copied} new, "
        f"{result.updated} updated, {result.unchanged} unchanged; "
        f"{result.sidecars_preserved} curated sidecars preserved."
    )


if __name__ == "__main__":
    main()
