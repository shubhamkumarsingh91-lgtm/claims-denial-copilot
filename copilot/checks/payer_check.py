"""Billed-payer check: was the claim sent to the plan that covered the member on the DOS?

Two kinds of wrong payer, each with its own denial code:
- Managed care vs. fee-for-service (RJ-056, code 24): the member was in a managed
  care plan on the date of service, but the claim went to fee-for-service Medicaid.
- Any other wrong payer (RJ-059, code 109): the claim went to a plan that didn't
  cover the member on the date of service (an old card on file, the wrong managed
  care plan, a commercial plan instead of Medicaid, and so on).
"""

from __future__ import annotations

from copilot.checks.result import BILL_CORRECT_PAYER, CheckResult, Finding, to_date


def check_billed_payer(
    claim: dict,
    eligibility_segments: list[dict],
    managed_care_plans: set[str],
    fee_for_service_plans: set[str],
) -> CheckResult:
    """claim: {"claim_id", "date_of_service", "billed_plan"}
    eligibility_segments: [{"plan", "start_date", "end_date"}] for this member
    managed_care_plans: names of Medicaid managed care (MCO) plans
    fee_for_service_plans: names of Medicaid fee-for-service plans
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

    evidence = {"date_of_service": dos.isoformat(), "billed_plan": billed, "plan_on_dos": dos_plan}

    if dos_plan in managed_care_plans and billed in fee_for_service_plans:
        return CheckResult(
            check_name="billed_payer", passed=False,
            findings=[Finding(
                check="billed_ffs_member_in_managed_care", carc="24",
                explanation=(f"On the date of service the member was enrolled in {dos_plan}, a managed care plan, "
                             f"so the claim belongs there, not to {billed}."),
                evidence=evidence,
            )],
            next_action=BILL_CORRECT_PAYER,
            notes=[f"Send the claim to {dos_plan}, and check that the provider is in its network."],
        )

    return CheckResult(
        check_name="billed_payer", passed=False,
        findings=[Finding(
            check="wrong_payer", carc="109",
            explanation=(f"On the date of service the member was covered by {dos_plan}, not {billed}, "
                         f"so {billed} won't pay this claim."),
            evidence=evidence,
        )],
        next_action=BILL_CORRECT_PAYER,
        notes=[f"Send the claim to {dos_plan} and update the patient's insurance on file. "
               "The filing deadline usually keeps running while a claim sits at the wrong payer."],
    )


__all__ = ["check_billed_payer"]
