"""Exact frequency-informed baselines for condition combinations."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from reaction_integrity_lab.audit import normalize_cell

Record = Mapping[str, Any]


def canonical_combination(record: Record, columns: Sequence[str]) -> tuple[str, ...]:
    """Return the order-insensitive component combination used by ORDerly."""

    return tuple(sorted(normalize_cell(record.get(column)) or "NULL" for column in columns))


@dataclass(frozen=True)
class FrequencyBaseline:
    """Result of predicting the most frequent training combinations."""

    train_rows: int
    test_rows: int
    top_n: int
    correct_test_rows: int
    accuracy: float
    most_common: tuple[tuple[tuple[str, ...], int], ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready representation."""

        result = asdict(self)
        result["most_common"] = [
            {"combination": list(combination), "train_count": count}
            for combination, count in self.most_common
        ]
        return result


def frequency_informed_baseline(
    train: Iterable[Record],
    test: Iterable[Record],
    *,
    columns: Sequence[str],
    top_n: int = 3,
) -> FrequencyBaseline:
    """Predict the ``top_n`` most common training combinations for every test row.

    This deliberately matches the reference implementation's set-style scoring: component slots
    are normalized, sorted within each row, and compared as complete combinations.
    """

    if not columns:
        raise ValueError("columns must be non-empty")
    if top_n < 1:
        raise ValueError("top_n must be positive")

    train_counts: Counter[tuple[str, ...]] = Counter()
    train_rows = 0
    for record in train:
        train_counts[canonical_combination(record, columns)] += 1
        train_rows += 1

    most_common = tuple(train_counts.most_common(top_n))
    predicted = {combination for combination, _ in most_common}
    test_rows = 0
    correct = 0
    for record in test:
        correct += canonical_combination(record, columns) in predicted
        test_rows += 1

    return FrequencyBaseline(
        train_rows=train_rows,
        test_rows=test_rows,
        top_n=top_n,
        correct_test_rows=correct,
        accuracy=correct / test_rows if test_rows else 0.0,
        most_common=most_common,
    )
