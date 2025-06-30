import os, asyncio, json, aiohttp
from typing import Any

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

class ORClient:
    """Minimalny async klient OpenRouter (tylko chat.completions)."""
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.session: aiohttp.ClientSession | None = None
        self.api_key  = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("Brak zmiennej OPENROUTER_API_KEY")

    async def _post(self, payload: dict[str, Any]) -> dict:
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}",
                         "Content-Type": "application/json"}
            )
        async with self.session.post(
            f"{OPENROUTER_BASE}/chat/completions",
            json=payload, timeout=30
        ) as resp:
            return await resp.json()

    async def chat(self, messages: list[dict], **kw) -> str | None:
        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0,
            "max_tokens": 1,
            **kw
        }
        data = await self._post(payload)
        # jeśli błąd -> zwróć None
        if "choices" not in data:
            print("⚠️  OpenRouter error:", data.get("error", data))
            return None
        return data["choices"][0]["message"]["content"].strip()

    async def close(self):
        if self.session:
            await self.session.close()
