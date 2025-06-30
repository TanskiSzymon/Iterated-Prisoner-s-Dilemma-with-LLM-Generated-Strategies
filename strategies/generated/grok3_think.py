from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "grok3_Think-LLM"
    
    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not opp_history:
            return "C"
        last_opp_move = opp_history[-1]
        if last_opp_move == "C":
            return "C"
        else:
            if random.random() < 0.1:
                return "C"
            else:
                return "D"