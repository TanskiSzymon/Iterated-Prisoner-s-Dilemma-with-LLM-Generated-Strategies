import random
from strategies.base import Strategy

class StrategyLLM(Strategy):
    name = "Gemini_2.5Pro-LLM"

    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        if not opp_history:
            # First round, cooperate
            return "C"

        opponent_last_move = opp_history[-1]
        my_last_move = self_history[-1] if self_history else None

        # Case 1: Opponent defected in the last round
        if opponent_last_move == "D":
            if my_last_move == "D":
                # Both were defecting (mutual defection scenario)
                # Higher chance to try cooperating to break the cycle
                if random.random() < 0.30:  # 30% chance to cooperate
                    return "C"
                else:
                    return "D"  # Continue defecting
            else:
                # Opponent defected, but I cooperated (or it's early and I haven't established a D pattern)
                # Strong retaliation, but with a very small chance of forgiveness
                if random.random() < 0.05:  # 5% chance to forgive by cooperating
                    return "C"
                else:
                    return "D"  # Retaliate
        # Case 2: Opponent cooperated in the last round
        else:  # opponent_last_move == "C"
            # Opponent cooperated, so I should generally cooperate too.
            # Small chance to probe with a defection.
            if random.random() < 0.05:  # 5% chance to defect (probe)
                return "D"
            else:
                return "C"  # Continue cooperating