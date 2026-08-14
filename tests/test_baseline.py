import pytest

from reaction_integrity_lab.baseline import canonical_combination, frequency_informed_baseline


def test_canonical_combination_matches_set_style_slot_scoring():
    row = {"a": "water", "b": None, "c": " ethanol "}
    assert canonical_combination(row, ("a", "b", "c")) == ("NULL", "ethanol", "water")


def test_frequency_baseline_scores_complete_top_n_combinations():
    train = [
        {"a": "S1", "b": "A1"},
        {"a": "A1", "b": "S1"},
        {"a": "S2", "b": "A2"},
        {"a": "S3", "b": "A3"},
    ]
    test = [
        {"a": "S1", "b": "A1"},
        {"a": "A2", "b": "S2"},
        {"a": "S4", "b": "A4"},
    ]
    result = frequency_informed_baseline(train, test, columns=("a", "b"), top_n=2)
    assert result.train_rows == 4
    assert result.correct_test_rows == 2
    assert result.accuracy == pytest.approx(2 / 3)
    assert result.to_dict()["most_common"][0]["train_count"] == 2


@pytest.mark.parametrize("top_n", [0, -1])
def test_frequency_baseline_rejects_non_positive_top_n(top_n):
    with pytest.raises(ValueError, match="positive"):
        frequency_informed_baseline([], [], columns=("a",), top_n=top_n)


def test_frequency_baseline_rejects_empty_columns():
    with pytest.raises(ValueError, match="non-empty"):
        frequency_informed_baseline([], [], columns=())
