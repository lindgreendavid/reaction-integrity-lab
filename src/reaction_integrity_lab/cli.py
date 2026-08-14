"""Command-line interface for local audit reproduction."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from .audit import audit_splits
from .io import parquet_records

INPUT_COLUMNS = ("reactant_000", "reactant_001", "product_000")
OUTPUT_COLUMNS = ("solvent_000", "solvent_001", "agent_000", "agent_001", "agent_002")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Audit an ORDerly condition benchmark split")
    command.add_argument("--train", type=Path, required=True)
    command.add_argument("--test", type=Path, required=True)
    command.add_argument("--output", type=Path)
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    columns = list(INPUT_COLUMNS + OUTPUT_COLUMNS)
    audit = audit_splits(
        parquet_records(args.train, columns),
        parquet_records(args.test, columns),
        input_columns=INPUT_COLUMNS,
        output_columns=OUTPUT_COLUMNS,
    ).to_dict()
    rendered = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
