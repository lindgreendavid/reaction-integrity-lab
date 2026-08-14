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
    baselines = json.loads((ROOT / "reports" / "v0.2-baselines.json").read_text(encoding="utf-8"))
    assert provenance["doi"] == "10.6084/m9.figshare.23298467.v4"
    assert sum(file["size_bytes"] for file in provenance["files"]) == 394_497_018
    assert all(len(file["md5"]) == 32 for file in provenance["files"])
    assert provenance["supplement"]["md5"] == "4a99b6e3678e4ac312678e26fd3caec2"
    assert registry["published_reference_results_percent"]["independently_reproduced_here"] is False
    assert registry["published_pipeline_audit"]["independently_reproduced_here"] is False
    values = registry["published_reference_results_percent"]
    assert {
        values["trusted_labels_rare_to_other"],
        values["trusted_labels_delete_rare_reaction"],
        values["reaction_string_rare_to_other"],
        values["reaction_string_delete_rare_reaction"],
    } == {67, 68, 35, 36}
    assert split_audit["train_rows"] + split_audit["test_rows"] == 691_142
    assert split_audit["overlapping_test_inputs"] == 0
    assert split_audit["cross_split_duplicate_records"] == 0
    assert baselines["complete"] is True
    assert set(baselines["results"]) == {
        "trusted_labels_rare_to_other",
        "trusted_labels_delete_rare",
        "reaction_string_rare_to_other",
        "reaction_string_delete_rare",
    }
    assert all(
        result["absolute_deviation_percentage_points"] <= 1.0
        for result in baselines["results"].values()
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
