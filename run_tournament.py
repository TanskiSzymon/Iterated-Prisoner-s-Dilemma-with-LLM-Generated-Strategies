#!/usr/bin/env python3
"""
Round‑robin wszystkich strategii (baseline + wygenerowane).
Każda para gra REPETITIONS_STAGE1 razy.
Wyniki: raw CSV + tabela agregatów + wykres słupkowy.
"""

import random
from pathlib import Path
from itertools import combinations

import pandas as pd

from analysis.metrics   import step_payoff, game_to_frame, aggregate
from analysis.plots     import bar_mean_payoff
from config             import ROUNDS_STAGE1, REPETITIONS_STAGE1, SEED
from strategies         import STRATEGY_REGISTRY     # auto‑load

random.seed(SEED)


from pandas import DataFrame

def pair_table(record_df: DataFrame, out_path: Path):
    """Zapisz tabelę przebiegu konkretnego meczu do pliku CSV i Markdown."""
    p1, p2 = record_df.p1.iloc[0], record_df.p2.iloc[0]
    tbl = DataFrame({
        f"{p1} pkt": record_df.p1_pay,
        f"{p1} ruch": record_df.p1_move.str.lower(),   # małe litery c/w
        f"{p2} ruch": record_df.p2_move.str.lower(),
        f"{p2} pkt":  record_df.p2_pay,
    }, index=range(1, len(record_df)+1))
    tbl.index.name = "runda"

    # wiersz z sumą
    tbl.loc["Suma"] = [
        record_df.p1_pay.sum(), "", "", record_df.p2_pay.sum()
    ]

    # zapis
    stem = f"{p1}__vs__{p2}".replace(" ", "_")
    csv_path  = out_path / f"{stem}.csv"
    md_path   = out_path / f"{stem}.md"
    tbl.to_csv(csv_path, encoding="utf-8-sig")
    tbl.to_markdown(md_path)             


def play_game(p1, p2, rounds: int, rep_id: int):
    rec, h1, h2 = [], [], []
    for r in range(rounds):
        m1 = p1.decide(h1, h2)
        m2 = p2.decide(h2, h1)
        p1_pay, p2_pay = step_payoff(m1, m2)
        rec.append(dict(
            repetition = rep_id,
            round      = r + 1,
            p1         = p1.name, p1_move = m1, p1_pay = p1_pay,
            p2         = p2.name, p2_move = m2, p2_pay = p2_pay
        ))
        h1.append(m1); h2.append(m2)
    return rec

def round_robin(strategies: dict):
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "pair_tables").mkdir(exist_ok=True)
    records = []
    for (name_a, strat_a), (name_b, strat_b) in combinations(strategies.items(), 2):
        for rep in range(1, REPETITIONS_STAGE1 + 1):
            game_rec = play_game(strat_a, strat_b, ROUNDS_STAGE1, rep)
            records += game_rec
            # zapisz tabelę z przebiegiem
            pair_df = DataFrame(game_rec)
            pair_table(pair_df, out_dir / "pair_tables")
    return game_to_frame(records)

def main():
    df = round_robin(STRATEGY_REGISTRY)
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)

    # surowe wyniki
    df.to_csv(out_dir / "stage1_raw.csv", index=False)

    # agregacja po strategii (średnio z 5 powtórzeń)
    summary = aggregate(df)
    summary_display = (
        summary
        .sort_values("mean_payoff", ascending=False)
        .reset_index(drop=True)
        .round({"mean_payoff": 3, "coop_rate": 3, "mean_diff": 3, "std_payoff": 3})
    )
    print("\n=== RANKING (średnia z 5 gier) ===")
    print(summary_display.to_string(index=False))
    summary.to_csv(out_dir / "stage1_summary.csv", index=False)

    # wykres słupkowy
    bar_mean_payoff(summary, out_dir / "stage1_mean_payoff.png")

    # konsola
    print("\n=== SUMMARY (średnia z pięciu prób) ===")
    print(summary.to_string(index=False))

    # pełna tabela –  jedna linia = jedna gra
    pivot = (
        df.groupby(["p1", "p2", "repetition"])
          .agg(p1_total=("p1_pay","sum"),
               p2_total=("p2_pay","sum"))
          .reset_index()
    )
    pivot.to_csv(out_dir / "stage1_games.csv", index=False)

    from tabulate import tabulate    # pip install tabulate
    print("\n=== WYNIKI POJEDYNKÓW (średni wynik z 20 rund) ===")
    print(tabulate(pivot.head(20), headers="keys", tablefmt="pretty"))
    print("\nWygenerowano również plik stage1_games.csv "
          "(wynik każdej z 5 iteracji).")

if __name__ == "__main__":
    main()
