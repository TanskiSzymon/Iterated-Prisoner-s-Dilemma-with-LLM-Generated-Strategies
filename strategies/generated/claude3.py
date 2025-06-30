from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "claude3-LLM"

    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not self_history:
            return "C"

        if len(self_history) < 5:
            return "C"

        opp_defections = opp_history.count("D")
        self_defections = self_history.count("D")

        if opp_defections > self_defections:
            return "D"
        elif opp_defections < self_defections:
            return "C"
        else:
            if random.random() < 0.5:
                return "C"
            else:
                return "D"

