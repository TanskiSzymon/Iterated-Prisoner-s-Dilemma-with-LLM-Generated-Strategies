class Strategy:
    """Interfejs bazowy. Wszystkie strategie muszą go implementować."""
    name: str = "BaseStrategy"

    def decide(self,
               self_history: list[str],
               opp_history:  list[str]) -> str:
        raise NotImplementedError
