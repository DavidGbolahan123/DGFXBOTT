import os
import csv
import json
from datetime import datetime, timedelta
import config
from telegram_bot import send_telegram_message as send_telegram_alert
from pnl_tracker import update_pnl_stats

# Create logs folder if not exists
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# Define log file paths
SIGNAL_LOG_PATH = os.path.join(LOG_FOLDER, "signals_log.csv")
WEEKLY_SUMMARY_PATH = os.path.join(LOG_FOLDER, "weekly_summary.csv")

# Header for signal log
SIGNAL_LOG_HEADER = [
    "timestamp", "pair", "action", "confidence", "rsi", "trend", 
    "entry", "sl", "tp", "volume", "win_rate", "ai_score"
]

# --- 1. Function to log signals to CSV ---
def log_signal_to_csv(signal_data: dict):
    file_exists = os.path.isfile(SIGNAL_LOG_PATH)

    with open(SIGNAL_LOG_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=SIGNAL_LOG_HEADER)
        if not file_exists:
            writer.writeheader()
        writer.writerow(signal_data)

    print(f"[+] Signal logged for {signal_data['pair']} at {signal_data['timestamp']}")

    # Also update the PnL tracker if TP/SL already hit
    update_pnl_stats(signal_data)

    # Optional: Send Telegram alert
    message = f"""📊 *NEW SIGNAL ALERT*
---------------------
📌 *Pair:* {signal_data['pair']}
🕒 *Time:* {signal_data['timestamp']}
📈 *Action:* {signal_data['action'].upper()}
💡 *Trend:* {signal_data['trend']}
📊 *RSI:* {signal_data['rsi']}
⚙️ *Confidence:* {signal_data['confidence']}%
🎯 *Entry:* {signal_data['entry']}
🛑 *SL:* {signal_data['sl']}
🎯 *TP:* {signal_data['tp']}
🧠 *AI Score:* {signal_data['ai_score']}%
📚 *Win Rate:* {signal_data['win_rate']}%
"""
    try:
        send_telegram_alert(config.TELEGRAM_CHAT_ID, message)
    except Exception as e:
        print(f"[x] Telegram alert failed: {e}")

# --- 2. Function to generate weekly summary ---
def generate_weekly_summary():
    summary = []
    if not os.path.exists(SIGNAL_LOG_PATH):
        print("[!] No signals to summarize.")
        return

    week_ago = datetime.now() - timedelta(days=7)

    with open(SIGNAL_LOG_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_time = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            if row_time > week_ago:
                summary.append(row)

    if not summary:
        print("[!] No signals in the past 7 days.")
        return

    with open(WEEKLY_SUMMARY_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=SIGNAL_LOG_HEADER)
        writer.writeheader()
        for row in summary:
            writer.writerow(row)

    print("[✓] Weekly summary CSV generated.")

    try:
        send_telegram_alert(config.TELEGRAM_CHAT_ID, "📬 Weekly summary CSV generated successfully.")
    except Exception as e:
        print(f"[x] Telegram summary alert failed: {e}")
