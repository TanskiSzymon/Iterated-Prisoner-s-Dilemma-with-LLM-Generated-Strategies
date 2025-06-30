import asyncio, random
from pathlib import Path
import pandas as pd

from config            import (
    MODELS_PRIMARY, PROMPT_TEMPLATE, ROUNDS_PER_GAME, REPETITIONS_PER_PAIR,
    TIMEOUT_S, SEED
)
from openrouter_async  import ORClient
from metrics           import step_payoff, aggregate

random.seed(SEED)

async def one_move(client: ORClient, self_hist, opp_hist) -> str:
    prompt = PROMPT_TEMPLATE.format(
        self_hist=" ".join(self_hist) or "<pusta>",
        opp_hist=" ".join(opp_hist) or "<pusta>",
    )
    try:
        resp = await asyncio.wait_for(
            client.chat([{"role":"user","content":prompt}]),
            timeout=TIMEOUT_S
        )
    except asyncio.TimeoutError:
        return "D"
    return "C" if resp and resp.strip().upper().startswith("C") else "D"

async def play_game(tag_a, tag_b, clients, rep_id):
    p1, p2 = clients[tag_a], clients[tag_b]
    h1, h2, rec = [], [], []
    for r in range(ROUNDS_PER_GAME):
        m1, m2 = await asyncio.gather(
            one_move(p1, h1, h2),
            one_move(p2, h2, h1),
        )
        p1_pay, p2_pay = step_payoff(m1, m2)
        rec.append({
            "repetition": rep_id, "round": r+1,
            "p1": tag_a, "p1_move": m1, "p1_pay": p1_pay,
            "p2": tag_b, "p2_move": m2, "p2_pay": p2_pay,
        })
        h1.append(m1); h2.append(m2)
    return rec

async def round_robin() -> pd.DataFrame:
    clients = {tag: ORClient(mid) for tag,mid in MODELS_PRIMARY.items()}
    try:
        records=[]
        tags=list(MODELS_PRIMARY)
        for i, a in enumerate(tags):
            for b in tags[i+1:]:
                for rep in range(1, REPETITIONS_PER_PAIR+1):
                    records += await play_game(a,b,clients,rep)
        return pd.DataFrame(records)
    finally:
        await asyncio.gather(*(c.close() for c in clients.values()))
