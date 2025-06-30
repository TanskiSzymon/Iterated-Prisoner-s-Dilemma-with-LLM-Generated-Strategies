from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "gpt4o-LLM"

    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not opp_history:
            return "C"
        if opp_history[-1] == "D":
            return "D"
        return "C"
