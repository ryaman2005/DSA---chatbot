import requests
import json

def stream_ollama_response(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "tinyllama", "prompt": prompt, "stream": True},
        stream=True
    )

    for line in response.iter_lines():
        if line:
            try:
                chunk = json.loads(line.decode("utf-8"))
                if "response" in chunk:
                    yield chunk["response"]
            except json.JSONDecodeError:
                continue
