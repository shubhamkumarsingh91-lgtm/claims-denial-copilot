# Feature: provider eligibility check

> Independent personal project. Public reference information and synthetic data only. See the [README disclaimer](../../README.md#disclaimer).

**Code:** [`copilot/checks/provider_check.py`](../../copilot/checks/provider_check.py) · **Test cases:** [`data/synthetic/provider_cases.json`](../../data/synthetic/provider_cases.json) · **Tests:** [`tests/test_checks.py`](../../tests/test_checks.py)

## The problem

A payer only pays a provider who was allowed to bill it **on the date of service**. Five different facts produce the same denial code, B7 ("provider not eligible on this date"), and each needs a different fix. Treating them alike wastes time: an excluded provider should never be resubmitted, while a late revalidation sometimes can be.

## What it checks

| Fact on the date of service | Finding | Code | Scenario | Next action |
|---|---|---|---|---|
| No provider record matches the NPI on the claim | `provider_not_on_file` | 208 | RJ-029 | `correct_and_resubmit` (likely a typo or the wrong NPI) |
| Provider on the federal exclusion list | `provider_excluded` | B7 | RJ-033 | `write_off`: Medicare and Medicaid can't pay; raise with compliance |
| Never enrolled with this payer | `provider_not_enrolled` | B7 | RJ-035 | `fix_provider_enrollment` |
| Service before enrollment or credentialing started | `dos_before_enrollment` | B7 | RJ-030 | `fix_provider_enrollment`: ask if the start date can be backdated |
| Service after enrollment ended (e.g. revalidation not completed) | `enrollment_ended` | B7 | RJ-057 | `fix_provider_enrollment`: resubmit only if reinstatement is backdated |
| License expired before the service | `license_expired` | B7 | RJ-028 | `fix_provider_enrollment`: resubmit only if renewed with no gap |

- Every problem found is reported, not just the first.
- An exclusion outranks everything else when choosing the next action, because it's the one case where resubmitting is never right.
- Dates are inclusive: a service on the first or last day of enrollment is fine, and an exclusion that starts after the service doesn't count.

Medicaid providers must revalidate their enrollment at least every 5 years ([42 CFR 455.414](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-455/subpart-E/section-455.414)). The exclusion list in real life is the public HHS-OIG LEIE; the data here is synthetic.

**Not covered yet:** whether the NPI is valid in the public national registry (NPPES). This check only asks whether the payer has a record for it. Checking the registry is the `lookup_npi` tool in step 2.1.

## Test cases (12, all synthetic)

PRV-01 all good · PRV-02 NPI not on file → 208 · PRV-03 license expired · PRV-04 billed before credentialing · PRV-05 service on the day enrollment starts → fine · PRV-06 excluded → write off · PRV-07 facility never enrolled · PRV-08 revalidation not completed · PRV-09 service on the last enrolled day → fine · PRV-10 enrollment ended *and* license expired → both reported · PRV-11 exclusion starts after the service → fine · PRV-12 payer terminated the enrollment → reason shown
