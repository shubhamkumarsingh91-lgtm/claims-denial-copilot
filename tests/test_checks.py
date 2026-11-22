"""Tests for the rule-based checks.

Each synthetic case's FULL output (every field: passed, every finding's check,
code, explanation and evidence, next action, notes) must equal the hand-written
expected answer. Run with:  python -m pytest tests/ -v
"""

import csv
import json
from pathlib import Path

import pytest

from copilot.checks import check_billed_payer, check_date_of_service, check_other_coverage, check_prior_auth
from copilot.checks.result import NEXT_ACTIONS

ROOT = Path(__file__).resolve().parents[1]
DOS = json.loads((ROOT / "data/synthetic/dos_cases.json").read_text())
PA = json.loads((ROOT / "data/synthetic/pa_cases.json").read_text())
TPL = json.loads((ROOT / "data/synthetic/tpl_cases.json").read_text())
PAY = json.loads((ROOT / "data/synthetic/payer_cases.json").read_text())

# Every denial code a check emits must exist in the reference mapping.
with open(ROOT / "data/reference/carc_mapping.csv", newline="") as f:
    KNOWN_CARCS = {row["carc"] for row in csv.DictReader(f) if row["status"] != "dropped"}


def run_dos(case):
    return check_date_of_service(
        case["claim"], case["eligibility_segments"],
        coverage_rules=DOS["coverage_rules"], denial_carc=case["denial_carc"],
    ).to_dict()


def run_pa(case):
    return check_prior_auth(case["claim"], PA["authorizations"], pa_required=case["pa_required"]).to_dict()


def run_tpl(case):
    return check_other_coverage(
        case["claim"], TPL["other_coverage"], case["billed_payer_type"],
        medicaid_allowed=case["medicaid_allowed"], denial_carc=case["denial_carc"],
    ).to_dict()


def run_pay(case):
    return check_billed_payer(case["claim"], case["eligibility_segments"], set(PAY["managed_care_plans"])).to_dict()


RUNNERS = {"DOS": run_dos, "PA-": run_pa, "TPL": run_tpl, "PAY": run_pay}
ALL_CASES = DOS["cases"] + PA["cases"] + TPL["cases"] + PAY["cases"]


def run(case):
    return RUNNERS[case["id"][:3]](case)


@pytest.mark.parametrize("case", ALL_CASES, ids=[c["id"] for c in ALL_CASES])
def test_case(case):
    assert run(case) == case["expected"]


@pytest.mark.parametrize("case", ALL_CASES, ids=[c["id"] for c in ALL_CASES])
def test_codes_and_actions_are_known(case):
    result = run(case)
    assert result["next_action"] in NEXT_ACTIONS
    for finding in result["findings"]:
        assert finding["carc"] in KNOWN_CARCS, f"invented code {finding['carc']}"
    assert result["passed"] == (not result["findings"])


def test_submission_before_service_is_rejected():
    claim = {"claim_id": "CLM-SYN-X", "date_of_service": "2026-03-10",
             "submission_date": "2026-03-01", "procedure_code": "99213"}
    with pytest.raises(ValueError):
        check_date_of_service(claim, [{"plan": "PLAN-A", "start_date": "2025-01-01", "end_date": None}])


def test_coverage_check_can_be_skipped():
    claim = {"claim_id": "CLM-SYN-Y", "date_of_service": "2026-03-10",
             "submission_date": "2026-03-11", "procedure_code": "00000"}
    result = check_date_of_service(claim, [{"plan": "PLAN-A", "start_date": "2025-01-01", "end_date": None}])
    assert result.passed is True


def test_timely_filing_limit_is_configurable_and_inclusive():
    claim = {"claim_id": "CLM-SYN-Z", "date_of_service": "2026-01-01",
             "submission_date": "2026-03-02", "procedure_code": "99213"}  # 60 days
    seg = [{"plan": "PLAN-A", "start_date": "2025-01-01", "end_date": None}]
    assert check_date_of_service(claim, seg, timely_filing_days=60).passed is True
    late = check_date_of_service(claim, seg, timely_filing_days=59)
    assert [f.check for f in late.findings] == ["timely_filing_exceeded"]
