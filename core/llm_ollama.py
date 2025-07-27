# core/llm_ollama.py

import requests

# Default model
MODEL_NAME = "mistral"

def set_model_name(name: str):
    global MODEL_NAME
    MODEL_NAME = name

def query_local_llm(prompt: str) -> str:
    try:
        url = "http://localhost:11434/api/generate"
        response = requests.post(url, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"[Ollama API Error] {response.text}"
    except Exception as e:
        return f"[System Error] {str(e)}"
