"""Consistency tests for the reference data.

The same facts live in three places: each kb/*.md scenario, the machine-readable
data/reference/carc_mapping.csv, and the human-readable kb/rejection_mapping.md
table. These tests check every scenario's code, remark code, scope and status
across all three, so they can't silently drift apart.
"""

import csv
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
KB_FILES = ["eligibility.md", "coding.md", "provider.md", "authorization.md", "medicaid.md"]

with open(ROOT / "data/reference/carc_mapping.csv", newline="") as f:
    CSV_ROWS = {row["scenario_id"]: row for row in csv.DictReader(f)}


def kb_scenarios():
    """Parse each '### RJ-xxx' block's CARC line (and optional RARC line)."""
    found = {}
    for name in KB_FILES:
        text = (ROOT / "kb" / name).read_text()
        for block in re.split(r"\n(?=### RJ-)", text):
            head = re.match(r"### (RJ-\d{3})", block)
            if not head:
                continue
            # e.g. "**CARC:** 197 (Confirmed; payer scope: all)"
            #   or "**CARC:** 16 + RARC M76 (Confirmed; payer scope: all)"
            carc = re.search(
                r"\*\*CARC:\*\* (\S+)(?: \+ RARC (\S+))? \((\w+); payer scope: (\w+)\)", block)
            found[head.group(1)] = {
                "file": name,
                "carc": carc.group(1) if carc else None,
                "rarc": (carc.group(2) or "") if carc else "",
                "status": carc.group(3).lower() if carc else None,
                "payer_scope": carc.group(4) if carc else None,
            }
    return found


KB = kb_scenarios()
TABLE = {
    m.group(1): [c.strip() for c in line.split("|")[1:-1]]
    for line in (ROOT / "kb/rejection_mapping.md").read_text().splitlines()
    if (m := re.match(r"\| (RJ-\d{3}) ", line))
}


def test_counts():
    assert len(CSV_ROWS) == 59
    assert set(CSV_ROWS) == set(TABLE)
    # RJ-010 was dropped and has no CARC line in the KB
    assert set(CSV_ROWS) - set(KB) <= {"RJ-010"}


def test_ids_are_sequential():
    assert sorted(CSV_ROWS) == [f"RJ-{n:03d}" for n in range(1, 60)]


@pytest.mark.parametrize("sid", sorted(KB))
def test_kb_matches_csv(sid):
    kb, row = KB[sid], CSV_ROWS[sid]
    if row["status"] == "dropped":
        return
    assert kb["carc"] == row["carc"], f"{sid} CARC differs between kb/{kb['file']} and CSV"
    assert kb["payer_scope"] == row["payer_scope"]
    assert kb["status"] == row["status"]
    assert kb["rarc"] == row["rarc"], f"{sid} remark code differs between kb/{kb['file']} and CSV"


@pytest.mark.parametrize("sid", sorted(CSV_ROWS))
def test_table_matches_csv(sid):
    row, cells = CSV_ROWS[sid], TABLE[sid]
    # columns: scenario | legacy | carc | rarc | meaning | scope | status | note | source
    assert cells[1] == row["legacy_code"]
    assert cells[2] == row["carc"]
    assert cells[3] == row["rarc"]
    assert cells[5] == row["payer_scope"]
    assert cells[6].lower().startswith(row["status"])
    if row["source"]:
        assert row["source"] in cells[8]
