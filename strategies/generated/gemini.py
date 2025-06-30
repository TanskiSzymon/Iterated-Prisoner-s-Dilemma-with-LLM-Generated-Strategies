import random
from strategies.base import Strategy

class StrategyLLM(Strategy):
    name = "gemini-LLM"

    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not self_history:
            return "C"
        else:
            if opp_history[-1] == "D":
                return "D"
            else:
                return "C"
