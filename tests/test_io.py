import sys
from types import SimpleNamespace

from reaction_integrity_lab.io import parquet_records


def test_parquet_records_yields_batched_rows(monkeypatch, tmp_path):
    batches = [
        SimpleNamespace(to_pylist=lambda: [{"x": 1}]),
        SimpleNamespace(to_pylist=lambda: [{"x": 2}]),
    ]
    fake_file = SimpleNamespace(iter_batches=lambda **kwargs: iter(batches))
    fake_parquet = SimpleNamespace(ParquetFile=lambda path: fake_file)
    monkeypatch.setitem(sys.modules, "pyarrow", SimpleNamespace(parquet=fake_parquet))
    monkeypatch.setitem(sys.modules, "pyarrow.parquet", fake_parquet)
    assert list(parquet_records(tmp_path / "x.parquet", ["x"])) == [{"x": 1}, {"x": 2}]
