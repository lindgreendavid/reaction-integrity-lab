"""Prespecified chemical identity, scaffold, and fingerprint utilities."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.DataStructs.cDataStructs import ExplicitBitVect

MORGAN_GENERATOR = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)


@dataclass(frozen=True)
class WilsonInterval:
    """Binomial proportion and two-sided Wilson 95% interval."""

    successes: int
    total: int
    proportion: float
    lower: float
    upper: float

    def to_dict(self) -> dict[str, int | float]:
        """Return a JSON-ready representation."""

        return asdict(self)


def molecule(smiles: str | None) -> Chem.Mol | None:
    """Parse a non-empty SMILES string without changing its chemistry."""

    if not smiles or not smiles.strip():
        return None
    return Chem.MolFromSmiles(smiles)


def canonical_smiles(smiles: str | None) -> str | None:
    """Return canonical isomeric SMILES, or ``None`` for missing/invalid input."""

    mol = molecule(smiles)
    return Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True) if mol else None


def murcko_scaffold(smiles: str | None) -> str | None:
    """Return a canonical non-empty Bemis-Murcko scaffold."""

    mol = molecule(smiles)
    if mol is None:
        return None
    scaffold = MurckoScaffold.GetScaffoldForMol(mol)  # type: ignore[no-untyped-call]
    if scaffold.GetNumAtoms() == 0:
        return None
    return Chem.MolToSmiles(scaffold, canonical=True, isomericSmiles=True)


def morgan_fingerprint(smiles: str | None) -> ExplicitBitVect | None:
    """Return the frozen radius-2, 2,048-bit Morgan fingerprint."""

    mol = molecule(smiles)
    return MORGAN_GENERATOR.GetFingerprint(mol) if mol else None


def maximum_tanimoto(query: ExplicitBitVect, references: list[ExplicitBitVect]) -> float:
    """Return the exact maximum Tanimoto similarity against all references."""

    if not references:
        raise ValueError("references must be non-empty")
    return float(max(DataStructs.BulkTanimotoSimilarity(query, references)))


def wilson_interval(successes: int, total: int, *, z: float = 1.959963984540054) -> WilsonInterval:
    """Calculate the two-sided Wilson score interval for a binomial proportion."""

    if total <= 0:
        raise ValueError("total must be positive")
    if successes < 0 or successes > total:
        raise ValueError("successes must lie between zero and total")
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total))
        / denominator
    )
    return WilsonInterval(successes, total, proportion, center - margin, center + margin)
