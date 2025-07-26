# pnl_tracker.py

import os
import csv
from datetime import datetime, timedelta
import config

PNL_FILE = "pnl_log.csv"

def initialize_pnl_file():
    if not os.path.exists(PNL_FILE):
        with open(PNL_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Symbol", "Direction", "Entry", "Exit", "Profit($)", "Result"])

def update_pnl_stats(symbol, direction, entry_price, exit_price, lot_size):
    initialize_pnl_file()
    
    pip_value = 10 if symbol.endswith("JPY") else 1
    profit = (exit_price - entry_price) if direction == "buy" else (entry_price - exit_price)
    dollar_profit = round(profit * pip_value * (lot_size * 10), 2)

    result = "Win" if dollar_profit > 0 else "Loss" if dollar_profit < 0 else "Break-even"

    with open(PNL_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol, direction, entry_price, exit_price, dollar_profit, result
        ])
    
    print(f"[PnL Tracker] {symbol} | {direction.upper()} | Profit: ${dollar_profit} | {result}")
    return dollar_profit, result


def get_weekly_summary():
    initialize_pnl_file()
    total_pnl = 0
    wins = 0
    losses = 0
    with open(PNL_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                date = datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S")
                if datetime.now() - date <= timedelta(days=7):
                    pnl = float(row["Profit($)"])
                    total_pnl += pnl
                    if pnl > 0:
                        wins += 1
                    elif pnl < 0:
                        losses += 1
            except:
                continue
    return {
        "total_pnl": round(total_pnl, 2),
        "wins": wins,
        "losses": losses,
        "net_result": "Profit" if total_pnl > 0 else "Loss" if total_pnl < 0 else "Neutral"
    }
