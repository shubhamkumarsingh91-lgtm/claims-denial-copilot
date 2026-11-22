"""Other-insurance check (third-party liability / coordination of benefits).

Rule: when a member has other insurance that pays first, the claim must go to
that insurer first, and the secondary claim must carry its payment details.
Medicaid is the payer of last resort (42 CFR 433.139), so for a Medicaid claim
ANY other coverage active on the date of service pays first. For other payers,
only coverage marked "primary" does.

Denial code: 22 (RJ-009 general COB, RJ-055 Medicaid TPL with remark MA04).
"""

from __future__ import annotations

from decimal import Decimal

from copilot.checks.result import (
    BILL_OTHER_COVERAGE, NO_ACTION, RESUBMIT_AS_IS, CheckResult, Finding, to_date,
)


def _active_on(row: dict, day) -> bool:
    start = to_date(row["start_date"])
    end = to_date(row["end_date"]) if row.get("end_date") else None
    return start <= day and (end is None or day <= end)


def _money(value) -> Decimal | None:
    return None if value in (None, "") else Decimal(str(value)).quantize(Decimal("0.01"))


def check_other_coverage(
    claim: dict,
    other_coverage: list[dict],
    billed_payer_type: str,
    medicaid_allowed: str | float | None = None,
    denial_carc: str | None = None,
) -> CheckResult:
    """Check whether another insurer should have been billed first.

    claim: {"claim_id", "member_id", "date_of_service", "billed_plan", "primary_paid_amount"?}
        primary_paid_amount: what the primary insurer paid; None/"" if the claim has no primary payment info.
    other_coverage: [{"member_id", "carrier", "coverage_order", "start_date", "end_date"}]
    billed_payer_type: "medicaid" or "commercial" (the payer this claim was sent to).
    medicaid_allowed: Medicaid's allowed amount for the service, if known; used only to
        estimate what Medicaid would pay after the primary.
    denial_carc: the code on the denial, if known, to spot a 22 the facts don't support.
    """
    dos = to_date(claim["date_of_service"])
    is_medicaid = billed_payer_type == "medicaid"
    pays_first = [
        row for row in other_coverage
        if row["member_id"] == claim["member_id"] and _active_on(row, dos)
        and (is_medicaid or row["coverage_order"] == "primary")
    ]
    primary_paid = _money(claim.get("primary_paid_amount"))

    if pays_first and primary_paid is None:
        carriers = ", ".join(sorted({r["carrier"] for r in pays_first}))
        why = (f"Medicaid pays last. {carriers} coverage was active on the date of service, "
               "and the claim has no payment information from it."
               if is_medicaid else
               f"{carriers} is primary on the date of service, and the claim has no payment information from it.")
        return CheckResult(
            check_name="other_coverage", passed=False,
            findings=[Finding(
                check="other_coverage_primary", carc="22", explanation=why,
                evidence={"date_of_service": dos.isoformat(), "billed_plan": claim["billed_plan"],
                          "other_coverage": [{"carrier": r["carrier"], "coverage_order": r["coverage_order"],
                                              "start_date": r["start_date"], "end_date": r.get("end_date") or None}
                                             for r in pays_first],
                          "primary_paid_amount": None},
            )],
            next_action=BILL_OTHER_COVERAGE,
            notes=[f"Bill {carriers} first, then resubmit with its payment details. If that coverage "
                   "has ended, ask the payer to update its other-coverage record."],
        )

    notes: list[str] = []
    next_action = NO_ACTION
    if pays_first and is_medicaid and medicaid_allowed is not None:
        allowed = _money(medicaid_allowed)
        expected = max(allowed - primary_paid, Decimal("0.00"))
        notes.append(f"Under a typical lesser-of method, Medicaid pays at most its allowed amount minus what "
                     f"the primary paid: ${allowed} - ${primary_paid} = ${expected}. State methods vary.")
    if not pays_first and denial_carc == "22":
        notes.append("Denied for other insurance (22), but no other coverage was active on the date of service. "
                     "Ask the payer to update its other-coverage record, then resubmit.")
        next_action = RESUBMIT_AS_IS
    return CheckResult(check_name="other_coverage", passed=True, next_action=next_action, notes=notes)


__all__ = ["check_other_coverage"]
