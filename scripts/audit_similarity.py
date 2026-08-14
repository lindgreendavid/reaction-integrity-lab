"""Run the prespecified v1 chemical-similarity and provenance audit."""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow.parquet as pq
from rdkit import RDLogger

from reaction_integrity_lab.similarity import (
    canonical_smiles,
    maximum_tanimoto,
    morgan_fingerprint,
    murcko_scaffold,
    wilson_interval,
)

ROOT = Path(__file__).resolve().parents[1]
SEED = 20_260_814
SAMPLE_SIZE = 1_000
THRESHOLDS = (0.7, 0.8, 0.9, 1.0)


def fraction(successes: int, total: int) -> float:
    return successes / total if total else 0.0


def years(values: list[Any]) -> list[int]:
    return [value.year for value in values if value is not None]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "external" / "paper-v3" / "condition_prediction_datasets",
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports" / "v1-similarity-audit.json"
    )
    args = parser.parse_args()
    train_path = args.data_dir / "orderly_no_trust_no_map_train.parquet"
    test_path = args.data_dir / "orderly_no_trust_no_map_test.parquet"
    columns = ["original_index", "product_000", "extracted_from_file", "grant_date"]
    train = pq.read_table(train_path, columns=columns).to_pydict()
    test = pq.read_table(test_path, columns=columns).to_pydict()

    RDLogger.DisableLog("rdApp.error")
    raw_train_products = train["product_000"]
    raw_test_products = test["product_000"]
    canonical_cache = {
        value: canonical_smiles(value) for value in set(raw_train_products + raw_test_products)
    }
    train_products = {canonical_cache[value] for value in raw_train_products}
    train_products.discard(None)
    valid_test_products = [canonical_cache[value] for value in raw_test_products]
    valid_test_count = sum(value is not None for value in valid_test_products)
    identity_overlap = sum(value in train_products for value in valid_test_products if value)

    scaffold_cache = {value: murcko_scaffold(value) for value in canonical_cache.values() if value}
    train_scaffolds = {scaffold_cache[value] for value in train_products}
    train_scaffolds.discard(None)
    test_scaffolds = [scaffold_cache[value] for value in valid_test_products if value]
    valid_test_scaffold_count = sum(value is not None for value in test_scaffolds)
    scaffold_overlap = sum(value in train_scaffolds for value in test_scaffolds if value)

    train_sources = {value for value in train["extracted_from_file"] if value}
    test_sources = test["extracted_from_file"]
    valid_test_source_count = sum(bool(value) for value in test_sources)
    source_overlap = sum(value in train_sources for value in test_sources if value)

    train_years = years(train["grant_date"])
    test_years = years(test["grant_date"])
    later_than_train = sum(value > max(train_years) for value in test_years)

    rng = np.random.default_rng(SEED)
    sample_positions = sorted(
        rng.choice(len(raw_test_products), SAMPLE_SIZE, replace=False).tolist()
    )
    unique_train_products = sorted(train_products)
    train_fingerprints = [
        fingerprint
        for value in unique_train_products
        if (fingerprint := morgan_fingerprint(value)) is not None
    ]
    sampled: list[dict[str, int | float]] = []
    for position in sample_positions:
        product = valid_test_products[position]
        fingerprint = morgan_fingerprint(product)
        if fingerprint is None:
            continue
        sampled.append(
            {
                "row_position": position,
                "original_index": int(test["original_index"][position]),
                "maximum_tanimoto": maximum_tanimoto(fingerprint, train_fingerprints),
            }
        )
    similarities = [float(item["maximum_tanimoto"]) for item in sampled]
    threshold_results = {}
    for threshold in THRESHOLDS:
        successes = sum(value >= threshold for value in similarities)
        threshold_results[str(threshold)] = wilson_interval(successes, len(similarities)).to_dict()

    payload = {
        "schema_version": "1.0.0",
        "generated_utc": datetime.now(UTC).isoformat(),
        "study_type": "prespecified secondary representation-overlap audit",
        "dataset_variant": "reaction-string role assignment; delete rare reactions",
        "method": {
            "rdkit_version": "2026.03.5",
            "product_identity": "canonical isomeric SMILES",
            "scaffold": "Bemis-Murcko; empty acyclic scaffolds excluded",
            "fingerprint": "Morgan radius 2; 2048 bits",
            "similarity": "Tanimoto",
            "sample_seed": SEED,
            "sample_size_requested": SAMPLE_SIZE,
            "thresholds": list(THRESHOLDS),
        },
        "row_counts": {"train": len(raw_train_products), "test": len(raw_test_products)},
        "product_identity": {
            "unique_valid_train": len(train_products),
            "valid_test_rows": valid_test_count,
            "invalid_or_missing_test_rows": len(raw_test_products) - valid_test_count,
            "overlapping_test_rows": identity_overlap,
            "overlapping_test_fraction": fraction(identity_overlap, valid_test_count),
        },
        "product_scaffold": {
            "unique_nonempty_train": len(train_scaffolds),
            "valid_nonempty_test_rows": valid_test_scaffold_count,
            "scaffoldless_or_invalid_test_rows": len(raw_test_products) - valid_test_scaffold_count,
            "overlapping_test_rows": scaffold_overlap,
            "overlapping_test_fraction": fraction(scaffold_overlap, valid_test_scaffold_count),
        },
        "source_file_provenance": {
            "unique_train_values": len(train_sources),
            "valid_test_rows": valid_test_source_count,
            "overlapping_test_rows": source_overlap,
            "overlapping_test_fraction": fraction(source_overlap, valid_test_source_count),
        },
        "grant_date": {
            "valid_train_rows": len(train_years),
            "valid_test_rows": len(test_years),
            "train_min_year": min(train_years),
            "train_median_year": statistics.median(train_years),
            "train_max_year": max(train_years),
            "test_min_year": min(test_years),
            "test_median_year": statistics.median(test_years),
            "test_max_year": max(test_years),
            "test_rows_later_than_latest_train": later_than_train,
            "test_fraction_later_than_latest_train": fraction(later_than_train, len(test_years)),
        },
        "sampled_product_similarity": {
            "valid_sample_rows": len(similarities),
            "minimum": min(similarities),
            "median": statistics.median(similarities),
            "mean": statistics.fmean(similarities),
            "maximum": max(similarities),
            "threshold_results": threshold_results,
            "rows": sampled,
        },
        "interpretation_boundary": (
            "Measures product representation, scaffold, source-file, and grant-date overlap. It "
            "does not establish patent-family leakage, mechanistic equivalence, causation, or "
            "prospective model performance. Fingerprint results estimate a sampled test-row "
            "proportion rather than a full-population nearest-neighbor census."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
