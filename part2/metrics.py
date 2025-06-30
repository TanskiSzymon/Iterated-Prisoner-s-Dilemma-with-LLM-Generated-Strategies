import numpy as np
import pandas as pd

PAYOFF = {("C","C"):(3,3), ("C","D"):(0,5), ("D","C"):(5,0), ("D","D"):(1,1)}

def step_payoff(a:str,b:str) -> tuple[int,int]:
    return PAYOFF[(a,b)]

def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    out=[]
    for strat in sorted(set(df.p1)|set(df.p2)):
        rows=df[(df.p1==strat)|(df.p2==strat)]
        pay=np.where(rows.p1==strat, rows.p1_pay, rows.p2_pay)
        opp=np.where(rows.p1==strat, rows.p2_pay, rows.p1_pay)
        out.append({
            "strategy": strat,
            "mean_payoff": pay.mean(),
            "coop_rate": ((rows.p1==strat)&(rows.p1_move=="C")|
                          (rows.p2==strat)&(rows.p2_move=="C")).mean(),
            "mean_diff": (pay-opp).mean(),
            "std_payoff": pay.std(ddof=1)
        })
    return pd.DataFrame(out).sort_values("mean_payoff",ascending=False)
