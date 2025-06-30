from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "claude3_opus-LLM"
    
    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if len(opp_history) == 0:
            return random.choice(["C", "D"])
        if opp_history[-1] == "D":
            return "D"
        num_rounds = len(self_history)
        if num_rounds < 5:
            return "C"
        recent_self = self_history[-5:]
        recent_opp = opp_history[-5:]
        if recent_opp.count("D") > 1:
            return "D"
        if recent_self.count("C") > 3:
            return "D"
        return "C"