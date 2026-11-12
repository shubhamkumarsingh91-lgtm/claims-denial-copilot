import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "gemma3:1b",
    "prompt": "Explain: Claim rejected - Member not eligible on date of service",
    "stream": False
}

response = requests.post(url, json=payload)
print(response.json()["response"])

