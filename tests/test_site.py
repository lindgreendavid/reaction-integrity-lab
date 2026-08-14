from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_site_exposes_interaction_evidence_status_and_boundaries():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
    styles = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")

    assert "The accuracy inflation microscope" in html
    assert "The released split passes its exact-identity audit" in html
    assert "independent model training remains pending" in html
    assert "zero exact train/test input collisions" in html
    assert "What this study can—and cannot—say" in html
    assert 'aria-live="polite"' in html
    assert 'aria-pressed="true"' in html
    assert "44%" in html and "47%" in html and "21%" in html and "24%" in html
    assert "independently reproduced" not in html.lower()
    assert "renderCell" in script
    assert "renderStage" in script
    assert "prefers-reduced-motion" in styles
    assert "forced-colors: active" in styles
    assert "min-height: 44px" in styles


def test_no_unreviewed_remote_scripts_or_insecure_links():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    assert "http://" not in html
    assert '<script src="http' not in html
    assert 'target="_blank"' not in html
