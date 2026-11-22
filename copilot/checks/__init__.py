"""Rule-based checks the copilot runs before (or instead of) asking the AI.

Each check is a pure function: same input, same output, no network, no database.
"""

from copilot.checks.dos_check import check_date_of_service
from copilot.checks.pa_matcher import check_prior_auth
from copilot.checks.payer_check import check_billed_payer
from copilot.checks.tpl_check import check_other_coverage

__all__ = ["check_date_of_service", "check_prior_auth", "check_other_coverage", "check_billed_payer"]
