from app.llm.providers.ollama import generate as ollama_generate

class LLMClient:
    def __init__(self, provider: str = "ollama"):
        self.provider = provider

    async def generate(self, prompt: str) -> str:
        if self.provider == "ollama":
            return await ollama_generate(prompt)

        raise ValueError(f"Unsupported LLM provider: {self.provider}")
