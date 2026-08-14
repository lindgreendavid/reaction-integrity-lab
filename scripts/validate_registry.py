"""Validate fixed source identities and interpretation boundaries."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    provenance = json.loads((ROOT / "data" / "provenance.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "reports" / "v0.1-source-audit.json").read_text(encoding="utf-8"))
    split_audit = json.loads(
        (ROOT / "reports" / "v0.1-split-audit.json").read_text(encoding="utf-8")
    )
    assert provenance["doi"] == "10.6084/m9.figshare.23298467.v4"
    assert sum(file["size_bytes"] for file in provenance["files"]) == 394_497_018
    assert all(len(file["md5"]) == 32 for file in provenance["files"])
    assert registry["published_reference_results_percent"]["independently_reproduced_here"] is False
    assert registry["published_pipeline_audit"]["independently_reproduced_here"] is False
    assert set(registry["published_reference_results_percent"].values()) >= {44, 47, 21, 24}
    assert split_audit["train_rows"] + split_audit["test_rows"] == 691_142
    assert split_audit["overlapping_test_inputs"] == 0
    assert split_audit["cross_split_duplicate_records"] == 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
