"""Prior authorization (PA) matcher.

PA denials usually come from a mismatch between the claim and the approved
authorization, but the denial rarely says WHICH part. This check compares the
claim with every authorization on file for the member and reports every field
that fails, not just the first one.

Denial codes come from data/reference/carc_mapping.csv:
197 missing (RJ-039), 302 expired (RJ-040), 284 different procedure (RJ-041),
198 units exceeded (RJ-042), 296 different provider (RJ-043).
"""

from __future__ import annotations

from copilot.checks.result import (
    CORRECT_AND_RESUBMIT, NO_ACTION, REQUEST_AUTH_UPDATE, REQUEST_RETRO_AUTH,
    CheckResult, Finding, to_date,
)


def _compare(claim: dict, auth: dict) -> list[Finding]:
    """Every way this one authorization fails to cover the claim."""
    dos = to_date(claim["date_of_service"])
    start, end = to_date(auth["start_date"]), to_date(auth["end_date"])
    failures: list[Finding] = []

    if claim["procedure_code"] != auth["procedure_code"]:
        failures.append(Finding(
            check="procedure_code_mismatch", carc="284",
            explanation=(f"The authorization approves {auth['procedure_code']}, "
                         f"but the claim bills {claim['procedure_code']}."),
            evidence={"auth_id": auth["auth_id"], "claim_code": claim["procedure_code"],
                      "auth_code": auth["procedure_code"]},
        ))

    if dos > end:
        failures.append(Finding(
            check="dos_after_auth_expired", carc="302",
            explanation=f"The service date is after the authorization ended ({end.isoformat()}).",
            evidence={"auth_id": auth["auth_id"], "date_of_service": dos.isoformat(),
                      "auth_start": start.isoformat(), "auth_end": end.isoformat()},
        ))
    elif dos < start:
        failures.append(Finding(
            check="dos_before_auth_start", carc="197",
            explanation=(f"The service date is before the authorization started ({start.isoformat()}), "
                         "so no approval covered it."),
            evidence={"auth_id": auth["auth_id"], "date_of_service": dos.isoformat(),
                      "auth_start": start.isoformat(), "auth_end": end.isoformat()},
        ))

    units = int(claim.get("units", 1))
    used, approved = int(auth.get("units_used", 0)), int(auth["approved_units"])
    if used + units > approved:
        failures.append(Finding(
            check="units_exceeded", carc="198",
            explanation=(f"Billing {units} unit(s) with {used} already used goes over the "
                         f"{approved} approved; {max(approved - used, 0)} remain."),
            evidence={"auth_id": auth["auth_id"], "claim_units": units, "units_used": used,
                      "approved_units": approved, "units_remaining": max(approved - used, 0)},
        ))

    auth_npi, claim_npi = auth.get("npi"), claim.get("rendering_npi")
    if auth_npi and claim_npi and auth_npi != claim_npi:
        failures.append(Finding(
            check="provider_mismatch", carc="296",
            explanation="The authorization was approved for a different provider.",
            evidence={"auth_id": auth["auth_id"], "claim_npi": claim_npi, "auth_npi": auth_npi},
        ))

    return failures


def check_prior_auth(claim: dict, authorizations: list[dict], pa_required: bool = True) -> CheckResult:
    """Match one claim against the member's authorizations.

    claim: {"claim_id", "member_id", "procedure_code", "date_of_service", "units", "rendering_npi"?}
    authorizations: [{"auth_id", "member_id", "procedure_code", "start_date", "end_date",
                      "approved_units", "units_used", "npi"?}]
    pa_required: whether this procedure needs PA under the payer's (public) PA list.
    """
    if not pa_required:
        return CheckResult(check_name="prior_auth", passed=True,
                           notes=["Prior authorization is not required for this procedure."])

    candidates = [a for a in authorizations if a["member_id"] == claim["member_id"]]
    if not candidates:
        return CheckResult(
            check_name="prior_auth", passed=False,
            findings=[Finding(
                check="no_auth_on_file", carc="197",
                explanation="This procedure needs prior authorization and none is on file for the member.",
                evidence={"member_id": claim["member_id"], "procedure_code": claim["procedure_code"],
                          "date_of_service": claim["date_of_service"], "auths_on_file": 0},
            )],
            next_action=REQUEST_RETRO_AUTH,
            notes=["Check whether the payer allows retro authorization; if not, appeal with clinical notes."],
        )

    # Pick the authorization that comes closest (fewest failures; first one on a tie).
    scored = [(auth, _compare(claim, auth)) for auth in candidates]
    best_auth, failures = min(scored, key=lambda pair: len(pair[1]))

    if not failures:
        return CheckResult(check_name="prior_auth", passed=True,
                           notes=[f"Authorization {best_auth['auth_id']} covers this claim."])

    checks = {f.check for f in failures}
    notes = [f"Closest authorization on file: {best_auth['auth_id']}."]
    if "procedure_code_mismatch" in checks:
        next_action = CORRECT_AND_RESUBMIT
        notes.append("If the claim code is a typo, correct it and resubmit. If the billed code is right, "
                     "request an authorization update for it.")
    elif checks & {"provider_mismatch", "dos_after_auth_expired", "dos_before_auth_start", "units_exceeded"}:
        next_action = REQUEST_AUTH_UPDATE
        notes.append("Ask the payer to update the authorization (dates, units, or provider). "
                     "If they refuse, appeal with clinical notes.")
    else:  # defensive: every failure type above is handled
        next_action = NO_ACTION

    return CheckResult(check_name="prior_auth", passed=False, findings=failures,
                       next_action=next_action, notes=notes)


__all__ = ["check_prior_auth"]
