# Generated synthetic denials

> **Synthetic data only.** Every member, provider, plan, authorization, date and claim here is invented by [`scripts/generate_denials.py`](../../../scripts/generate_denials.py). No PHI, PII, Medicaid data, or internal data. Provider IDs use a `SYN-NPI-` format on purpose so they can't be mistaken for real NPIs. See the [README disclaimer](../../../README.md#disclaimer).

Regenerate (same seed, same files): `python scripts/generate_denials.py`

## Tables

| File | Rows | What it holds |
|---|---|---|
| `denials.csv` | 200 | One denied claim per row: claim details, the denial code (CARC/RARC), the scenario it came from, and for checkable ones the expected finding and next action |
| `members.csv` | 200 | One synthetic member per denial |
| `eligibility_segments.csv` | 201 | Coverage periods per member (a coverage gap needs two rows; "member not found" has none) |
| `other_coverage.csv` | 3 | Other insurance that should pay first (scenario RJ-055) |
| `providers.csv` | 20 | Synthetic providers; `SYN-NPI-020`'s enrollment ended 2025-12-31 |
| `coverage_rules.csv` | 18 | Which procedure codes each plan covers and which need prior authorization |
| `authorizations.csv` | 20 | Prior authorizations, built to mismatch the claim in exactly one way |
| `manifest.json` | — | Seed and row counts |

## How the denials are built

- Every one of the 57 active scenarios gets at least 3 denials; the 14 scenarios the checks can diagnose get 5 or 6. **71 denials are checkable.**
- The supporting tables are written so the facts **cause** the denial. Examples: a coverage-gap denial has a real gap around the date of service; a units-exceeded denial has an authorization whose remaining units are fewer than billed; a managed-care denial (RJ-056) has the member enrolled in `MEDICAID-MCO-A` but billed to `MEDICAID-FFS`.
- For non-checkable scenarios, the facts are planted where it's simple (spend-down, other insurance, managed care, lapsed provider) and the rest carry just the claim and the denial code for now. The checks for those come in Phase 2.

## How it's tested ([`tests/test_generator.py`](../../../tests/test_generator.py))

Reproducible output, row counts against the manifest, every code against the mapping, every ID linked, every ID marked synthetic, sane dates, and, for each of the 71 checkable denials, the real check run on these tables must find exactly the planted cause, with the denial's own code and the expected next action.
