from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "grok3-LLM"
    
    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not opp_history:
            return "C"
        if opp_history[-1] == "D":
            return "D"
        if len(opp_history) > 1 and opp_history[-2] == "D":
            return "D"
        return "C"
