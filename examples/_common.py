"""Shared paths for the examples."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DATA = ROOT / "data"
RESULTS = Path(__file__).resolve().parent / "case_study_results"
RESULTS.mkdir(exist_ok=True)
