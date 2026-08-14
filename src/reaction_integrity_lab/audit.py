"""Pure audit functions for reaction-condition benchmark records."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

Record = Mapping[str, Any]


@dataclass(frozen=True)
class SplitAudit:
    """Machine-readable audit results for a fixed train/test pair."""

    train_rows: int
    test_rows: int
    unique_train_inputs: int
    unique_test_inputs: int
    overlapping_test_inputs: int
    overlapping_test_input_fraction: float
    cross_split_duplicate_records: int
    missing_input_cells: int
    missing_output_cells: int
    unique_train_output_combinations: int
    most_common_train_output_count: int
    most_common_train_output_fraction: float

    def to_dict(self) -> dict[str, int | float]:
        """Return a JSON-ready representation."""

        return asdict(self)


def normalize_cell(value: Any) -> str:
    """Normalize nullable scalar cells without interpreting chemical identity."""

    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "<na>"} else text


def record_key(record: Record, columns: Sequence[str]) -> tuple[str, ...]:
    """Create an ordered, normalized key from declared columns."""

    return tuple(normalize_cell(record.get(column)) for column in columns)


def _missing_cells(records: Iterable[Record], columns: Sequence[str]) -> int:
    return sum(not normalize_cell(record.get(column)) for record in records for column in columns)


def audit_splits(
    train: Iterable[Record],
    test: Iterable[Record],
    *,
    input_columns: Sequence[str],
    output_columns: Sequence[str],
) -> SplitAudit:
    """Audit exact overlap, duplicate records, missingness, and output prevalence.

    Exact equality is deliberately narrow. It detects identity leakage but makes no claim about
    chemical similarity, scaffold overlap, or mechanistic equivalence.
    """

    if not input_columns or not output_columns:
        raise ValueError("input_columns and output_columns must both be non-empty")

    train_rows = list(train)
    test_rows = list(test)
    train_inputs = [record_key(row, input_columns) for row in train_rows]
    test_inputs = [record_key(row, input_columns) for row in test_rows]
    train_input_set = set(train_inputs)
    test_input_set = set(test_inputs)
    overlapping_test_inputs = sum(key in train_input_set for key in test_inputs)

    all_columns = tuple(input_columns) + tuple(output_columns)
    train_records = set(record_key(row, all_columns) for row in train_rows)
    cross_split_duplicates = sum(record_key(row, all_columns) in train_records for row in test_rows)

    output_counts = Counter(record_key(row, output_columns) for row in train_rows)
    most_common_count = output_counts.most_common(1)[0][1] if output_counts else 0

    return SplitAudit(
        train_rows=len(train_rows),
        test_rows=len(test_rows),
        unique_train_inputs=len(train_input_set),
        unique_test_inputs=len(test_input_set),
        overlapping_test_inputs=overlapping_test_inputs,
        overlapping_test_input_fraction=(
            overlapping_test_inputs / len(test_rows) if test_rows else 0.0
        ),
        cross_split_duplicate_records=cross_split_duplicates,
        missing_input_cells=_missing_cells(train_rows + test_rows, input_columns),
        missing_output_cells=_missing_cells(train_rows + test_rows, output_columns),
        unique_train_output_combinations=len(output_counts),
        most_common_train_output_count=most_common_count,
        most_common_train_output_fraction=(
            most_common_count / len(train_rows) if train_rows else 0.0
        ),
    )
