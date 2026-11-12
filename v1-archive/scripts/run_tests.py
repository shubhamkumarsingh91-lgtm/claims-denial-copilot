import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "hf.co/unsloth/Qwen3-4B-GGUF:Q4_K_M"  # change if needed


PATIENT_PROMPT = """
You are a healthcare assistant explaining claim rejections to patients.

Use simple language.

Format:
1. What happened
2. What it means for you
3. What you should do next
"""

PROVIDER_PROMPT = """
You are a healthcare claims assistant for providers.

Format:
1. Likely cause
2. What to verify
3. Next action
"""

ANALYST_PROMPT = """
You are a healthcare claims analyst.

Format:
1. Interpretation
2. Likely issue area
3. Technical notes
4. Next debugging step
"""


def clean_output(text):
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    return text.strip()


def run_prompt(system_prompt, user_prompt):
    full_prompt = f"{system_prompt}\n\nUser Input:\n{user_prompt}"

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": full_prompt,
            "stream": False
        },
        timeout=180
    )

    data = response.json()

    if "response" not in data:
        print("ERROR:", data)
        return ""

    return clean_output(data["response"])


def main():
    os.makedirs("outputs", exist_ok=True)

    with open("tests/multi_step_prompts.md", "r") as f:
        prompts = f.read().split("\n\n")

    with open("outputs/multi_step_results.md", "w") as out:
        for i, prompt in enumerate(prompts, start=1):
            if not prompt.strip():
                continue

            print(f"Running Test {i}...")

            patient_output = run_prompt(PATIENT_PROMPT, prompt)
            provider_output = run_prompt(PROVIDER_PROMPT, prompt)
            analyst_output = run_prompt(ANALYST_PROMPT, prompt)

            out.write(f"## TEST {i}\n")
            out.write(f"PROMPT:\n{prompt}\n\n")

            out.write("### Patient Output\n")
            out.write(patient_output + "\n\n")

            out.write("### Provider Output\n")
            out.write(provider_output + "\n\n")

            out.write("### Analyst Output\n")
            out.write(analyst_output + "\n\n")

            out.write("---\n\n")

    print("Done. Results saved in outputs/multi_step_results.md")


if __name__ == "__main__":
    main()
