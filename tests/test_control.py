import pytest

from reaction_integrity_lab.control import (
    build_control,
    held_out_overlap,
    held_out_similarity_sample,
)


def test_overlap_requires_a_different_input_key():
    values = ["A", "A", "B"]
    different = [("r1", "", "A"), ("r2", "", "A"), ("r3", "", "B")]
    out = held_out_overlap(values, different)
    assert out["overlapping_rows"] == 2
    assert out["overlapping_fraction"] == pytest.approx(2 / 3)
    same_key = [("r1", "", "A"), ("r1", "", "A"), ("r3", "", "B")]
    assert held_out_overlap(values, same_key)["overlapping_rows"] == 0


def test_overlap_ignores_invalid_values():
    out = held_out_overlap(["A", None], [("a", "", "A"), ("b", "", "")])
    assert out["valid_rows"] == 1 and out["overlapping_fraction"] == 0.0


def test_similarity_sample_masks_a_rows_own_unique_molecule():
    products = ["CCO", "CCO", "CCCO", "c1ccccc1"]
    keys = [("a", "", "CCO"), ("b", "", "CCO"), ("c", "", "CCCO"), ("d", "", "c1ccccc1")]
    out = held_out_similarity_sample(products, keys, sample_size=4, seed=1)
    assert out["valid_sample_rows"] == 4
    thresholds = out["threshold_results"]
    # the two CCO rows find each other at similarity 1.0; the unique ones cannot match themselves
    assert thresholds["1.0"]["successes"] == 2


def test_similarity_sample_skips_unparseable_products():
    out = held_out_similarity_sample(
        ["CCO", "not a molecule", "CCCO"],
        [("a", "", "x"), ("b", "", "y"), ("c", "", "z")],
        sample_size=3,
        seed=2,
    )
    assert out["valid_sample_rows"] == 2


def test_build_control_end_to_end():
    reactants0 = ["CCO", "CCO", "CCC", "CCCC"]
    reactants1 = ["", "O", "", ""]
    products = ["CC(=O)O", "OC(C)=O", "c1ccccc1", "Cc1ccccc1"]
    out = build_control(reactants0, reactants1, products, sample_size=4, seed=3)
    assert out["label"].startswith("POST-HOC")
    assert out["rows"] == 4
    # CC(=O)O and OC(C)=O are the same molecule under different strings and different input keys
    assert out["product_identity"]["overlapping_rows"] == 2
    assert out["product_scaffold"]["valid_rows"] >= 0
