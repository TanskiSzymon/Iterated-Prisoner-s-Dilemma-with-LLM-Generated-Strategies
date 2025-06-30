#!/usr/bin/env python
"""
Pobiera od LLM-ów kod strategii, zapisuje do strategies/generated/{model}.py
"""
from pathlib import Path
from openrouter_client import OpenRouterClient, extract_code
from config            import MODELS_PRIMARY, PROMPT_SYSTEM

GENERATED_DIR = Path(__file__).parent / "strategies" / "generated"
GENERATED_DIR.mkdir(exist_ok=True, parents=True)
(GENERATED_DIR / "__init__.py").touch(exist_ok=True)
PROMPT_USER = """
Napisz wyłącznie kod Python 3.11 jednej klasy strategii.

Wymagania - ważne:
1. Dodaj linię:  from strategies.base import Strategy
2. Zdefiniuj klasę  StrategyLLM(Strategy):
3. Atrybut  `name = "{tag}-LLM"`
4. Metoda  decide(self, self_history: list[str], opp_history: list[str]) -> str
   musi zwracać dokładnie "C" albo "D".
5. Brak importów poza  random  i w/w Strategy.
6. Zacznij od współpracy, liczba rund nieznana, strategia odporna.
Zwróć tylko kod (bez markdown, komentarzy, wyjaśnień).
"""

def main():
    for tag, model_name in MODELS_PRIMARY.items():
        PROMPT_USER2 = PROMPT_USER.format(tag=tag)
        client = OpenRouterClient(model_name)
        print(f"↻  Generuję strategię dla {tag}...")
        raw  = client.chat(system=PROMPT_SYSTEM, user=PROMPT_USER2,
                           temperature=0.2, max_tokens=512)
        code = extract_code(raw)
        out  = GENERATED_DIR / f"{tag}.py"
        out.write_text(code, encoding="utf-8")
        print(f"✔  Zapisano {out}")

if __name__ == "__main__":
    main()


