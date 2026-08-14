"""Input helpers kept separate from the pure scientific audit."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any


def parquet_records(path: Path, columns: list[str]) -> Iterator[dict[str, Any]]:
    """Yield selected Parquet columns in bounded batches.

    PyArrow is optional so the core audit and CI fixtures remain lightweight.
    """

    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment-specific branch
        raise RuntimeError("Install the data extra: pip install -e '.[data]'") from exc

    parquet = pq.ParquetFile(path)
    for batch in parquet.iter_batches(columns=columns, batch_size=65_536):
        yield from batch.to_pylist()
