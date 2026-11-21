# Claims Denial Copilot: one-page PRD

> Independent personal project. Public reference information and synthetic data only. No PHI, PII, Medicaid data, or internal data. See the [README disclaimer](../README.md#disclaimer).

**Status:** v1 draft, 2026-11-21 · **Owner:** Shubham Singh

## Who it's for

**Primary user:** a biller or denial specialist at a **small, Medicaid-heavy provider** (a clinic, a therapy practice, a home-health agency) working a queue of denied claims, often alone or on a team of two or three.

**Not for:** patients, payers (who decide claims, not fix them), or large hospital systems that already buy enterprise denial-management tools.

## The problem

Billers know what denial codes mean. What they lack is time. Each denial means looking up eligibility, authorizations and payer rules in several places, working out the root cause, and deciding what to do. Medicaid adds its own traps: coverage judged on the date of service, retro eligibility, spend-down, other insurance paying first, managed care vs. fee-for-service. Denials left unworked are money the provider never collects.

## What v1 does

For one denied claim, the copilot:

1. Reads the denial code and claim details.
2. Runs rule-based checks against the facts (**built:** date of service, prior authorization; **next:** other insurance, frequency and duplicates, provider and place of service, code-pair edits, NPI).
3. Names the root cause with the evidence side by side.
4. Picks one next action: correct and resubmit, resubmit as is, request or update an authorization, bill other coverage, appeal, or write off.
5. Drafts the fix or appeal, and says **"needs human review"** when facts conflict or evidence is thin.

A human approves, edits or rejects every suggestion. Nothing is sent automatically.

**Design choice:** rules check the facts first, and the AI explains and drafts. Rules are cheap, exact and testable; the AI handles the messy parts (multiple causes, wording an appeal). That keeps invented answers to a minimum.

## Out of scope for v1

Submitting claims or appeals to payers · real patient or provider data · any state's internal rules or systems · fine-tuning models · production billing use.

## How success is measured

| Metric | Target for v1 | How it's measured |
|---|---|---|
| Right root cause | 80 of 100 test denials | Answer key of 100 cases (Phase 3) |
| Invented denial codes | 0 | Every code checked against the mapping (already enforced in tests for the rule-based checks) |
| Right next action | 80 of 100 | Same answer key |
| Correct escalation | 9 of 10 "should escalate" cases flagged | Same answer key |
| Time per denial | Under 2 minutes of human review | Timed demo with a test user |
| Cost per denial | Under $0.05 in AI usage | Logged per run |

## What could go wrong

| Risk | Mitigation |
|---|---|
| AI states a wrong cause confidently | Rules check facts first; evidence shown for every claim; low-confidence cases escalate |
| Payer rules differ by state and plan | Limits (like timely filing days) are settings, not hard-coded; scenarios say "verify" where rules vary |
| Codes change (X12 deactivates codes) | Mapping keeps a source per code; codes re-checked against X12 (code 15 was already caught as deactivated) |
| Users over-trust it | Human approval on every action; "not for real decisions" disclaimer until validated |
| Synthetic data hides real-world mess | Talk to working billers before building more (see open questions) |

## Open questions

1. Will billers at small practices pay for this, and how much? (Talk to 3 to 5 before Phase 4.)
2. Claude API as the main engine, or a local model? (Plan: Claude by default, compare both in the evals.)
3. Which denial categories cost small Medicaid providers the most? That decides which checks come next.
