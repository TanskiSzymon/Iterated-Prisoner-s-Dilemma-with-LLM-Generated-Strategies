# Iterated Prisoner's Dilemma with LLM-Generated Strategies

**Project Author**: Szymon Tański  
**Course**: Decision Support Algorithms  
**Language Models Used**: GPT-4o, Gemini, Claude, Grok, DeepSeek, and their premium variants  
**Prompted With**: Python code generation for strategy implementation

---

## Project Overview

This project investigates whether Large Language Models (LLMs) can autonomously generate effective strategies for the *Iterated Prisoner's Dilemma* (IPD), especially under the assumption of unknown game length. The aim was to compare LLM-derived strategies with classical baselines like **Tit-for-Tat (TFT)** and **Grim Trigger (GT)**, both in **offline** simulations and **online** execution via real API calls.

---

## Research Objectives

- Evaluate if LLMs can generate executable, robust IPD strategies in Python.
- Measure their effectiveness (payoff) compared to human-designed strategies.
- Analyze cooperation tendencies and stability across different LLMs.
- Compare baseline vs. "thinking"/reflective LLM variants.

---

## Game Setup

The game uses the standard Prisoner's Dilemma payoff matrix:

| Player A \ Player B | Cooperate (C) | Defect (D) |
|---------------------|---------------|------------|
| **Cooperate (C)**   | A: 3 / B: 3   | A: 0 / B: 5|
| **Defect (D)**      | A: 5 / B: 0   | A: 1 / B: 1|

Properties:
- Temptation \( T = 5 \)
- Reward \( R = 3 \)
- Punishment \( P = 1 \)
- Sucker’s payoff \( S = 0 \)

Classic IPD conditions: \( T > R > P > S \), \( 2R > T + S \)

---

## Evaluation Metrics

Each strategy was assessed using:

- **Mean Payoff**: Average points earned per round.
- **Cooperation Rate**: Frequency of choosing to cooperate (C).
- **Mean Difference**: Average score difference vs. opponents.
- **Std. Deviation of Payoff**: Variability across games.

---

## Experimental Design

### Offline Simulations

- Run locally, no API cost.
- Rounds tested: **50, 100, 500, 1000, 10,000**
- Each pair of strategies was repeated 10 times.

### Online API Tournament

- Executed via [OpenRouter](https://openrouter.ai/)
- 20 rounds × 3 repetitions per LLM pair
- Total: **1200 API calls**
- Only top strategies evaluated due to cost

---

## Strategy Types

### Classical Baselines:
- **Tit-for-Tat (TFT)**: Start with cooperation, mirror opponent.
- **Grim Trigger (GT)**: Cooperate until betrayed, then always defect.

### LLM-Generated:
- **Basic LLMs**: E.g., GPT-4o, Gemini, Grok3, DeepSeek, Claude
- **“Thinking” LLMs**: With enhanced reasoning prompts – e.g., o3-LLM, Grok3-Think, DeepSeek-R1, Gemini-2.5-Pro

All LLMs were prompted to return a Python class:
```python
from strategies.base import Strategy

class StrategyLLM(Strategy):
    name = "LLM-Tag"
    def decide(self, self_history: list[str], opp_history: list[str]) -> str:
        # Return "C" or "D"
```
Results Summary
Best Performing Strategies (Offline)
Strategy	Consistent High Payoff
o3-LLM	Highest overall
Grok3_Think	High cooperation + adaptability
DeepSeek_R1	Balanced and reflective

⚠Less Effective Strategies
Strategy	Observed Behavior
claude3_opus-LLM	Chaotic, aggressive
DeepSeek-LLM	Low cooperation, unstable

Performance Over Time
Graph Placeholder
Insert here the following plot (e.g. matplotlib/seaborn):

![plot](https://github.com/user-attachments/assets/0a90d4e8-112c-4aa3-844d-7d8ad1f54529)
Mean Payoff vs. Number of Rounds for All Strategies (Offline Simulations)

```csharp
Online Tournament Results
Strategy	Mean Payoff 	Cooperation Rate
Gemini	    3.000			1.000
Claude3	     2.988			1.000
GPT-4o	     2.988			0.971
Grok	     2.829			0.921
DeepSeek	2.804			0.892
```

These results indicate that prompt formulation may significantly bias strategies toward cooperation.

Key Findings
LLMs can autonomously generate functional IPD strategies.

Thinking variants (e.g. o3-LLM) outperform basic models in long-term simulations.

Trust-based cooperation yields best results in longer games.

Prompt engineering significantly affects strategic behavior.

Classical strategies like Tit-for-Tat remain strong but are now often outclassed.

Project Structure
```csharp
├── strategies/
│   ├── base.py
│   ├── gpt4o_strategy.py
│   ├── gemini_strategy.py
│   └── ...
├── results/
│   ├── offline_metrics.csv
│   ├── online_metrics.csv
├── plots/
│   └── mean_payoff_vs_rounds.png
├── notebooks/
│   └── analysis.ipynb
├── README.md
└── report.pdf
```

How to Reproduce
```python
#Clone the repository:
git clone https://github.com/your_username/ipd-llm-strategies.git
cd ipd-llm-strategies

#(Optional) Set up a virtual environment:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#Run simulation:
python simulate_tournament.py

#Generate plots:
python plot_metrics.py
```
References
Axelrod, R. (1984). The Evolution of Cooperation.
Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
Aquino et al. (2025). From RAG to Multi-Agent Systems: A Survey of Modern Approaches in LLM Development.

License
MIT License. See LICENSE for details.

Contact
For questions or collaboration opportunities, feel free to open an issue or contact me at:
szymontanski8@gmail.com
