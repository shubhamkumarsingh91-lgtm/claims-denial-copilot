# Feature: prior authorization matcher

> Independent personal project. Public reference information and synthetic data only. See the [README disclaimer](../../README.md#disclaimer).

**Code:** [`copilot/checks/pa_matcher.py`](../../copilot/checks/pa_matcher.py) · **Test cases:** [`data/synthetic/pa_cases.json`](../../data/synthetic/pa_cases.json) · **Tests:** [`tests/test_checks.py`](../../tests/test_checks.py)

## The problem

Prior authorization (PA) denials usually come from a mismatch between the claim and the approved authorization, but the denial rarely says **which** part didn't match.

## How it works

1. If the procedure doesn't need PA, it passes.
2. If no authorization is on file for the member, it fails with **197** (missing PA).
3. Otherwise it compares the claim with **every** authorization on file for the member, picks the closest one (fewest problems), and reports **every** problem with it:

| Check | Fails when | Code |
|---|---|---|
| Procedure code | Claim code differs from the approved code | 284 |
| Date window | DOS is after the authorization ended | 302 |
| | DOS is before the authorization started | 197 |
| Units | Units already used + units billed > units approved | 198 |
| Provider | Authorization names a different provider | 296 |

Each problem shows the claim value and the authorization value side by side, so the biller can verify it in seconds.

## Next action

| Situation | Next action |
|---|---|
| No authorization on file | `request_retro_auth` (appeal with clinical notes if retro auth isn't allowed) |
| Code mismatch (with or without other problems) | `correct_and_resubmit` if the claim code is a typo; otherwise request an authorization update |
| Dates, units, or provider only | `request_auth_update` (appeal if refused) |
| Everything matches | `no_action` |

## Test cases (9, all synthetic)

PA-01 all match · PA-02 none on file · PA-03 surgery approved once, billed twice · PA-04 one day after expiry · PA-05 wrong code · PA-06 code, expiry, and provider wrong at once · PA-07 two authorizations, the newer one covers it · PA-08 PA not required · PA-09 before the authorization started
