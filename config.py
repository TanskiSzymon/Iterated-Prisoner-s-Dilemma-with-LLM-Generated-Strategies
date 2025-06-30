# Konfiguracja globalna projektu
MODELS_PRIMARY = {
    "gpt4o"   : "openai/o3",
    "grok3"   : "x-ai/grok-3-beta",       
    "gemini"  : "google/gemini-2.0-flash-001", 
    "deepseek": "deepseek/deepseek-r1:free",
    "claude3" : "anthropic/claude-3-sonnet"
}

PROMPT_SYSTEM = (
    "You are a top-tier game-theory expert and senior Python developer. "
    "Return only valid Python 3.13 code."
)
# patrz generate_strategies.py
ROUNDS_STAGE1      = 20  # liczba rund w jednej grze
REPETITIONS_STAGE1 = 10    # ile razy ta sama para gra od nowa
SEED               = 42


"""
MODELS_PRIMARY = {
    "gpt4o"   : "openai/gpt-4o-mini",
    "grok3"   : "x-ai/grok-3-beta",       
    "gemini"  : "google/gemini-2.0-flash-001", 
    "deepseek": "deepseek/deepseek-chat",
    "claude3" : "anthropic/claude-3-sonnet"
}"""