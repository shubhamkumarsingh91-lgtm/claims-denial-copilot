# v1 archive: Healthcare Claims Translator (April 2026)

> **Disclaimer:** independent personal project. No PHI, no PII, and no Medicaid, agency, or other non-public data is used. Only public reference information and synthetic (invented) examples. See the full disclaimer in the [README](../README.md#disclaimer).

This folder keeps the work from version 1 of this project, originally in [healthcare-translator-ai](https://github.com/shubhamkumarsingh91-lgtm/healthcare-translator-ai). It's kept for history and as a **baseline**: the v2 eval harness will compare against these results.

v1 explained claim rejections to three personas (patient, provider, analyst) using local models (Ollama with Qwen3 4B / Gemma 3 1B) and a RAG knowledge base in Open WebUI. The story of what it taught and why v2 changed direction is in [`docs/build-log.md`](../docs/build-log.md).

| Folder | What's in it |
|---|---|
| `prompts/` | The three persona system prompts used in Open WebUI. In the source PDF, the last words of the analyst prompt's first line are cut off; they were completed as "provided knowledge." |
| `outputs/` | Model outputs from v1 test runs: week 1 single-line tests, week 2 persona tests, multi-step prompts, advanced scenarios with the eligibility tool. Graded by eye, not scored. |
| `scripts/` | `ollama_test.py` (first local model call) and `run_tests.py` (runs the multi-step prompts through all three personas). |
| `screenshots/` | Open WebUI runs of four advanced scenarios: tool conflict, member not found, two rejection reasons, authorization plus provider mismatch. |

These files are not used by the v2 copilot.
