"""POST-HOC (not preregistered): a within-training control for the similarity audit.

The v1 audit reports that 5.78% of test products occur in training, 80.84% of test product
scaffolds occur in training, and 60.5% of a 1,000-row test sample has a training product at
Tanimoto >= 0.70. It cannot say how much of that is *specific to the released split* rather than
inherent to any random hold-out of this data. This module supplies the missing reference by
applying the same measurements to the training set itself, held out one row at a time:

* a training row's references are the products (or scaffolds) of the other training rows whose
  exact input key (reactant_000, reactant_001, product_000) differs from its own, mirroring the
  released split's property that no test input key occurs in training;
* the same canonical-SMILES identity, Bemis-Murcko scaffold and Morgan radius-2 2,048-bit
  Tanimoto definitions as the frozen audit are used.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

import numpy as np
from rdkit import DataStructs
from rdkit.DataStructs.cDataStructs import ExplicitBitVect

from reaction_integrity_lab.similarity import (
    canonical_smiles,
    morgan_fingerprint,
    murcko_scaffold,
    wilson_interval,
)

CONTROL_SEED = 20_261_009
CONTROL_SAMPLE_SIZE = 1_000
THRESHOLDS = (0.7, 0.8, 0.9, 1.0)

InputKey = tuple[str, str, str]


def _distinct_keys(
    values: Sequence[str | None], keys: Sequence[InputKey]
) -> dict[str, set[InputKey]]:
    table: dict[str, set[InputKey]] = defaultdict(set)
    for value, key in zip(values, keys, strict=True):
        if value is not None:
            table[value].add(key)
    return table


def held_out_overlap(values: Sequence[str | None], keys: Sequence[InputKey]) -> dict[str, float]:
    """Fraction of rows whose value also occurs on a row with a different input key."""

    table = _distinct_keys(values, keys)
    valid = [v for v in values if v is not None]
    hits = sum(1 for v in valid if len(table[v]) >= 2)
    return {
        "valid_rows": len(valid),
        "overlapping_rows": hits,
        "overlapping_fraction": hits / len(valid) if valid else 0.0,
    }


def held_out_similarity_sample(
    products: Sequence[str | None],
    keys: Sequence[InputKey],
    sample_size: int = CONTROL_SAMPLE_SIZE,
    seed: int = CONTROL_SEED,
) -> dict[str, object]:
    """Maximum Tanimoto of sampled training products to other-input-key training products."""

    table = _distinct_keys(products, keys)
    unique = sorted(table)
    fingerprints: list[ExplicitBitVect] = []
    index_of: dict[str, int] = {}
    for product in unique:
        fingerprint = morgan_fingerprint(product)
        if fingerprint is not None:
            index_of[product] = len(fingerprints)
            fingerprints.append(fingerprint)
    rng = np.random.default_rng(seed)
    positions = sorted(rng.choice(len(products), min(sample_size, len(products)), replace=False))
    similarities: list[float] = []
    for position in positions:
        product = products[position]
        if product is None or product not in index_of:
            continue
        scores = DataStructs.BulkTanimotoSimilarity(fingerprints[index_of[product]], fingerprints)
        if len(table[product]) == 1:
            scores[index_of[product]] = -1.0  # its own molecule is not a different-input reference
        similarities.append(float(max(scores)))
    threshold_results = {
        str(t): wilson_interval(sum(s >= t for s in similarities), len(similarities)).to_dict()
        for t in THRESHOLDS
    }
    arr = np.array(similarities)
    return {
        "valid_sample_rows": len(similarities),
        "median": float(np.median(arr)),
        "mean": float(arr.mean()),
        "threshold_results": threshold_results,
    }


def build_control(
    reactant_0: Sequence[str],
    reactant_1: Sequence[str],
    raw_products: Sequence[str],
    sample_size: int = CONTROL_SAMPLE_SIZE,
    seed: int = CONTROL_SEED,
) -> dict[str, object]:
    cache = {value: canonical_smiles(value) for value in set(raw_products)}
    products = [cache[value] for value in raw_products]
    keys = list(zip(reactant_0, reactant_1, raw_products, strict=True))
    scaffold_cache = {value: murcko_scaffold(value) for value in set(products) if value}
    scaffolds = [scaffold_cache.get(value) if value else None for value in products]
    return {
        "schema_version": 1,
        "label": "POST-HOC (not preregistered): within-training control for the similarity audit",
        "seed": seed,
        "rows": len(raw_products),
        "product_identity": held_out_overlap(products, keys),
        "product_scaffold": held_out_overlap(scaffolds, keys),
        "sampled_product_similarity": held_out_similarity_sample(products, keys, sample_size, seed),
    }
