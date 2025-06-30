import os
import re
from openai import OpenAI

class OpenRouterClient:
    """Minimalny wrapper na OpenRouter API – tylko chat.completions."""
    def __init__(self, model: str):
        self._model  = model
        self._client = OpenAI(
            base_url = "https://openrouter.ai/api/v1",
            api_key  = os.getenv("OPENROUTER_API_KEY")
        )
        if not self._client.api_key:
            raise RuntimeError("Brak zmiennej środowiskowej OPENROUTER_API_KEY")

    def chat(self, system: str, user: str,
             temperature: float = 0.0,
             max_tokens: int = 1024) -> str:
        resp = self._client.chat.completions.create(
            model       = self._model,
            temperature = temperature,
            max_tokens  = max_tokens,
            messages    = [
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ]
        )
        return resp.choices[0].message.content

# --------------------------------------------------
_CODE_BLOCK_RE = re.compile(r"```(?:python)?(.*?)```", re.S)

def extract_code(text: str) -> str:
    """
    Usuwa markdown i zwraca czysty kod. Jeśli nie ma ``` ``` –
    zwraca oryginał.
    """
    match = _CODE_BLOCK_RE.search(text)
    return match.group(1).strip() if match else text.strip()
