"""Shared result format for every rule-based check.

Every check returns a CheckResult so the AI engine (Phase 2) and the
evaluation scripts (Phase 3) can read all checks the same way.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date


# The standard next actions a biller can take. Every diagnosis ends in one.
CORRECT_AND_RESUBMIT = "correct_and_resubmit"
RESUBMIT_AS_IS = "resubmit_as_is"            # the facts now support payment (e.g. retro eligibility)
REQUEST_RETRO_AUTH = "request_retro_auth"
REQUEST_AUTH_UPDATE = "request_auth_update"  # extend dates or add units to an existing auth
APPEAL = "appeal"
BILL_OTHER_COVERAGE = "bill_other_coverage"   # another insurer, or the patient, should be billed first
BILL_CORRECT_PAYER = "bill_correct_payer"     # the claim went to the wrong plan (e.g. managed care vs FFS)
WRITE_OFF = "write_off"
NO_ACTION = "no_action"

NEXT_ACTIONS = {
    CORRECT_AND_RESUBMIT, RESUBMIT_AS_IS, REQUEST_RETRO_AUTH, REQUEST_AUTH_UPDATE,
    APPEAL, BILL_OTHER_COVERAGE, BILL_CORRECT_PAYER, WRITE_OFF, NO_ACTION,
}


@dataclass
class Finding:
    """One failed rule: what failed, the denial code it points to, and the evidence."""

    check: str        # short machine name, e.g. "no_eligibility_on_dos"
    carc: str         # denial code this failure normally produces (from carc_mapping.csv)
    explanation: str  # plain words for the biller
    evidence: dict    # the values the rule compared, so a human can verify


@dataclass
class CheckResult:
    check_name: str
    passed: bool
    findings: list[Finding] = field(default_factory=list)
    next_action: str = NO_ACTION
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def to_date(value: str | date) -> date:
    """Accept '2026-03-10' or a date object."""
    return value if isinstance(value, date) else date.fromisoformat(value)
