# Build log

## v1: Healthcare Claims & EDI Translator (Apr 2026)

Repo: [healthcare-translator-ai](https://github.com/shubhamkumarsingh91-lgtm/healthcare-translator-ai)

**Idea:** translate claim rejection messages into three explanations (patient, provider billing staff, analyst), grounded in a local knowledge base. Public documentation and synthetic examples only.

**Stack:** Ollama (Qwen3 4B, Gemma 3 1B), Open WebUI for chat, knowledge base and persona models, Docling for PDF-to-Markdown parsing, Docker, Python, GitHub.

**What I learned building it**

| Problem I hit | What it taught me | How I fixed it |
|---|---|---|
| A plain model call gave a wrong definition of the EDI 837 | Small models hallucinate without grounding | Added RAG with a knowledge base |
| RAG returned short or wrong answers, e.g. a title-only chunk for "What is EDI 837?" | Retrieval quality depends on document structure, not just the model | Rewrote knowledge as clean, self-contained Markdown designed around the target questions |
| Raw PDFs parsed poorly in Open WebUI | Parsing is its own pipeline step | Added Docling: PDF → Markdown → knowledge base |
| `pip install` failed with "externally-managed-environment" on macOS | System Python shouldn't be modified | Used a virtual environment (`python3 -m venv .venv`) |
| GitHub rejected password pushes; later the push was rejected because the remote had new commits | How Git authentication and history work | Set up SSH keys; used `git pull --rebase` before pushing |
| Outputs drifted off format | Prompts need explicit structure and an "I don't know" rule | Wrote per-persona system prompts with fixed formats and grounding rules |

**What v1 also showed:** I added an eligibility tool and multi-issue test scenarios. One test exposed a reasoning gap: the model treated "member is active today" as proof the denial was wrong, when what matters is coverage **on the date of service**.

## Why the project changed direction (Nov 2026)

Reviewing v1 honestly:

- **Explaining a claim isn't worth much on its own.** Patients want to know what they owe, billers already know what the codes mean, and analysts have the data. What billers lack is time.
- **The codes were invented** (ELG-001 and so on). Real denials carry CARC/RARC codes on the 835 remittance.
- **Some scenarios were commercial-only** (waiting periods, pre-existing conditions) in a project meant to show Medicaid depth.
- **The system lived inside Open WebUI**, so nobody could clone the repo and reproduce the results.
- **Results were graded by eye**, with no answer key and no score.

So v2 is a **copilot**: it does the root-cause digging and drafts the fix, with a human approving each one. It has a payer-agnostic core with a Medicaid specialty layer, everything lives in code, and every version is scored against an answer key.

## v2 progress

| Date | What changed |
|---|---|
| 2026-11-11 | New repo. All 50 scenarios mapped to real CARCs (38 confirmed, 4 to verify, 7 need a RARC, 1 dropped). Payer scope tagged per scenario. |
| 2026-11-11 | Brought over the v1 prompts, outputs, scripts and screenshots into `v1-archive/`. README rewritten as a step-by-step project plan. |
| 2026-11-11 | Step 1.4: remark codes added for the 7 code-16 scenarios; 4 "verify" rows checked. Found CARC 15 deactivated (2018), RJ-044 moved to 296. Now 46 confirmed, 3 verify, 1 dropped. Each row links its source. |
| 2026-11-21 | Phase 2 pulled forward: built the date-of-service check (eligibility on the DOS, coverage on the DOS, timely filing, plan-change and retro-eligibility notes) and the prior auth matcher (missing, code, date window, units, provider; reports every failure). Plain Python rules, no AI. 20 synthetic cases with hand-written answers; 43 tests compare the full output and reject any code not in the mapping. Tests were deliberately broken once to prove they fail. |
| 2026-11-21 | Step 1.5: 8 Medicaid scenarios (RJ-051 to RJ-058) in `kb/medicaid.md`: spend-down 178, patient liability 142, timely filing 29, retro eligibility 26, TPL 22 + MA04, managed care vs. FFS 24, revalidation B7, non-rebatable drug 211. All codes confirmed active on the X12 lists. Now 54 confirmed, 3 verify, 1 dropped. Added `tests/test_mapping.py`, which cross-checks every scenario's code, remark code, scope and status across the KB files, the CSV and the mapping table (161 tests total). |
| 2026-11-21 | Steps 1.6 and 1.7, Phase 1 done. `scripts/generate_denials.py` builds 200 synthetic denials (seeded, reproducible) across all 57 active scenarios, with members, eligibility, other coverage, providers, coverage rules and authorizations written so the facts cause each denial. 71 denials are checkable today; a test runs the real checks on every one and confirms exactly the planted cause is found. `docs/PRD.md`: target user (billers at small Medicaid-heavy providers), v1 scope, metrics, risks. 238 tests pass. |
| 2026-11-22 | Phase 2: two more checks. Other-insurance check (`tpl_check.py`, code 22): Medicaid treats any active other coverage as paying first; a $0 primary payment still counts as payment info; estimates Medicaid's payment with exact decimals (lesser-of method, never below $0). Billed-payer check (`payer_check.py`, code 24): managed care member billed fee-for-service; other wrong-plan cases get a note, not an invented code. 16 hand-written cases. Generator: RJ-009/055/056 now checkable (80 of 200), new `plans.csv`. New test: on every checkable denial, the other three checks must find nothing. 359 tests pass; 3 deliberate breaks were each caught. |
| 2026-11-22 | New scenario RJ-059, claim sent to the wrong payer (code 109, confirmed active on X12), in `kb/eligibility.md`. The billed-payer check now flags every wrong payer instead of leaving a note: code 24 only when fee-for-service Medicaid was billed for a managed care member, 109 for every other wrong plan. Also fixed my own rule: a managed care member billed to a commercial plan had been getting 24, but only fee-for-service Medicaid sends 24. 4 new or updated hand-written cases; RJ-059 is checkable in the generated data. 365 tests pass; 2 deliberate breaks were each caught. |
| 2026-11-22 | Provider eligibility check (`provider_check.py`): NPI not on file (208, RJ-029), excluded (B7, RJ-033), never enrolled (RJ-035), before credentialing (RJ-030), enrollment ended / revalidation (RJ-057), license expired (RJ-028). Exclusion means write off, never resubmit. Fixed the generator: all five B7 scenarios had been given the same "enrollment ended" fact, which was only true for RJ-057; each now gets its own provider with the one fact that causes it. 12 hand-written cases; 98 of 200 generated denials now checkable (24 of 58 scenarios). 425 tests pass; 3 deliberate breaks were each caught. |
