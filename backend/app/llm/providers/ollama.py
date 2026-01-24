import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

class OllamaProvider:
    def __init__(self, model: str = "mistral"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()