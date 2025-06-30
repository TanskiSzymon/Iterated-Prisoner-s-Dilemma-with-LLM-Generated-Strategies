from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "o3-LLM"

    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not opp_history:
            return "C"
        if opp_history[-1] == "C":
            return "C"
        return "C" if random.random() < 0.25 else "D"