"""Download and verify frozen ORDerly condition benchmark files."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "data" / "provenance.json"


def md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(file: dict[str, Any], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(file["download_url"], destination)
    actual = md5(destination)
    if actual != file["md5"]:
        destination.unlink(missing_ok=True)
        raise RuntimeError(f"checksum mismatch for {destination.name}: {actual}")


def extract_verified_archive(archive: Path, destination: Path) -> None:
    """Extract the checksum-verified supplement without allowing path traversal."""

    destination_root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination_root):
                raise RuntimeError(f"unsafe archive member: {member.filename}")
        bundle.extractall(destination)


def main() -> int:
    command = argparse.ArgumentParser()
    command.add_argument("--output", type=Path, default=ROOT / "data" / "external")
    command.add_argument(
        "--include-supplement",
        action="store_true",
        help="also fetch and extract the four-variant v3 condition archive",
    )
    args = command.parse_args()
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    for file in provenance["files"]:
        target = args.output / file["name"]
        if target.exists() and md5(target) == file["md5"]:
            continue
        download(file, target)
    if args.include_supplement:
        supplement = provenance["supplement"]
        archive = args.output / supplement["archive_name"]
        if not archive.exists() or md5(archive) != supplement["md5"]:
            download(supplement, archive)
        extract_verified_archive(archive, args.output / "paper-v3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
