# import json
# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "mistral"


# def ask_mistral(prompt: str) -> str:
#     """
#     Calls local Ollama Mistral model and returns raw text response.

#     This function is intentionally kept LLM-agnostic:
#     - No schema enforcement here
#     - No JSON parsing here
#     - Caller decides how to extract / validate output
#     """

#     if not prompt or not prompt.strip():
#         raise ValueError("Empty prompt passed to Mistral")

#     payload = {
#         "model": MODEL_NAME,
#         "prompt": prompt,
#         "stream": False
#     }

#     try:
#         response = requests.post(
#             OLLAMA_URL,
#             headers={"Content-Type": "application/json"},
#             json=payload,
#             timeout=120
#         )
#     except requests.exceptions.ConnectionError:
#         raise RuntimeError(
#             "❌ Cannot connect to Ollama. Is `ollama serve` running?"
#         )
#     except requests.exceptions.Timeout:
#         raise RuntimeError(
#             "❌ Mistral request timed out (120s). Try smaller input."
#         )

#     if response.status_code != 200:
#         raise RuntimeError(
#             f"❌ Ollama error {response.status_code}: {response.text}"
#         )

#     result = response.json()

#     # Defensive checks
#     llm_text = result.get("response")

#     if not llm_text or not isinstance(llm_text, str):
#         raise RuntimeError(
#             f"❌ Invalid LLM response format: {result}"
#         )

#     return llm_text.strip()


import os
import requests
import json

# 1. Set your API Key (Best practice: use environment variables)
# os.environ["GROQ_API_KEY"] = "gsk_..." 4
# put you groq_API_key down below 
GROQ_API_KEY = "your api key"

# 2. Groq API Endpoint
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# 3. CHOOSE A WORKING MODEL (Updated Jan 2026)
# Option A: Best for Extraction (Recommended)
MODEL_NAME = "llama-3.3-70b-versatile" 

# Option B: If you strictly want Mistral (The new supported version)
# MODEL_NAME = "mistral-saba-24b"

def ask_mistral(prompt: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("❌ No GROQ_API_KEY found. Check your .env file.")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            # System prompt helps force JSON mode
            {"role": "system", "content": "You are a helpful API that outputs strict JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,  # Keep it deterministic
        "response_format": {"type": "json_object"} # Force JSON mode (supported by Llama 3.3)
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json=payload,
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"❌ Connection Error: {e}")

    if response.status_code != 200:
        raise RuntimeError(f"❌ API Error {response.status_code}: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]

# --- Test Run ---
if __name__ == "__main__":
    ocr_sample = "Invoice #12345 Date: 2026-01-20 Total: $500.00"
    
    prompt = f"""
    Extract data as JSON.
    Text: {ocr_sample}
    Schema: {{ "invoice_number": string, "total": string }}
    """
    
    print(f"Using Model: {MODEL_NAME}")
    print(ask_groq(prompt))