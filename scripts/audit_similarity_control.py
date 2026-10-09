"""Run the POST-HOC within-training control for the similarity audit (requires the `chem` extra)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.parquet as pq
from rdkit import RDLogger

from reaction_integrity_lab.control import build_control

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train",
        type=Path,
        default=ROOT
        / "data"
        / "external"
        / "paper-v3"
        / "condition_prediction_datasets"
        / "orderly_no_trust_no_map_train.parquet",
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports" / "post-release-similarity-control.json"
    )
    args = parser.parse_args()
    RDLogger.DisableLog("rdApp.error")
    table = pq.read_table(args.train, columns=["reactant_000", "reactant_001", "product_000"])
    data = table.to_pydict()
    result = build_control(
        [value or "" for value in data["reactant_000"]],
        [value or "" for value in data["reactant_001"]],
        [value or "" for value in data["product_000"]],
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
