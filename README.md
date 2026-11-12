# Claims Denial Copilot

**An AI assistant that helps medical billing teams fix denied insurance claims: it finds out why a claim was denied, checks the facts, and drafts the fix. A human approves every step.**

<a id="disclaimer"></a>

> **Disclaimer: independent project, public and synthetic data only**
>
> - **Independent:** I built this project on my own time and my own personal computer, outside of any job. No employer, state agency, Medicaid program, health plan, or vendor is connected to it, has endorsed it, or has contributed to it.
> - **No PHI or PII, ever:** no real patient's health information and no information that could identify a real person (names, SSNs, member IDs, dates of birth, addresses, phone numbers, or anything similar) is used anywhere in this project.
> - **No Medicaid or agency data:** no claims, member, provider, eligibility, or payment records from any Medicaid program, state agency, or payer are used, and no internal documents, system screenshots, tickets, reports, or business rules from any organization.
> - **Only two kinds of data:** (1) **public** reference information that anyone can look up, such as standard denial-code numbers and public CMS and NPI registry data, and (2) **synthetic** examples I invented. Any names, IDs, dates, or plans in examples are made up.
> - **Not for real decisions:** the outputs are for learning and demonstration only and must never be used for real billing, coverage, or medical decisions.

---

## Contents

1. [The problem, in plain words](#1-the-problem-in-plain-words)
2. [What the copilot does](#2-what-the-copilot-does)
3. [A worked example](#3-a-worked-example)
4. [What's in and out of scope](#4-whats-in-and-out-of-scope)
5. [The project plan, step by step](#5-the-project-plan-step-by-step)
6. [Where the project is today](#6-where-the-project-is-today)
7. [How the repository is organized](#7-how-the-repository-is-organized)
8. [Glossary](#8-glossary)
9. [How this project started](#9-how-this-project-started)

---

## 1. The problem, in plain words

When a doctor's office or hospital treats a patient, it sends a bill (a **claim**) to the patient's insurance. Many claims come back **denied**, with a short reason code instead of a payment.

Someone on the billing team then has to:

1. Figure out **why** it was denied: was the patient covered that day? Was approval needed in advance? Was a billing code wrong?
2. Look up the facts in several different systems.
3. **Fix** the claim and resend it, or write an appeal.

Billers already know what the codes mean. What they lack is **time**: with hundreds of denials in a queue, the digging is slow and repetitive, and every denial left unworked is money the provider never collects.

## 2. What the copilot does

The copilot does the digging so the biller doesn't have to start from zero. For each denied claim:

| Step | The copilot… | Example |
|---|---|---|
| 1. Read | Reads the denial code and the claim details | "Code 27: coverage ended" |
| 2. Check | Uses **tools** to check facts instead of guessing | Looks up whether the patient was covered *on the date of the visit* |
| 3. Explain | Names the most likely root cause and shows its evidence | "Old plan ended Feb 28; a new plan started Mar 1" |
| 4. Suggest | Drafts the fix: what to correct, what to resend, or an appeal letter | "Bill the new plan instead" |
| 5. Escalate | Says **"needs human review"** when facts conflict or evidence is thin | Two tools disagree, so it flags the case instead of guessing |
| 6. Wait | The biller **approves, edits, or rejects** the suggestion | Nothing is sent without a human |

It's a *copilot*, not an autopilot: it prepares the work, and the person stays in charge.

## 3. A worked example

*(Synthetic example: invented patient, invented plans.)*

**The denial:** a clinic billed an office visit on **March 10**. The insurer denied it with reason code **27**, which means the service happened after the patient's coverage ended.

**What a biller would normally do:** open the eligibility system, search for the patient, read the coverage dates, then work out what to do next. Repeated for every claim in the queue.

**What the copilot does:**

1. Reads code 27 and knows to check coverage dates.
2. Calls `check_eligibility(member, 2026-03-10)` and finds that Plan A ended **Feb 28** and Plan B started **Mar 1**.
3. Concludes: *"The denial is correct for Plan A. The patient was covered by Plan B on the date of service."*
4. Suggests: *"Resubmit the claim to Plan B with the new member ID. No appeal needed."*
5. The biller checks it, clicks **Approve**, and moves to the next denial.

Note the trap in step 2: a patient who is "active" **today** may not have been covered **on the day of the visit**. The copilot checks the date of service, not the current status.

## 4. What's in and out of scope

| In scope | Out of scope |
|---|---|
| Denied claims, worked by provider billing staff | Patients as users |
| **Any insurer**: the denial codes work the same for Medicare, Medicaid, and commercial plans | Real patient, member, or provider data |
| **Medicaid rules as a specialty layer** on top | Anything from any employer, agency, or vendor |
| Made-up (synthetic) data and public reference information | Fine-tuning AI models |
| Measuring how accurate the AI is | Real billing in production |

## 5. The project plan, step by step

The project runs in **5 phases over about 12–13 weeks** (about 7 hours a week). Each phase ends with something that works and can be shown.

### Phase 1: Foundation (get the facts right)

*Goal: the copilot learns from real denial codes and realistic examples, not made-up ones.*

- [x] **Step 1.1:** Write 50 denial scenarios across four areas: eligibility, coding, provider, and prior authorization ([`kb/`](kb/))
- [x] **Step 1.2:** Map every scenario to a real denial code (CARC) ([`kb/rejection_mapping.md`](kb/rejection_mapping.md), [`data/reference/carc_mapping.csv`](data/reference/carc_mapping.csv))
- [x] **Step 1.3:** Tag each scenario as "all insurers" or "commercial only"
- [x] **Step 1.4:** Add remark codes (RARCs) for the 7 scenarios that use the general code 16, and confirm the 4 marked "verify" (3 scenarios still marked "verify", see below)
- [ ] **Step 1.5:** Add Medicaid-specific scenarios: spend-down, retroactive eligibility, timely filing, other insurance that pays first, provider enrollment
- [ ] **Step 1.6:** Build a generator that creates about 200 fake denials with patients, coverage dates, authorizations, and providers
- [ ] **Step 1.7:** Write a one-page product requirements document (PRD): who it's for, the problem, what v1 does, how success is measured, what could go wrong

**Done when:** no invented codes remain, and 200 synthetic denials exist.

### Phase 2: Tools and engine (make it think and check)

*Goal: the copilot can take one denial and produce a checked, structured answer.*

- [ ] **Step 2.1:** Build five tools the AI can call:
  - `check_eligibility`: was the patient covered **on the date of service**?
  - `lookup_carc`: what kind of denial is this code?
  - `check_auth`: does the prior approval match the service, provider, and date?
  - `check_ncci`: are these two procedure codes allowed together? (public Medicare edit tables)
  - `lookup_npi`: is the provider's ID active? (public national registry)
- [ ] **Step 2.2:** Connect an AI model (Claude, with a local model as an option) that decides which tools to call
- [ ] **Step 2.3:** Make it answer in a fixed format: root cause, evidence, fix steps, appeal draft, escalate yes/no
- [ ] **Step 2.4:** Run one denial end to end with a single command

**Done when:** one command takes a denial and returns a structured answer with evidence from at least one tool.

### Phase 3: Evaluation (prove it works)

*Goal: measure accuracy with numbers, not impressions.*

- [ ] **Step 3.1:** Write an answer key of 100 test cases, each with the correct root cause and fix: 60 simple, 20 with several causes, 10 where a tool contradicts the denial, 10 that should be escalated
- [ ] **Step 3.2:** Build a script that runs all 100 and scores them automatically
- [ ] **Step 3.3:** Track the scores: right root cause, complete fix, invented codes (target: zero), right tools used, correct escalations, cost and time per denial
- [ ] **Step 3.4:** Save every run so improvement is visible from version to version

**Done when:** there's a score to quote (e.g., "right root cause on 81 of 100") and a list of failures with reasons.

### Phase 4: Copilot screen (make it usable)

*Goal: a billing person can actually work a queue with it.*

- [ ] **Step 4.1:** Build a simple web screen (Streamlit) listing the denials in a queue
- [ ] **Step 4.2:** Show each AI suggestion with its evidence
- [ ] **Step 4.3:** Add **Approve / Edit / Reject** buttons and a draft appeal letter
- [ ] **Step 4.4:** Save every decision, so the system learns where it's wrong

**Done when:** someone new can work 10 denials without help.

### Phase 5: Analytics and launch (show the bigger picture)

*Goal: show patterns across denials and put the project in front of people.*

- [ ] **Step 5.1:** Write SQL reports: most common denial codes, how many were preventable, trends over time
- [ ] **Step 5.2:** Publish a live demo link
- [ ] **Step 5.3:** Record a 3-minute demo video
- [ ] **Step 5.4:** Write up the results and what was learned

**Done when:** the demo link works, and this README shows the evaluation scores.

More detail on each phase: [`docs/ROADMAP.md`](docs/ROADMAP.md)

## 6. Where the project is today

**Phase 1, steps 1.1–1.4 done.** All 50 scenarios now carry real denial codes, and the general code-16 ones also carry a remark code (RARC) saying exactly what's wrong:

| Status | Scenarios |
|---|---|
| Confirmed against the X12 list or a published payer/CMS source | 46 |
| Best fit, still to confirm | 3 |
| Dropped (pre-existing condition, largely barred under the ACA) | 1 |

**Found while checking:** code 15 (authorization doesn't match) was **deactivated by X12 in 2018**, so RJ-044 was moved to code 296. Checking codes against the live list, not memory, is exactly what the copilot will have to do too.

**Next:** step 1.5, Medicaid-specific scenarios.

## 7. How the repository is organized

```
claims-denial-copilot/
├── README.md              ← you are here: the project plan
├── kb/                    ← the 50 denial scenarios and how each maps to a real code
├── data/reference/        ← carc_mapping.csv: the mapping as data the code will read
├── evals/seed_scenarios/  ← tricky test cases carried over from v1, the start of the answer key
├── docs/
│   ├── ROADMAP.md         ← phase details, tools, how scoring works
│   └── build-log.md       ← what v1 taught and why the project changed direction
└── v1-archive/            ← the original translator: prompts, outputs, scripts, screenshots
```

Folders added as the phases land: `copilot/` (tools and AI engine), `evals/` scoring, `app/` (the screen), `analytics/` (SQL), `scripts/` (data generator).

## 8. Glossary

| Term | Meaning |
|---|---|
| **Claim** | A bill a provider sends to an insurer for a service |
| **Denial** | The insurer refuses to pay all or part of a claim |
| **CARC** | Claim Adjustment Reason Code: the standard code explaining *why* a claim wasn't paid in full (e.g., 197 = prior authorization missing) |
| **RARC** | Remittance Advice Remark Code: an extra code that gives more detail, needed when the CARC is general (like 16) |
| **835** | The standard electronic file insurers send back to providers with payments and denial codes |
| **DOS** | Date of service: the day the patient was treated |
| **Prior authorization** | Approval from the insurer that's required *before* some services |
| **NPI** | National Provider Identifier: a unique ID for every provider in the US |
| **NCCI** | National Correct Coding Initiative: public Medicare rules about which procedure codes can't be billed together |
| **Payer** | The insurer: Medicare, Medicaid, or a commercial plan |
| **Medicaid spend-down** | A Medicaid rule where some people must spend a set amount on medical costs before coverage applies |
| **Eval / answer key** | A set of test cases with known correct answers, used to score the AI |

## 9. How this project started

It began as the [Healthcare Claims Translator](https://github.com/shubhamkumarsingh91-lgtm/healthcare-translator-ai) (v1, April 2026). That version explained claim rejections to patients, providers, and analysts using local AI models. Building it taught the core lessons (grounding, retrieval, testing), and reviewing it honestly showed that billers need the work done, not explained. The full story: [`docs/build-log.md`](docs/build-log.md). The original files: [`v1-archive/`](v1-archive/).

### About the codes

CARC and RARC codes are maintained by [X12](https://x12.org/codes/claim-adjustment-reason-codes). The official descriptions are copyrighted, so this project uses the code numbers with **plain-language summaries in its own words** and links to X12 as the source. CPT procedure descriptions (owned by the AMA) are not reproduced.
