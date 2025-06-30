import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def bar_mean_payoff(table: pd.DataFrame, out: Path):
    plt.figure()
    plt.bar(table.strategy, table.mean_payoff)
    plt.ylabel("Średni zysk / rundę")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out.parent.mkdir(exist_ok=True)
    plt.savefig(out)
    plt.close()
