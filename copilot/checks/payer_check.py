"""Billed-payer check: was the claim sent to the plan that covered the member on the DOS?

The common Medicaid case: the member was enrolled in a managed care plan on the
date of service, but the claim was billed to fee-for-service Medicaid.
Denial code 24 (RJ-056).

Other wrong-payer cases (e.g. billed a plan the member had left) have no
scenario in the mapping yet, so they're reported as a note, not given a code.
"""

from __future__ import annotations

from copilot.checks.result import BILL_CORRECT_PAYER, CheckResult, Finding, to_date


def check_billed_payer(claim: dict, eligibility_segments: list[dict], managed_care_plans: set[str]) -> CheckResult:
    """claim: {"claim_id", "date_of_service", "billed_plan"}
    eligibility_segments: [{"plan", "start_date", "end_date"}] for this member
    managed_care_plans: names of plans that are managed care (MCO) plans
    """
    dos = to_date(claim["date_of_service"])
    billed = claim["billed_plan"]
    dos_plan = next(
        (s["plan"] for s in eligibility_segments
         if to_date(s["start_date"]) <= dos and (not s.get("end_date") or dos <= to_date(s["end_date"]))),
        None,
    )

    if dos_plan is None:
        return CheckResult(check_name="billed_payer", passed=True,
                           notes=["Skipped: no coverage on the date of service (see the date-of-service check)."])
    if dos_plan == billed:
        return CheckResult(check_name="billed_payer", passed=True)

    if dos_plan in managed_care_plans and billed not in managed_care_plans:
        return CheckResult(
            check_name="billed_payer", passed=False,
            findings=[Finding(
                check="billed_ffs_member_in_managed_care", carc="24",
                explanation=(f"On the date of service the member was enrolled in {dos_plan}, a managed care plan, "
                             f"so the claim belongs there, not to {billed}."),
                evidence={"date_of_service": dos.isoformat(), "billed_plan": billed, "plan_on_dos": dos_plan},
            )],
            next_action=BILL_CORRECT_PAYER,
            notes=[f"Send the claim to {dos_plan}, and check that the provider is in its network."],
        )

    return CheckResult(
        check_name="billed_payer", passed=True, next_action=BILL_CORRECT_PAYER,
        notes=[f"Billed {billed}, but the member was covered by {dos_plan} on the date of service. "
               "Bill that plan. (No denial scenario covers this case yet, so no code is given.)"],
    )


__all__ = ["check_billed_payer"]
