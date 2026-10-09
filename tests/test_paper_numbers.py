import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEX = (ROOT / "paper" / "paper.tex").read_text(encoding="utf-8")
CONTROL = json.loads((ROOT / "reports" / "post-release-similarity-control.json").read_text())
FROZEN = json.loads((ROOT / "reports" / "v1-similarity-audit.json").read_text())
BASE = json.loads((ROOT / "reports" / "v0.2-baselines.json").read_text())["results"]


def pct(x: float, d: int = 2) -> str:
    return f"{100 * x:.{d}f}"


def test_frozen_audit_numbers_in_paper():
    assert pct(FROZEN["product_identity"]["overlapping_test_fraction"]) in TEX
    assert pct(FROZEN["product_scaffold"]["overlapping_test_fraction"]) in TEX
    frozen_sim = FROZEN["sampled_product_similarity"]["threshold_results"]
    assert pct(frozen_sim["0.7"]["proportion"], 1) in TEX


def test_control_numbers_in_paper():
    assert pct(CONTROL["product_identity"]["overlapping_fraction"]) in TEX
    assert pct(CONTROL["product_scaffold"]["overlapping_fraction"]) in TEX
    sim = CONTROL["sampled_product_similarity"]
    for key in ("0.7", "0.8", "0.9", "1.0"):
        assert pct(sim["threshold_results"][key]["proportion"], 1) in TEX
    assert f"{sim['median']:.3f}" in TEX and f"{sim['mean']:.3f}" in TEX


def test_baselines_in_paper():
    for cell in BASE.values():
        assert pct(cell["accuracy"]) in TEX
