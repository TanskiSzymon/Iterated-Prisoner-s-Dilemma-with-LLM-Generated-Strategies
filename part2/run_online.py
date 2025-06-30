#!/usr/bin/env python3
import asyncio
from pathlib import Path
from tabulate import tabulate

from simulation import round_robin
from metrics     import aggregate

RESULT_DIR = Path("results_online")
RESULT_DIR.mkdir(exist_ok=True)

async def main():
    df = await round_robin()
    df.to_csv(RESULT_DIR/"raw.csv", index=False, encoding="utf-8-sig")
    summary = aggregate(df)
    summary.to_csv(RESULT_DIR/"summary.csv", index=False, encoding="utf-8-sig")

    print("\n=== RANKING (średnia) ===")
    print(tabulate(summary, headers="keys", tablefmt="pretty", showindex=False))

if __name__ == "__main__":
    asyncio.run(main())
