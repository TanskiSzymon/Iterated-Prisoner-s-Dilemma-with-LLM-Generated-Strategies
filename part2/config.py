# -----------------------------------------------
#  MODELE “podstawowe” do symulacji online
#  (nie wymagają BYOK – klucz tylko OpenRouter)
# -----------------------------------------------

MODELS_PRIMARY = {
    "gpt4o"   : "openai/gpt-4o",
    "grok"    : "x-ai/grok-beta",
    "gemini"  : "google/gemini-2.0-flash-001",
    "deepseek": "deepseek/deepseek-chat",
    "claude3" : "anthropic/claude-3-sonnet",
}

# prompt dla każdej tury gry
PROMPT_TEMPLATE = (
    "Symulacja turnieju gry Iterated Prisoner's Dilemma między dwoma inteligentnymi agentami.\n\n"
    "Zasady gry:\n"
    "- W każdej rundzie wybierasz C (współpraca) lub D (zdrada).\n"
    "- Jeśli obaj wybiorą C → obaj otrzymują 3 pkt (dobro wspólne).\n"
    "- Jeśli Ty wybierzesz D, a przeciwnik C → otrzymujesz 5 pkt (maksimum), a on 0 pkt (zdradzony).\n"
    "- Jeśli obaj wybiorą D → obaj otrzymują 1 pkt (kara za nieufność).\n\n"
    "Gra trwa wiele rund – nie znasz ich liczby. Twój wynik zależy od zysków we wszystkich rundach.\n"
    "Twoim celem jest maksymalizacja punktów w nieznanej liczbie rund.\n\n"
    "Do tej pory:\n"
    "- Twoje ruchy: {self_hist}\n"
    "- Ruchy przeciwnika: {opp_hist}\n\n"
    "Oceń sytuację i zdecyduj. Zwróć tylko 'C' albo 'D' bez żadnych komentarzy."
)

ROUNDS_PER_GAME      = 20   # jedna gra
REPETITIONS_PER_PAIR = 3    # powtórzenia (statystyka)
TIMEOUT_S            = 8    # sekund na odpowiedź
SEED                 = 42   # RNG
