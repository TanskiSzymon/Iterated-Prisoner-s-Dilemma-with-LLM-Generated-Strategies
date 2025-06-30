from .base import Strategy

class TitForTat(Strategy):
    name = "Tit‑for‑Tat"
    def decide(self, self_history, opp_history) -> str:
        return "C" if not opp_history or opp_history[-1] == "C" else "D"

class GrimTrigger(Strategy):
    name = "Grim Trigger"
    def decide(self, self_history, opp_history) -> str:
        if "D" in opp_history:
            return "D"
        return "C"
