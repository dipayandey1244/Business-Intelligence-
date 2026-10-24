"""Lightweight static checks for repository structure."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_main_app_and_requirements_exist():
    assert (ROOT / "app.py").exists()
    assert (ROOT / "requirements.txt").exists()

def test_secrets_are_not_committed():
    assert not (ROOT / ".streamlit" / "secrets.toml").exists()
    assert (ROOT / ".streamlit" / "secrets.toml.example").exists()

def test_synthetic_and_governance_disclosures_exist():
    assert "synthetic" in (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert (ROOT / "docs" / "GOVERNANCE.md").exists()
