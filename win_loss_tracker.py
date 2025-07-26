# win_loss_tracker.py

import pandas as pd
import os
from config import SIGNAL_LOG_CSV_PATH

def calculate_pnl_stats():
    if not os.path.exists(SIGNAL_LOG_CSV_PATH):
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "total_profit": 0.0
        }

    df = pd.read_csv(SIGNAL_LOG_CSV_PATH)

    total_trades = len(df)
    wins = df[df["Result"] == "Win"].shape[0]
    losses = df[df["Result"] == "Loss"].shape[0]
    total_profit = df["Profit"].sum()

    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "total_profit": total_profit
    }
def update_trade_log(symbol, direction, result, sl_hit, tp_hit, pnl, timestamp):
    """
    Logs win/loss results of trades into the win_loss_log.csv.
    """
    import csv
    import os

    log_file = "win_loss_log.csv"

    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Symbol', 'Direction', 'Result', 'SL Hit', 'TP Hit', 'PnL'])

        writer.writerow([timestamp, symbol, direction, result, sl_hit, tp_hit, pnl])
