# Feature: other-insurance check (TPL / coordination of benefits)

> Independent personal project. Public reference information and synthetic data only. See the [README disclaimer](../../README.md#disclaimer).

**Code:** [`copilot/checks/tpl_check.py`](../../copilot/checks/tpl_check.py) · **Test cases:** [`data/synthetic/tpl_cases.json`](../../data/synthetic/tpl_cases.json) · **Tests:** [`tests/test_checks.py`](../../tests/test_checks.py)

## The problem

When a patient has other insurance that pays first, the claim must go there first, and the claim to the second payer must include what the first one paid. Medicaid is the **payer of last resort** ([42 CFR 433.139](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-433/subpart-D/section-433.139)), so for a Medicaid claim **any** other coverage active on the date of service pays first. For other payers, only coverage marked "primary" does.

## How it works

| Situation | Result | Code | Next action |
|---|---|---|---|
| Other coverage pays first, active on the date of service, and the claim has no payment info from it | Fails | 22 (with MA04 for Medicaid) | `bill_other_coverage` |
| The primary paid (even $0), and Medicaid's allowed amount is known | Passes, with an estimate of what Medicaid would pay | — | `no_action` |
| Denied with 22, but no other coverage was active on the date of service | Passes; the denial doesn't hold | — | `resubmit_as_is`, after asking the payer to update its record |
| No other coverage | Passes | — | `no_action` |

**The payment estimate** uses a typical "lesser-of" method: Medicaid pays at most its allowed amount minus what the primary paid, never below $0. State methods vary, and the note says so. Amounts use exact decimal maths, not floating point, so cents never drift.

**A $0 primary payment counts as payment information.** A primary that applied the whole bill to the deductible still processed the claim, so it isn't flagged.

## Test cases (9, all synthetic)

TPL-01 Medicaid billed first · TPL-02 primary paid $80 of $120 → at most $40 · TPL-03 primary paid more than allowed → $0, never negative · TPL-04 denied for other insurance that had ended → the denial doesn't hold · TPL-05 commercial claim, other coverage is secondary → fine · TPL-06 commercial claim, other plan is primary → flagged (general COB) · TPL-07 no other coverage · TPL-08 Medicaid treats even "secondary" coverage as paying first · TPL-09 primary paid $0 → not flagged
