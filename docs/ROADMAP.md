# Roadmap

Pace: about 7 hours a week (short weekday sessions for learning and small fixes, weekend blocks for building). Estimated total: 12–13 weeks.

## Phase 1: Foundation (1–2 weeks)

- Map every scenario to a real CARC (done) and add RARCs for the CARC-16 rows
- Tag scenarios by payer scope (all payers vs. commercial-only) and add a Medicaid layer: spend-down, retro eligibility, timely filing, TPL / coordination of benefits, provider enrollment and revalidation
- Synthetic data generator: members, eligibility spans, authorizations, providers, denials (stored in DuckDB)
- One-page PRD: user, problem, v1 scope, success metric, failure modes

## Phase 2: Tools + engine (3–4 weeks)

Five tools, all against synthetic data except the public NPI registry:

| Tool | What it answers |
|---|---|
| `check_eligibility(member_id, date_of_service)` | Was the member covered **on that date** (not today)? |
| `lookup_carc(code)` | What category and group does this denial code fall into? |
| `check_auth(auth_id, procedure_code, npi, date_of_service)` | Which auth fields match and which don't? |
| `check_ncci(code_a, code_b)` | Is this code pair blocked by a CMS NCCI edit? |
| `lookup_npi(npi)` | Is this NPI active, and what's its taxonomy? (NPPES public API) |

The engine is an LLM that calls these tools and returns structured JSON: root cause, evidence, fix steps, appeal draft, escalate flag.

## Phase 3: Evaluation (3 weeks)

A 100-case answer key (`evals/golden_set.csv`) written from domain knowledge:

- 60 single-cause denials, 20 multi-cause, 10 where a tool contradicts the denial, 10 that should be escalated
- Scored on: root-cause accuracy, fix completeness, invented-code rate (target 0), correct tool use, escalation accuracy, cost and time per denial
- Every run saved in `evals/results/` so improvement is visible version to version

## Phase 4: Copilot UI (2 weeks)

Streamlit work queue: the denial list, the AI suggestion with its evidence, Approve / Edit / Reject buttons, an appeal draft, and a log of each decision.

## Phase 5: Analytics + ship (2 weeks)

SQL denial-trend dashboard (top CARCs, preventable share, trends), a public demo link, a 3-minute video, and a write-up.

## Open decisions

- Main engine: Claude API (reliable tool use) vs. local Ollama (no API cost). Current plan: Claude as default, Ollama as a switch, and compare both in the eval results.
