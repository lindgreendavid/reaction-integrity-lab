from reaction_integrity_lab.audit import audit_splits, normalize_cell, record_key

INPUTS = ("reactant_000", "reactant_001", "product_000")
OUTPUTS = ("solvent_000", "agent_000")


def test_normalize_cell_handles_null_markers_and_scalars():
    assert normalize_cell(None) == ""
    assert normalize_cell("  <NA> ") == ""
    assert normalize_cell(" EtOH ") == "EtOH"
    assert normalize_cell(42) == "42"


def test_record_key_preserves_declared_column_order():
    row = {"a": "A", "b": " B "}
    assert record_key(row, ("b", "a", "missing")) == ("B", "A", "")


def test_audit_detects_exact_overlap_duplicates_missingness_and_prevalence():
    train = [
        {
            "reactant_000": "A",
            "reactant_001": "B",
            "product_000": "C",
            "solvent_000": "S",
            "agent_000": "X",
        },
        {
            "reactant_000": "D",
            "reactant_001": None,
            "product_000": "E",
            "solvent_000": "S",
            "agent_000": "X",
        },
        {
            "reactant_000": "F",
            "reactant_001": "G",
            "product_000": "H",
            "solvent_000": "T",
            "agent_000": None,
        },
    ]
    test = [
        {
            "reactant_000": "A",
            "reactant_001": "B",
            "product_000": "C",
            "solvent_000": "S",
            "agent_000": "X",
        },
        {
            "reactant_000": "A",
            "reactant_001": "B",
            "product_000": "C",
            "solvent_000": "Q",
            "agent_000": "Y",
        },
        {
            "reactant_000": "I",
            "reactant_001": "J",
            "product_000": "K",
            "solvent_000": "S",
            "agent_000": "X",
        },
    ]
    result = audit_splits(train, test, input_columns=INPUTS, output_columns=OUTPUTS)
    assert result.train_rows == 3
    assert result.test_rows == 3
    assert result.unique_train_inputs == 3
    assert result.unique_test_inputs == 2
    assert result.overlapping_test_inputs == 2
    assert result.overlapping_test_input_fraction == 2 / 3
    assert result.cross_split_duplicate_records == 1
    assert result.missing_input_cells == 1
    assert result.missing_output_cells == 1
    assert result.unique_train_output_combinations == 2
    assert result.most_common_train_output_count == 2
    assert result.most_common_train_output_fraction == 2 / 3
    assert result.to_dict()["test_rows"] == 3


def test_empty_splits_have_defined_zero_fractions():
    result = audit_splits([], [], input_columns=("input",), output_columns=("output",))
    assert result.overlapping_test_input_fraction == 0
    assert result.most_common_train_output_fraction == 0


def test_audit_rejects_empty_column_sets():
    try:
        audit_splits([], [], input_columns=(), output_columns=("output",))
    except ValueError as error:
        assert "non-empty" in str(error)
    else:
        raise AssertionError("expected ValueError")
