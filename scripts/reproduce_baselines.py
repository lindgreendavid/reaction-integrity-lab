"""Reproduce ORDerly's frequency-informed top-3 condition baselines."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow.parquet as pq

from reaction_integrity_lab.baseline import frequency_informed_baseline

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_COLUMNS = {
    "trusted_labels": (
        "solvent_000",
        "solvent_001",
        "catalyst_000",
        "reagent_000",
        "reagent_001",
    ),
    "reaction_string": (
        "solvent_000",
        "solvent_001",
        "agent_000",
        "agent_001",
        "agent_002",
    ),
}
REFERENCE_PERCENT = {
    "trusted_labels_rare_to_other": 52.0,
    "trusted_labels_delete_rare": 52.0,
    "reaction_string_rare_to_other": 20.0,
    "reaction_string_delete_rare": 20.0,
}


def selected_records(
    path: Path, columns: tuple[str, ...], mask: np.ndarray | None
) -> Iterator[dict[str, Any]]:
    """Stream declared columns, optionally retaining rows selected by a Boolean mask."""

    parquet = pq.ParquetFile(path)
    offset = 0
    for batch in parquet.iter_batches(columns=list(columns), batch_size=65_536):
        size = batch.num_rows
        if mask is not None:
            selected = np.flatnonzero(mask[offset : offset + size])
            batch = batch.take(selected)
        yield from batch.to_pylist()
        offset += size


def upstream_training_mask(
    rows: int, *, seed: int = 12_345, train_val_split: float = 0.8
) -> np.ndarray:
    """Match ORDerly's shuffled 80% training subset of its released train file."""

    rng = np.random.default_rng(seed)
    indices = np.arange(rows)
    rng.shuffle(indices)
    selected = indices[: int(rows * train_val_split)]
    mask = np.zeros(rows, dtype=bool)
    mask[selected] = True
    return mask


def first_existing(data_dir: Path, *names: str) -> Path:
    """Resolve the first available official filename across Figshare releases."""

    candidates = tuple(data_dir / name for name in names)
    return next((path for path in candidates if path.exists()), candidates[0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "external")
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "v0.2-baselines.json")
    parser.add_argument("--upstream-commit", default="77d0d900e369f3b512a44d47c740bd4bcb98fcb6")
    args = parser.parse_args()

    datasets = {
        "reaction_string_delete_rare": (
            first_existing(
                args.data_dir,
                "orderly_no_trust_no_map_train.parquet",
                "orderly_condition_train.parquet",
            ),
            first_existing(
                args.data_dir,
                "orderly_no_trust_no_map_test.parquet",
                "orderly_condition_test.parquet",
            ),
            "reaction_string",
        ),
        "reaction_string_rare_to_other": (
            args.data_dir / "orderly_no_trust_with_map_train.parquet",
            args.data_dir / "orderly_no_trust_with_map_test.parquet",
            "reaction_string",
        ),
        "trusted_labels_delete_rare": (
            args.data_dir / "orderly_with_trust_no_map_train.parquet",
            args.data_dir / "orderly_with_trust_no_map_test.parquet",
            "trusted_labels",
        ),
        "trusted_labels_rare_to_other": (
            args.data_dir / "orderly_with_trust_with_map_train.parquet",
            args.data_dir / "orderly_with_trust_with_map_test.parquet",
            "trusted_labels",
        ),
    }

    results: dict[str, Any] = {}
    for name, (train_path, test_path, representation) in datasets.items():
        if not train_path.exists() or not test_path.exists():
            continue
        train_rows = pq.ParquetFile(train_path).metadata.num_rows
        columns = OUTPUT_COLUMNS[representation]
        result = frequency_informed_baseline(
            selected_records(train_path, columns, upstream_training_mask(train_rows)),
            selected_records(test_path, columns, None),
            columns=columns,
            top_n=3,
        )
        result_dict = result.to_dict()
        result_dict["local_percent"] = result.accuracy * 100
        result_dict["published_percent"] = REFERENCE_PERCENT[name]
        result_dict["absolute_deviation_percentage_points"] = abs(
            result.accuracy * 100 - REFERENCE_PERCENT[name]
        )
        results[name] = result_dict

    payload = {
        "schema_version": "0.2.0",
        "generated_utc": datetime.now(UTC).isoformat(),
        "study_type": "known-result computational reproduction",
        "upstream_commit": args.upstream_commit,
        "reference_implementation": (
            "condition_prediction.run.ConditionPrediction.get_frequency_informed_guess"
        ),
        "split": {"seed": 12_345, "train_val_split": 0.8, "train_fraction": 1.0},
        "endpoint": "top-3 exact-match combined solvent-and-agent frequency baseline",
        "results": results,
        "complete": len(results) == 4,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
