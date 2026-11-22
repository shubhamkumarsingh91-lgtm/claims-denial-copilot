"""Generate a reproducible set of SYNTHETIC denied claims (step 1.6).

Independent personal project. Every member, provider, plan, date and claim
produced here is invented. No PHI, PII, Medicaid data, or internal data.

What makes this more than random rows: each denial is built from one of the
57 active scenarios in data/reference/carc_mapping.csv, and the supporting
tables are written so that the facts actually CAUSE that denial. Example: a
"coverage gap" denial (RJ-001) gets a member whose two eligibility periods
leave a gap exactly where the date of service falls.

For the 15 scenarios the rule-based checks can already diagnose, each denial
also records the check that should catch it and the expected next action, and
tests/test_generator.py runs the real checks to prove the facts line up.

Usage:
    python scripts/generate_denials.py                 # writes data/synthetic/generated/
    python scripts/generate_denials.py --out some/dir  # writes somewhere else
Same seed in, same files out.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "synthetic" / "generated"
SEED = 20261121
TOTAL_DENIALS = 200

PLANS = {  # synthetic plan names -> payer type
    "MEDICAID-FFS": "medicaid",
    "MEDICAID-MCO-A": "medicaid",
    "COMMERCIAL-X": "commercial",
}
PLAN_TYPES = {"MEDICAID-FFS": "fee_for_service", "MEDICAID-MCO-A": "managed_care", "COMMERCIAL-X": "commercial"}
COVERED_CODES = ["99213", "99214", "90834", "70551", "27447", "97110"]
PA_CODES = {"70551", "27447", "97110"}   # need prior authorization (synthetic rule)
NON_PA_CODES = ["99213", "99214", "90834"]
UNCOVERED_CODE = "99499"                  # deliberately not a covered benefit on any plan
LAPSED_PROVIDER = "SYN-NPI-020"           # enrollment ended 2025-12-31
LAPSED_PROVIDER_CARC = "B7"

# Scenarios the checks can diagnose today: scenario -> (check, finding, next action)
CHECKABLE = {
    "RJ-001": ("dos_check", "dos_in_coverage_gap", "bill_other_coverage"),
    "RJ-002": ("dos_check", "dos_before_coverage", "bill_other_coverage"),
    "RJ-003": ("dos_check", "member_not_found", "bill_other_coverage"),
    "RJ-007": ("dos_check", "not_covered_on_dos", "write_off"),
    "RJ-008": ("dos_check", "dos_after_coverage_ended", "bill_other_coverage"),
    "RJ-012": ("dos_check", "not_covered_on_dos", "write_off"),
    "RJ-013": ("dos_check", "dos_after_coverage_ended", "bill_other_coverage"),
    "RJ-053": ("dos_check", "timely_filing_exceeded", "write_off"),
    "RJ-054": ("dos_check", "denial_contradicted", "resubmit_as_is"),
    "RJ-039": ("pa_matcher", "no_auth_on_file", "request_retro_auth"),
    "RJ-040": ("pa_matcher", "dos_after_auth_expired", "request_auth_update"),
    "RJ-041": ("pa_matcher", "procedure_code_mismatch", "correct_and_resubmit"),
    "RJ-042": ("pa_matcher", "units_exceeded", "request_auth_update"),
    "RJ-043": ("pa_matcher", "provider_mismatch", "request_auth_update"),
    "RJ-009": ("tpl_check", "other_coverage_primary", "bill_other_coverage"),
    "RJ-055": ("tpl_check", "other_coverage_primary", "bill_other_coverage"),
    "RJ-056": ("payer_check", "billed_ffs_member_in_managed_care", "bill_correct_payer"),
    "RJ-059": ("payer_check", "wrong_payer", "bill_correct_payer"),
}


def load_scenarios() -> list[dict]:
    with open(ROOT / "data/reference/carc_mapping.csv", newline="") as f:
        return [r for r in csv.DictReader(f) if r["status"] != "dropped"]


def allocate(scenarios: list[dict]) -> list[str]:
    """3 denials per scenario, then the rest go round-robin to checkable scenarios until 200."""
    ids = [s["scenario_id"] for s in scenarios for _ in range(3)]
    if len(ids) > TOTAL_DENIALS:
        raise ValueError(f"3 per scenario already gives {len(ids)} denials, more than {TOTAL_DENIALS}")
    extra = sorted(CHECKABLE)
    i = 0
    while len(ids) < TOTAL_DENIALS:
        ids.append(extra[i % len(extra)])
        i += 1
    return ids


def generate(out_dir: Path, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    scenarios = {s["scenario_id"]: s for s in load_scenarios()}
    plan_ids = sorted(PLANS)

    def rand_date(start: date, end: date) -> date:
        return start + timedelta(days=rng.randint(0, (end - start).days))

    def plan_for(scope: str) -> str:
        if scope == "medicaid":
            return "MEDICAID-FFS"
        if scope == "commercial":
            return "COMMERCIAL-X"
        return rng.choice(plan_ids)

    providers = [
        {"npi": f"SYN-NPI-{n:03d}", "name": f"Synthetic Clinic {n:02d}",
         "enrolled_from": "2020-01-01", "enrolled_to": ""}
        for n in range(1, 20)
    ] + [{"npi": LAPSED_PROVIDER, "name": "Synthetic Clinic 20 (enrollment lapsed)",
          "enrolled_from": "2019-01-01", "enrolled_to": "2025-12-31"}]
    active_npis = [p["npi"] for p in providers if not p["enrolled_to"]]

    coverage_rules = [
        {"plan": p, "procedure_code": c, "effective_start": "2024-01-01", "effective_end": "",
         "pa_required": "yes" if c in PA_CODES else "no"}
        for p in plan_ids for c in COVERED_CODES
    ]

    members, segments, other_coverage, auths, denials = [], [], [], [], []

    for n, sid in enumerate(allocate(list(scenarios.values())), start=1):
        sc = scenarios[sid]
        member_id, claim_id = f"M-SYN-{n:04d}", f"CLM-SYN-{n:04d}"
        plan = plan_for(sc["payer_scope"])
        dos = rand_date(date(2026, 1, 5), date(2026, 9, 30))
        submitted = dos + timedelta(days=rng.randint(3, 60))
        code = rng.choice(NON_PA_CODES)
        units = 1
        npi = rng.choice(active_npis)
        billed_plan = plan
        seg_list: list[tuple[str, date, date | None]] = [(plan, date(2025, 1, 1), None)]

        # --- plant the facts that cause each scenario -------------------------
        if sid == "RJ-001":    # gap between two coverage periods
            end1 = dos - timedelta(days=rng.randint(5, 40))
            seg_list = [(plan, date(2025, 1, 1), end1), (plan, dos + timedelta(days=rng.randint(5, 40)), None)]
        elif sid == "RJ-002":  # coverage starts after the service
            seg_list = [(plan, dos + timedelta(days=rng.randint(3, 45)), None)]
        elif sid == "RJ-003":  # no eligibility record at all
            seg_list = []
        elif sid in ("RJ-008", "RJ-013"):  # coverage ended before the service
            seg_list = [(plan, date(2025, 1, 1), dos - timedelta(days=rng.randint(1, 60)))]
        elif sid in ("RJ-007", "RJ-012"):  # service not a covered benefit
            code = UNCOVERED_CODE
        elif sid == "RJ-053":  # filed more than 365 days after the service
            dos = rand_date(date(2025, 1, 5), date(2025, 6, 30))
            submitted = dos + timedelta(days=rng.randint(366, 480))
            seg_list = [(plan, date(2024, 1, 1), None)]
        elif sid == "RJ-054":  # denied as 'before coverage', retro eligibility posted later
            seg_list = [(plan, dos.replace(day=1), None)]
        elif sid == "RJ-051":  # spend-down met a few days after the service
            seg_list = [(plan, dos + timedelta(days=rng.randint(2, 15)), None)]
        elif sid in ("RJ-009", "RJ-055"):  # other insurance should pay first
            other_coverage.append({"member_id": member_id, "carrier": "OTHER-CARRIER-1",
                                   "coverage_order": "primary", "start_date": "2025-01-01", "end_date": ""})
        elif sid == "RJ-056":  # in managed care on the DOS, billed fee-for-service
            seg_list = [("MEDICAID-MCO-A", date(2025, 1, 1), None)]
            billed_plan = "MEDICAID-FFS"
        elif sid == "RJ-059":  # old card on file: left the employer plan, now on Medicaid, employer plan billed
            switch = dos - timedelta(days=rng.randint(10, 90))
            seg_list = [("COMMERCIAL-X", date(2024, 1, 1), switch - timedelta(days=1)), ("MEDICAID-FFS", switch, None)]
            billed_plan = "COMMERCIAL-X"
        elif sc["carc"] == LAPSED_PROVIDER_CARC:  # RJ-028/030/033/035/057: provider not eligible on DOS
            npi = LAPSED_PROVIDER

        if sid in ("RJ-039", "RJ-040", "RJ-041", "RJ-042", "RJ-043"):
            code = rng.choice(sorted(PA_CODES))
            auth = {"auth_id": f"AUTH-SYN-{n:04d}", "member_id": member_id, "procedure_code": code,
                    "start_date": (dos - timedelta(days=30)).isoformat(),
                    "end_date": (dos + timedelta(days=60)).isoformat(),
                    "approved_units": 1, "units_used": 0, "npi": npi}
            if sid == "RJ-040":
                end = dos - timedelta(days=rng.randint(1, 30))
                auth["end_date"], auth["start_date"] = end.isoformat(), (end - timedelta(days=90)).isoformat()
            elif sid == "RJ-041":
                auth["procedure_code"] = rng.choice(sorted(PA_CODES - {code}))
            elif sid == "RJ-042":
                approved = rng.choice([1, 6, 12])
                auth["approved_units"], auth["units_used"] = approved, approved - rng.randint(0, min(2, approved - 1))
                units = (approved - auth["units_used"]) + rng.randint(1, 3)
            elif sid == "RJ-043":
                auth["npi"] = rng.choice([x for x in active_npis if x != npi])
            if sid != "RJ-039":
                auths.append(auth)

        members.append({"member_id": member_id, "home_plan": plan})
        for p, start, end in seg_list:
            segments.append({"member_id": member_id, "plan": p, "payer_type": PLANS[p],
                             "start_date": start.isoformat(), "end_date": end.isoformat() if end else ""})

        check, finding, action = CHECKABLE.get(sid, ("", "", ""))
        denials.append({
            "denial_id": f"DEN-SYN-{n:04d}", "claim_id": claim_id, "member_id": member_id,
            "billed_plan": billed_plan, "rendering_npi": npi, "procedure_code": code, "units": units,
            "date_of_service": dos.isoformat(), "submission_date": submitted.isoformat(),
            "carc": sc["carc"], "rarc": sc["rarc"],
            "scenario_id": sid, "category": sc["category"], "payer_scope": sc["payer_scope"],
            "checkable_by": check, "expected_finding": finding, "expected_next_action": action,
        })

    plans = [{"plan": p, "payer_type": PLANS[p], "plan_type": PLAN_TYPES[p]} for p in plan_ids]
    tables = {
        "plans.csv": plans,
        "members.csv": members, "eligibility_segments.csv": segments, "other_coverage.csv": other_coverage,
        "providers.csv": providers, "coverage_rules.csv": coverage_rules,
        "authorizations.csv": auths, "denials.csv": denials,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    headers = {"other_coverage.csv": ["member_id", "carrier", "coverage_order", "start_date", "end_date"]}
    for name, rows in tables.items():
        with open(out_dir / name, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers.get(name) or list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    counts = {name: len(rows) for name, rows in tables.items()}
    manifest = {"seed": seed, "row_counts": counts,
                "checkable_denials": sum(1 for d in denials if d["checkable_by"]),
                "scenarios_covered": len({d["scenario_id"] for d in denials})}
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(json.dumps(generate(args.out, args.seed), indent=2))


if __name__ == "__main__":
    main()
