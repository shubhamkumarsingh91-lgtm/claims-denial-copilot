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
