"""Provider eligibility check: could this provider be paid for a service on this date?

Several different facts lead to the same denial code (B7, "provider not
eligible on this date"), and each needs a different fix. This check says which
one it is, using the provider's record as it stood ON THE DATE OF SERVICE:

| Fact                                         | Finding               | Code | Scenario |
|----------------------------------------------|-----------------------|------|----------|
| No provider record for the NPI on the claim  | provider_not_on_file  | 208  | RJ-029   |
| Provider excluded from federal programs      | provider_excluded     | B7   | RJ-033   |
| Never enrolled with this payer               | provider_not_enrolled | B7   | RJ-035   |
| Service before enrollment/credentialing      | dos_before_enrollment | B7   | RJ-030   |
| Service after enrollment ended (e.g. no      | enrollment_ended      | B7   | RJ-057   |
|   revalidation)                              |                       |      |          |
| License expired before the service           | license_expired       | B7   | RJ-028   |

All problems found are reported, not just the first.
"""

from __future__ import annotations

from copilot.checks.result import (
    CORRECT_AND_RESUBMIT, FIX_PROVIDER_ENROLLMENT, WRITE_OFF,
    CheckResult, Finding, to_date,
)

END_REASON_WORDS = {
    "revalidation_not_completed": "revalidation wasn't completed",
    "voluntary": "the provider ended it",
    "terminated": "the payer terminated it",
}


def _date_or_none(value):
    return to_date(value) if value else None


def check_provider_eligibility(claim: dict, providers: list[dict]) -> CheckResult:
    """claim: {"claim_id", "date_of_service", "rendering_npi"}
    providers: [{"npi", "name", "provider_type", "enrolled_from", "enrolled_to", "end_reason",
                 "license_expires", "excluded_from"}]; blank dates mean "none".
    """
    dos = to_date(claim["date_of_service"])
    npi = claim["rendering_npi"]
    record = next((p for p in providers if p["npi"] == npi), None)

    if record is None:
        return CheckResult(
            check_name="provider_eligibility", passed=False,
            findings=[Finding(
                check="provider_not_on_file", carc="208",
                explanation=f"No provider record matches the NPI on the claim ({npi}).",
                evidence={"rendering_npi": npi, "date_of_service": dos.isoformat()},
            )],
            next_action=CORRECT_AND_RESUBMIT,
            notes=["Check the NPI for a typo, and that it's the rendering provider's own NPI; "
                   "correct it and resubmit."],
        )

    name = record["name"]
    findings: list[Finding] = []
    enrolled_from = _date_or_none(record.get("enrolled_from"))
    enrolled_to = _date_or_none(record.get("enrolled_to"))
    license_expires = _date_or_none(record.get("license_expires"))
    excluded_from = _date_or_none(record.get("excluded_from"))

    if excluded_from and excluded_from <= dos:
        findings.append(Finding(
            check="provider_excluded", carc="B7",
            explanation=f"{name} was on the federal exclusion list from {excluded_from.isoformat()}, "
                        "before the date of service.",
            evidence={"npi": npi, "date_of_service": dos.isoformat(), "excluded_from": excluded_from.isoformat()},
        ))

    if enrolled_from is None:
        findings.append(Finding(
            check="provider_not_enrolled", carc="B7",
            explanation=f"{name} has never been enrolled with this payer.",
            evidence={"npi": npi, "provider_type": record.get("provider_type"), "enrolled_from": None},
        ))
    elif dos < enrolled_from:
        findings.append(Finding(
            check="dos_before_enrollment", carc="B7",
            explanation=f"The service was on {dos.isoformat()}, but {name}'s enrollment "
                        f"(credentialing) only started on {enrolled_from.isoformat()}.",
            evidence={"npi": npi, "date_of_service": dos.isoformat(), "enrolled_from": enrolled_from.isoformat()},
        ))
    elif enrolled_to and dos > enrolled_to:
        reason = END_REASON_WORDS.get(record.get("end_reason") or "", "")
        findings.append(Finding(
            check="enrollment_ended", carc="B7",
            explanation=f"{name}'s enrollment ended on {enrolled_to.isoformat()}"
                        + (f" because {reason}" if reason else "") + ", before the date of service.",
            evidence={"npi": npi, "date_of_service": dos.isoformat(), "enrolled_to": enrolled_to.isoformat(),
                      "end_reason": record.get("end_reason") or None},
        ))

    if license_expires and license_expires < dos:
        findings.append(Finding(
            check="license_expired", carc="B7",
            explanation=f"{name}'s license expired on {license_expires.isoformat()}, before the date of service.",
            evidence={"npi": npi, "date_of_service": dos.isoformat(), "license_expires": license_expires.isoformat()},
        ))

    if not findings:
        return CheckResult(check_name="provider_eligibility", passed=True)

    checks = {f.check for f in findings}
    if "provider_excluded" in checks:
        next_action = WRITE_OFF
        notes = ["Medicare and Medicaid can't pay for services by an excluded provider. Don't resubmit; "
                 "raise it with compliance."]
    else:
        next_action = FIX_PROVIDER_ENROLLMENT
        notes = []
        if checks & {"provider_not_enrolled", "dos_before_enrollment"}:
            notes.append("Ask the payer whether the enrollment effective date can cover the date of service. "
                         "If it can't, the service can't be billed to this payer.")
        if "enrollment_ended" in checks:
            notes.append("Complete revalidation or re-enrollment; resubmit only if reinstatement is "
                         "backdated to cover the date of service.")
        if "license_expired" in checks:
            notes.append("Get proof of license renewal. If the license was renewed with no gap, send the "
                         "payer the updated license and resubmit; if there was a gap, it can't be billed.")
    return CheckResult(check_name="provider_eligibility", passed=False,
                       findings=findings, next_action=next_action, notes=notes)


__all__ = ["check_provider_eligibility"]
