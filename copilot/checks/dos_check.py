"""Date-of-service (DOS) check.

The rule payers follow: a claim is judged by the eligibility and coverage rules
in effect ON THE DATE OF SERVICE, not today. Timely filing is a separate check,
measured from the date of service to the date the claim was submitted.

All denial codes used here come from data/reference/carc_mapping.csv, except
CARC 29 (timely filing), which is a public X12 code added with the Medicaid
scenarios in step 1.5.
"""

from __future__ import annotations

from copilot.checks.result import (
    BILL_OTHER_COVERAGE, NO_ACTION, RESUBMIT_AS_IS, WRITE_OFF,
    CheckResult, Finding, to_date,
)

# Federal Medicaid rule: claims within 12 months of the date of service
# (42 CFR 447.45(d)). Payers set their own limits, so it is configurable.
DEFAULT_TIMELY_FILING_DAYS = 365

# Denial codes that mean "not eligible". If one of these was on the denial but
# eligibility now shows coverage on the DOS, the facts contradict the denial.
ELIGIBILITY_CARCS = {"26", "27", "31", "200"}


def _segment_covers(segment: dict, day) -> bool:
    start = to_date(segment["start_date"])
    end = to_date(segment["end_date"]) if segment.get("end_date") else None
    return start <= day and (end is None or day <= end)


def _rule_covers(rule: dict, day) -> bool:
    start = to_date(rule["effective_start"])
    end = to_date(rule["effective_end"]) if rule.get("effective_end") else None
    return start <= day and (end is None or day <= end)


def _eligibility_finding(segments: list[dict], dos) -> Finding:
    """Explain WHY there was no coverage on the DOS: never covered, not yet, gap, or ended."""
    if not segments:
        return Finding(
            check="member_not_found", carc="31",
            explanation="No eligibility record exists for this member, so the payer cannot match the patient.",
            evidence={"date_of_service": dos.isoformat(), "segments_on_file": 0},
        )
    starts = [to_date(s["start_date"]) for s in segments]
    ends = [to_date(s["end_date"]) if s.get("end_date") else None for s in segments]
    evidence = {
        "date_of_service": dos.isoformat(),
        "segments_on_file": [
            {"plan": s["plan"], "start_date": s["start_date"], "end_date": s.get("end_date")}
            for s in segments
        ],
    }
    if dos < min(starts):
        return Finding(
            check="dos_before_coverage", carc="26",
            explanation=f"The service happened before coverage started ({min(starts).isoformat()}).",
            evidence=evidence,
        )
    if all(e is not None for e in ends) and dos > max(ends):
        return Finding(
            check="dos_after_coverage_ended", carc="27",
            explanation=f"The service happened after coverage ended ({max(ends).isoformat()}).",
            evidence=evidence,
        )
    return Finding(
        check="dos_in_coverage_gap", carc="200",
        explanation="The service fell in a gap between two coverage periods.",
        evidence=evidence,
    )


def check_date_of_service(
    claim: dict,
    eligibility_segments: list[dict],
    coverage_rules: list[dict] | None = None,
    timely_filing_days: int = DEFAULT_TIMELY_FILING_DAYS,
    denial_carc: str | None = None,
) -> CheckResult:
    """Run the date-of-service checks on one claim.

    claim: {"claim_id", "date_of_service", "submission_date", "procedure_code"}
    eligibility_segments: [{"plan", "start_date", "end_date" (None = still open)}]
    coverage_rules: [{"procedure_code", "plan", "effective_start", "effective_end"}];
        None skips the coverage check.
    denial_carc: the code on the denial, if known, so the check can spot a
        denial that the current facts contradict (e.g. retro eligibility).
    """
    dos = to_date(claim["date_of_service"])
    submitted = to_date(claim["submission_date"])
    if submitted < dos:
        raise ValueError("submission_date is before date_of_service; check the claim data")

    findings: list[Finding] = []
    notes: list[str] = []

    # 1. Eligibility on the date of service (not today).
    dos_segment = next((s for s in eligibility_segments if _segment_covers(s, dos)), None)
    if dos_segment is None:
        findings.append(_eligibility_finding(eligibility_segments, dos))

    # 2. Was the procedure covered by that plan on that date?
    if dos_segment is not None and coverage_rules is not None:
        code, plan = claim["procedure_code"], dos_segment["plan"]
        same_plan_rules = [r for r in coverage_rules if r["procedure_code"] == code and r["plan"] == plan]
        if not any(_rule_covers(r, dos) for r in same_plan_rules):
            periods = [
                {"effective_start": r["effective_start"], "effective_end": r.get("effective_end")}
                for r in same_plan_rules
            ]
            why = (
                f"Procedure {code} is covered by {plan} only in other periods, not on the date of service."
                if periods else f"Procedure {code} is not a covered benefit of {plan}."
            )
            findings.append(Finding(
                check="not_covered_on_dos", carc="204", explanation=why,
                evidence={"date_of_service": dos.isoformat(), "plan_on_dos": plan,
                          "procedure_code": code, "coverage_periods_for_code": periods},
            ))

    # 3. Timely filing, measured from DOS to submission (separate from eligibility).
    days_to_submit = (submitted - dos).days
    if days_to_submit > timely_filing_days:
        findings.append(Finding(
            check="timely_filing_exceeded", carc="29",
            explanation=(f"Submitted {days_to_submit} days after the date of service; "
                         f"the limit is {timely_filing_days} days."),
            evidence={"date_of_service": dos.isoformat(), "submission_date": submitted.isoformat(),
                      "days_to_submit": days_to_submit, "limit_days": timely_filing_days},
        ))

    # 4. Classic trap: today's plan is not the plan that counts.
    current_segment = next((s for s in eligibility_segments if _segment_covers(s, submitted)), None)
    if dos_segment and current_segment and current_segment["plan"] != dos_segment["plan"]:
        notes.append(f"Plan changed: {dos_segment['plan']} on the date of service, "
                     f"{current_segment['plan']} at submission. Bill the plan in effect on the date of service.")

    # 5. Do the facts now contradict an eligibility denial? (e.g. retro eligibility added later)
    contradicts_denial = (
        denial_carc is not None and str(denial_carc) in ELIGIBILITY_CARCS and dos_segment is not None
    )
    if contradicts_denial:
        notes.append(f"Denied with eligibility code {denial_carc}, but eligibility now shows coverage "
                     f"under {dos_segment['plan']} on the date of service (possible retro eligibility).")

    # Next action, most blocking problem first.
    checks = {f.check for f in findings}
    if checks & {"member_not_found", "dos_before_coverage", "dos_after_coverage_ended", "dos_in_coverage_gap"}:
        next_action = BILL_OTHER_COVERAGE
        notes.append("Check for other coverage or pending retro eligibility before billing the patient.")
    elif "not_covered_on_dos" in checks:
        next_action = WRITE_OFF
        notes.append("Confirm the procedure code is right first; if it was wrong, correct and resubmit instead.")
    elif "timely_filing_exceeded" in checks:
        next_action = WRITE_OFF
        notes.append("If you have proof the claim was first filed on time, or an exception applies "
                     "(such as retro eligibility), appeal instead.")
    elif contradicts_denial:
        next_action = RESUBMIT_AS_IS
    else:
        next_action = NO_ACTION

    return CheckResult(
        check_name="date_of_service", passed=not findings,
        findings=findings, next_action=next_action, notes=notes,
    )


__all__ = ["check_date_of_service", "DEFAULT_TIMELY_FILING_DAYS"]
