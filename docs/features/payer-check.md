# Feature: billed-payer check (managed care vs. fee-for-service)

> Independent personal project. Public reference information and synthetic data only. See the [README disclaimer](../../README.md#disclaimer).

**Code:** [`copilot/checks/payer_check.py`](../../copilot/checks/payer_check.py) · **Test cases:** [`data/synthetic/payer_cases.json`](../../data/synthetic/payer_cases.json) · **Tests:** [`tests/test_checks.py`](../../tests/test_checks.py)

## The problem

Many Medicaid members are enrolled in a managed care plan. When they are, the claim has to go to that plan, not to fee-for-service Medicaid. Members move between plans, so what counts is the plan **on the date of service**, not the plan they have today.

## How it works

| Situation | Result | Code | Next action |
|---|---|---|---|
| Billed the plan the member had on the date of service | Passes | — | `no_action` |
| Member in a managed care plan on the date of service, billed fee-for-service | Fails | 24 | `bill_correct_payer`, and check the provider is in that plan's network |
| Any other wrong plan (e.g. the wrong managed care plan, or a commercial plan) | Passes, with a note | none yet | `bill_correct_payer` |
| No coverage on the date of service | Skipped, left to the date-of-service check | — | `no_action` |

**A deliberate gap:** only the managed care case has a scenario in the mapping (RJ-056). Rather than invent a code for the other wrong-plan cases, the check tells the biller which plan to bill in a note. Adding a scenario for them is a small follow-up.

Which plans are managed care is passed in as a setting (in the generated data it comes from `plans.csv`), not hard-coded.

## Test cases (7, all synthetic)

PAY-01 right plan · PAY-02 managed care member billed fee-for-service · PAY-03 left managed care Jan 31, service Jan 20 → still the managed care plan · PAY-04 same member, service Feb 15 → fee-for-service is right · PAY-05 no coverage → skipped · PAY-06 billed a commercial plan instead of Medicaid → note · PAY-07 billed the wrong managed care plan → note
