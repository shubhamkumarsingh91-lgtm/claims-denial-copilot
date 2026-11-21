# Feature: date-of-service check

> Independent personal project. Public reference information and synthetic data only. See the [README disclaimer](../../README.md#disclaimer).

**Code:** [`copilot/checks/dos_check.py`](../../copilot/checks/dos_check.py) · **Test cases:** [`data/synthetic/dos_cases.json`](../../data/synthetic/dos_cases.json) · **Tests:** [`tests/test_checks.py`](../../tests/test_checks.py)

## The problem

Billers often check a claim against the patient's plan as it is **today**. Payers judge it by the eligibility and coverage in effect **on the date of service (DOS)**. Timely filing is a separate check, counted from the DOS to the day the claim was submitted.

## What it checks, in order

| # | Check | Fails when | Code |
|---|---|---|---|
| 1 | Eligibility on DOS | No eligibility record at all | 31 |
| | | DOS is before coverage started | 26 |
| | | DOS is after coverage ended | 27 |
| | | DOS falls in a gap between two coverage periods | 200 |
| 2 | Coverage on DOS | The DOS plan didn't cover the procedure on that date | 204 |
| 3 | Timely filing | Days from DOS to submission are over the limit (default 365, configurable) | 29 |
| 4 | Plan change (note only) | The plan at submission differs from the plan on the DOS | — |
| 5 | Denial contradicted (note only) | Denied with an eligibility code, but coverage now shows on the DOS (e.g. retro eligibility) | — |

All problems are reported, not just the first. The 365-day default follows the federal Medicaid rule of 12 months from the date of service ([42 CFR 447.45(d)](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-447/subpart-A/section-447.45)); payers can set their own.

## Next action

| Situation | Next action |
|---|---|
| Any eligibility failure | `bill_other_coverage`: check other coverage or pending retro eligibility before billing the patient |
| Not covered on DOS | `write_off`, unless the procedure code was wrong (then correct and resubmit) |
| Only late filing | `write_off`, unless there's proof of timely filing or an exception (then appeal) |
| Eligibility denial contradicted by the facts | `resubmit_as_is` |
| Nothing wrong | `no_action` |

## Test cases (11, all synthetic)

DOS-01 clean claim · DOS-02 benefit ended Nov 1, service in October, still covered · DOS-03 same benefit, service after it ended · DOS-04 coverage gap · DOS-05 filed 400 days late · DOS-06 plan changed after the DOS · DOS-07 retro eligibility contradicts a code-26 denial · DOS-08 before coverage · DOS-09 after coverage ended · DOS-10 no record · DOS-11 gap and late filing together
