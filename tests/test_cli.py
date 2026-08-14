import json

from reaction_integrity_lab import cli

ROWS = [
    {
        "reactant_000": "A",
        "reactant_001": "B",
        "product_000": "C",
        "solvent_000": "S",
        "solvent_001": None,
        "agent_000": "X",
        "agent_001": None,
        "agent_002": None,
    }
]


def test_cli_writes_json(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "parquet_records", lambda path, columns: iter(ROWS))
    output = tmp_path / "audit.json"
    assert (
        cli.main(["--train", "train.parquet", "--test", "test.parquet", "--output", str(output)])
        == 0
    )
    assert json.loads(output.read_text())["cross_split_duplicate_records"] == 1


def test_cli_prints_json(monkeypatch, capsys):
    monkeypatch.setattr(cli, "parquet_records", lambda path, columns: iter([]))
    assert cli.main(["--train", "train.parquet", "--test", "test.parquet"]) == 0
    assert json.loads(capsys.readouterr().out)["train_rows"] == 0
