import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"


async def generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )

        response.raise_for_status()
        return response.json()["response"]
