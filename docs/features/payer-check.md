# Feature: billed-payer check (managed care vs. fee-for-service)

> Independent personal project. Public reference information and synthetic data only. See the [README disclaimer](../../README.md#disclaimer).

**Code:** [`copilot/checks/payer_check.py`](../../copilot/checks/payer_check.py) · **Test cases:** [`data/synthetic/payer_cases.json`](../../data/synthetic/payer_cases.json) · **Tests:** [`tests/test_checks.py`](../../tests/test_checks.py)

## The problem

A claim sent to a plan that didn't cover the patient on the date of service will never be paid there. Every day it sits at the wrong payer is wasted, and the filing deadline at the right payer usually keeps running. Members move between plans, so what counts is the plan **on the date of service**, not the plan they have today, or the old card the clinic still has on file.

## How it works

| Situation | Result | Code | Next action |
|---|---|---|---|
| Billed the plan the member had on the date of service | Passes | — | `no_action` |
| Member in a Medicaid managed care plan on the date of service, billed to **fee-for-service** Medicaid | Fails | 24 (RJ-056) | `bill_correct_payer`, and check the provider is in that plan's network |
| Any other wrong plan: an old card on file, the wrong managed care plan, a commercial plan instead of Medicaid, or the reverse | Fails | 109 (RJ-059) | `bill_correct_payer`, and update the insurance on file |
| No coverage on the date of service | Skipped, left to the date-of-service check | — | `no_action` |

**Why two codes:** code 24 ("this belongs to a managed care plan") is what **fee-for-service Medicaid** sends back. Any other payer that gets a claim for someone it doesn't cover answers with code 109 ("send it to the correct payer"). So a managed care member billed to a *commercial* plan is a 109, not a 24 (case PAY-08).

Which plans are managed care and which are fee-for-service are passed in as settings (in the generated data they come from `plans.csv`), not hard-coded.

## Test cases (9, all synthetic)

PAY-01 right plan · PAY-02 managed care member billed fee-for-service → 24 · PAY-03 left managed care Jan 31, service Jan 20 → still the managed care plan → 24 · PAY-04 same member, service Feb 15 → fee-for-service is right · PAY-05 no coverage → skipped · PAY-06 billed a commercial plan instead of Medicaid → 109 · PAY-07 billed the wrong managed care plan → 109 · PAY-08 managed care member billed to a commercial plan → 109, not 24 · PAY-09 old employer card on file after switching to Medicaid → 109
