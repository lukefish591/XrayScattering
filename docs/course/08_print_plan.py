#!/usr/bin/env python3
"""Module 8 — print where to fill the experiment questionnaire. No fake data."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
qpath = ROOT / "docs" / "context" / "experiment-questionnaire.md"
print("Fill this file with YOUR experiment (leave blanks if unknown):")
print(" ", qpath)
print()
print("Do not copy Pyrex / PS-PMMA / Cu-pit numbers from the papers unless that is actually your sample.")
print("Course toys live in course/plots/ and are labelled toys.")
if not qpath.is_file():
    raise SystemExit("questionnaire missing")
print("questionnaire bytes:", qpath.stat().st_size)
