from strategies.base import Strategy
import random

class StrategyLLM(Strategy):
    name = "DeepSeek_R1-LLM"


    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not opp_history:
           return 'C'
        if opp_history[-1] == 'D':
            return 'D' if random.random() < 0.9 else 'C'
        return 'C'