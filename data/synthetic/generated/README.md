# Generated synthetic denials

> **Synthetic data only.** Every member, provider, plan, authorization, date and claim here is invented by [`scripts/generate_denials.py`](../../../scripts/generate_denials.py). No PHI, PII, Medicaid data, or internal data. Provider IDs use a `SYN-NPI-` format on purpose so they can't be mistaken for real NPIs. See the [README disclaimer](../../../README.md#disclaimer).

Regenerate (same seed, same files): `python scripts/generate_denials.py`

## Tables

| File | Rows | What it holds |
|---|---|---|
| `denials.csv` | 200 | One denied claim per row: claim details, the denial code (CARC/RARC), the scenario it came from, and for checkable ones the check that should catch it, the expected finding and the next action |
| `plans.csv` | 3 | The synthetic plans and their type: fee-for-service, managed care, or commercial |
| `members.csv` | 200 | One synthetic member per denial |
| `eligibility_segments.csv` | 204 | Coverage periods per member (a coverage gap or a plan switch needs two rows; "member not found" has none) |
| `other_coverage.csv` | 9 | Other insurance that should pay first (scenarios RJ-009 and RJ-055) |
| `providers.csv` | 20 | Synthetic providers; `SYN-NPI-020`'s enrollment ended 2025-12-31 |
| `coverage_rules.csv` | 18 | Which procedure codes each plan covers and which need prior authorization |
| `authorizations.csv` | 16 | Prior authorizations, built to mismatch the claim in exactly one way |
| `manifest.json` | — | Seed and row counts |

## How the denials are built

- Every one of the 58 active scenarios gets 3 denials. The other 26 go round-robin to the 18 scenarios the checks can diagnose, so each of those gets 4 or 5. **80 denials are checkable:** 43 by the date-of-service check, 20 by the prior auth matcher, 9 by the other-insurance check and 8 by the billed-payer check.
- The supporting tables are written so the facts **cause** the denial. Examples: a coverage-gap denial has a real gap around the date of service; a units-exceeded denial has an authorization whose remaining units are fewer than billed; a managed-care denial (RJ-056) has the member enrolled in `MEDICAID-MCO-A` but billed to `MEDICAID-FFS`; a wrong-payer denial (RJ-059) has a member who switched from `COMMERCIAL-X` to `MEDICAID-FFS` before the visit, with the old plan billed.
- For non-checkable scenarios, the facts are planted where it's simple (spend-down, lapsed provider) and the rest carry just the claim and the denial code for now. Their checks come later in Phase 2.

## How it's tested ([`tests/test_generator.py`](../../../tests/test_generator.py))

- Reproducible output, row counts against the manifest, every code against the mapping, every ID linked, every ID marked synthetic, sane dates.
- For each of the 80 checkable denials, the real check run on these tables must find **exactly the planted cause**, with the denial's own code and the expected next action.
- **No false alarms:** for each of the 80, the other three checks must find nothing.
