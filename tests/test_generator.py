"""Tests for scripts/generate_denials.py and its committed output.

1. Reproducible: regenerating gives byte-identical files to the committed ones.
2. Complete: 200 denials, every active scenario present, codes match the mapping.
3. Consistent: every ID a denial points to exists in its table.
4. Synthetic: every identifier carries the SYN marker.
5. Causal: for every checkable denial, the real check run on the generated facts
   finds exactly the planted cause, with the expected denial code and next action.
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "data/synthetic/generated"
sys.path.insert(0, str(ROOT / "scripts"))

import generate_denials  # noqa: E402
from copilot.checks import check_date_of_service, check_prior_auth  # noqa: E402


def read(name):
    with open(GEN / name, newline="") as f:
        return list(csv.DictReader(f))


DENIALS = read("denials.csv")
SEGMENTS = read("eligibility_segments.csv")
AUTHS = read("authorizations.csv")
RULES = read("coverage_rules.csv")
PROVIDERS = read("providers.csv")
MEMBERS = read("members.csv")
OTHER = read("other_coverage.csv")
with open(ROOT / "data/reference/carc_mapping.csv", newline="") as f:
    MAPPING = {r["scenario_id"]: r for r in csv.DictReader(f)}


def test_reproducible(tmp_path):
    generate_denials.generate(tmp_path)
    written = sorted(p.name for p in tmp_path.iterdir())
    committed = sorted(p.name for p in GEN.iterdir() if p.suffix in (".csv", ".json"))
    assert written == committed
    for name in written:
        assert (tmp_path / name).read_bytes() == (GEN / name).read_bytes(), f"{name} differs from a fresh run"


def test_counts_and_manifest():
    manifest = json.loads((GEN / "manifest.json").read_text())
    assert len(DENIALS) == 200 == manifest["row_counts"]["denials.csv"]
    for name, n in manifest["row_counts"].items():
        assert len(read(name)) == n, name
    active = {s for s, r in MAPPING.items() if r["status"] != "dropped"}
    per = Counter(d["scenario_id"] for d in DENIALS)
    assert set(per) == active and manifest["scenarios_covered"] == 57
    assert min(per.values()) >= 3
    checkable = [d for d in DENIALS if d["checkable_by"]]
    assert len(checkable) == manifest["checkable_denials"] == 71


def test_codes_match_mapping():
    for d in DENIALS:
        row = MAPPING[d["scenario_id"]]
        assert (d["carc"], d["rarc"], d["category"], d["payer_scope"]) == \
               (row["carc"], row["rarc"], row["category"], row["payer_scope"]), d["denial_id"]


def test_ids_unique_and_linked():
    for key in ("denial_id", "claim_id", "member_id"):
        assert len({d[key] for d in DENIALS}) == 200, key
    members = {m["member_id"] for m in MEMBERS}
    npis = {p["npi"] for p in PROVIDERS}
    plans = {r["plan"] for r in RULES}
    for d in DENIALS:
        assert d["member_id"] in members and d["rendering_npi"] in npis and d["billed_plan"] in plans
    for row in SEGMENTS + AUTHS + OTHER:
        assert row["member_id"] in members
    for a in AUTHS:
        assert a["npi"] in npis


def test_everything_is_marked_synthetic():
    for d in DENIALS:
        assert "SYN" in d["denial_id"] and "SYN" in d["claim_id"] and "SYN" in d["member_id"]
        assert d["rendering_npi"].startswith("SYN-NPI-")
    assert all(a["auth_id"].startswith("AUTH-SYN-") for a in AUTHS)


def test_dates_are_sane():
    for d in DENIALS:
        assert d["submission_date"] > d["date_of_service"], d["denial_id"]
    for s in SEGMENTS:
        assert not s["end_date"] or s["end_date"] >= s["start_date"]
    for a in AUTHS:
        assert a["end_date"] >= a["start_date"]


def _segments(member_id):
    return [{"plan": s["plan"], "start_date": s["start_date"], "end_date": s["end_date"] or None}
            for s in SEGMENTS if s["member_id"] == member_id]


def _rules():
    return [{"procedure_code": r["procedure_code"], "plan": r["plan"],
             "effective_start": r["effective_start"], "effective_end": r["effective_end"] or None}
            for r in RULES]


def _auths():
    return [{**a, "approved_units": int(a["approved_units"]), "units_used": int(a["units_used"])} for a in AUTHS]


PA_REQUIRED = {r["procedure_code"] for r in RULES if r["pa_required"] == "yes"}


@pytest.mark.parametrize("d", [d for d in DENIALS if d["checkable_by"]], ids=lambda d: f"{d['denial_id']}-{d['scenario_id']}")
def test_check_finds_planted_cause(d):
    if d["checkable_by"] == "dos_check":
        result = check_date_of_service(
            {"claim_id": d["claim_id"], "date_of_service": d["date_of_service"],
             "submission_date": d["submission_date"], "procedure_code": d["procedure_code"]},
            _segments(d["member_id"]), coverage_rules=_rules(), denial_carc=d["carc"],
        )
    else:
        result = check_prior_auth(
            {"claim_id": d["claim_id"], "member_id": d["member_id"], "procedure_code": d["procedure_code"],
             "date_of_service": d["date_of_service"], "units": int(d["units"]), "rendering_npi": d["rendering_npi"]},
            _auths(), pa_required=d["procedure_code"] in PA_REQUIRED,
        )

    assert result.next_action == d["expected_next_action"]
    if d["expected_finding"] == "denial_contradicted":
        # Retro eligibility: no failure now, and the check says the denial no longer holds.
        assert result.passed and result.findings == []
        assert any("possible retro eligibility" in n for n in result.notes)
    else:
        # Exactly one problem was planted, so exactly one is found, with the denial's own code.
        assert [(f.check, f.carc) for f in result.findings] == [(d["expected_finding"], d["carc"])]
