import pytest

from reaction_integrity_lab.similarity import (
    canonical_smiles,
    maximum_tanimoto,
    morgan_fingerprint,
    murcko_scaffold,
    wilson_interval,
)


def test_canonical_identity_normalizes_equivalent_smiles():
    assert canonical_smiles("C(C)O") == canonical_smiles("CCO")
    assert canonical_smiles(None) is None
    assert canonical_smiles("not smiles") is None


def test_murcko_scaffold_excludes_scaffoldless_molecules():
    assert murcko_scaffold("CCO") is None
    assert murcko_scaffold("Cc1ccccc1") == "c1ccccc1"


def test_fingerprint_similarity_is_bounded_and_exact_for_identity():
    ethanol = morgan_fingerprint("CCO")
    propanol = morgan_fingerprint("CCCO")
    assert ethanol is not None and propanol is not None
    assert maximum_tanimoto(ethanol, [propanol, ethanol]) == 1.0
    assert 0 < maximum_tanimoto(ethanol, [propanol]) < 1


def test_maximum_tanimoto_requires_references():
    fingerprint = morgan_fingerprint("CCO")
    assert fingerprint is not None
    with pytest.raises(ValueError, match="references"):
        maximum_tanimoto(fingerprint, [])


def test_wilson_interval_and_validation():
    interval = wilson_interval(50, 100)
    assert interval.proportion == 0.5
    assert interval.lower == pytest.approx(0.4038, abs=0.0001)
    assert interval.upper == pytest.approx(0.5962, abs=0.0001)
    assert interval.to_dict()["total"] == 100
    with pytest.raises(ValueError, match="positive"):
        wilson_interval(0, 0)
    with pytest.raises(ValueError, match="between"):
        wilson_interval(2, 1)
