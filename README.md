# Claims Denial Copilot

An AI copilot for provider billing teams. For each denied claim, it finds the likely root cause, checks the facts with tools, and drafts the fix. A human approves every suggestion.

> **Disclaimer:** This is an independent personal project. It is not affiliated with, endorsed by, or built for any employer, state agency, Medicaid program, or vendor. It uses only public reference information and fully synthetic examples. It contains no PHI, no SSNs, no real member or provider records, and no internal or confidential material from any organization. Outputs are for demonstration and learning only and must not be used for real billing, coverage, or medical decisions.

---

## The problem

When a provider bills an insurer, a large share of claims come back denied. A billing specialist then has to work out *why* (eligibility? authorization? coding? provider enrollment?), fix the claim, and resubmit or appeal it. With hundreds of denials in a queue, that's slow, repetitive work, and unworked denials are lost revenue.

Billers already know what denial codes mean. What they don't have is **time**. So this project doesn't explain claims. It does the digging and drafts the fix.

## What the copilot does (target v1)

For each denial in the work queue:

1. **Reads** the denial: the CARC/RARC reason codes and claim fields (from a synthetic 835 remittance or CSV row)
2. **Checks the facts** with tools: eligibility *on the date of service*, NPI status, prior-auth match, NCCI code-pair edits
3. **Returns structured output**: root-cause category, evidence (which tool said what), fix steps, corrected-claim checklist, appeal draft, confidence
4. **Escalates** with "needs human review" when the tools disagree or the evidence is thin, instead of guessing
5. **Waits for a human**: the biller approves, edits, or rejects each suggestion

## Scope

| In scope | Out of scope |
|---|---|
| Denied claims and provider billing staff | Patients as users |
| Any payer: a **payer-agnostic core** (CARC/RARC, 835, NCCI, NPI work the same for Medicare, Medicaid, commercial) | Real patient, member, or provider data |
| **Medicaid rules as the specialty layer** | Anything from any employer, agency, or vendor |
| Synthetic data and public reference information | Fine-tuning models, multi-agent frameworks |
| Measuring accuracy with an eval harness | Production deployment for real billing |

## Current status

**Phase 1: Foundation (in progress)**

- [x] 50 denial scenarios across eligibility, coding, provider, and authorization ([`kb/`](kb/))
- [x] Every scenario mapped to a real **Claim Adjustment Reason Code (CARC)** ([`data/reference/carc_mapping.csv`](data/reference/carc_mapping.csv), [`kb/rejection_mapping.md`](kb/rejection_mapping.md)): 38 confirmed, 4 to verify, 7 need a remark code (RARC), 1 dropped
- [ ] Add RARCs for the 7 generic CARC-16 scenarios
- [ ] Add Medicaid-specific scenarios (e.g., spend-down, retro eligibility, timely filing)
- [ ] Synthetic denial data generator
- [ ] One-page PRD

## Roadmap

| Phase | What gets built | Done when |
|---|---|---|
| 1. Foundation | Real codes, Medicaid layer, synthetic data, PRD | No invented codes; 200 synthetic denials |
| 2. Tools + engine | 5 tools + LLM with tool use and structured JSON output | One command runs a denial end to end with tool evidence |
| 3. Evaluation | 100-case answer key + automated scoring | A score per version, plus a list of failures with reasons |
| 4. Copilot UI | Streamlit work queue with Approve / Edit / Reject | A new user can work 10 denials without help |
| 5. Analytics + ship | SQL denial-trend dashboard, public demo, video | A public link works; README shows the eval scores |

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for details.

## Repository layout

```
claims-denial-copilot/
  README.md
  kb/                    denial scenarios (provider, analyst views) + code mappings
  data/reference/        carc_mapping.csv
  evals/seed_scenarios/  multi-issue and edge-case prompts carried over from v1
  docs/                  ROADMAP.md, build-log.md
```

Planned as the phases land: `copilot/` (tools, engine, prompts), `evals/` harness, `app/` (Streamlit), `analytics/` (SQL), `scripts/` (synthetic data).

## About the codes

CARC and RARC codes are maintained by [X12](https://x12.org/codes/claim-adjustment-reason-codes). The official descriptions are copyrighted, so this repo uses the code numbers with **plain-language summaries in our own words** and links to X12 as the source. CPT descriptions (owned by the AMA) are not reproduced.

## Background

This project grew out of [healthcare-translator-ai](https://github.com/shubhamkumarsingh91-lgtm/healthcare-translator-ai), a persona-based claims translator built with Ollama, Open WebUI, and a local RAG knowledge base. The build log in [`docs/build-log.md`](docs/build-log.md) covers what that version taught me and why the project changed direction.
