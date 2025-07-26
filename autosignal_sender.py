import time
import pandas as pd
import os

def load_latest_signal_csv(folder="signals"):
    """
    Load the most recent signal CSV file from the given folder.
    """
    try:
        files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        if not files:
            return pd.DataFrame()
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(folder, x)))
        return pd.read_csv(os.path.join(folder, latest_file))
    except Exception as e:
        print(f"[load_latest_signal_csv] Error loading CSV: {e}")
        return pd.DataFrame()

from config import (
    SYMBOLS,
    TIMEFRAME,
    SIGNAL_INTERVAL_SECONDS,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    ENABLE_RETRY_ON_FAILURE,
    MAX_RETRY_ATTEMPTS
)
from technical_analysis import analyze_pair
from telegram_alerts import send_telegram_alert
from trendline_detection import apply_trendline_filter
from smart_money_detection import analyze_smart_money
from support_resistance import is_near_support_or_resistance
from fibonacci import is_fib_retracement_valid
from logger import log_signal_to_csv
from pnl_tracker import update_pnl_stats
from datetime import datetime
from utils import is_bullish_engulfing


def retry_if_enabled(func, *args, **kwargs):
    if not ENABLE_RETRY_ON_FAILURE:
        return func(*args, **kwargs)
    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[Retry Attempt {attempt + 1}] Error: {e}")
            time.sleep(2)
    print("[Max retries reached] Skipping this pair.")
    return None


def generate_signals():
    if not SYMBOLS or not isinstance(SYMBOLS, list):
        print("❌ Error: SYMBOLS is empty, None, or not a list in config.py.")
        return

    print(f"\n[{datetime.now()}] 📡 Starting signal generation for {len(SYMBOLS)} pairs...")

    for symbol in SYMBOLS:
        try:
            print(f"\n🔍 Checking {symbol}...")

            # --- Smart Money Filter
            if not analyze_smart_money(symbol, TIMEFRAME):
                print("❌ No Smart Money setup.")
                continue

            # --- Trendline Filter
            if not apply_trendline_filter(symbol, TIMEFRAME):
                print("❌ Trendline not confirmed.")
                continue

            # --- Support/Resistance Filter
            if not is_near_support_or_resistance(symbol, TIMEFRAME):
                print("❌ No key Support/Resistance nearby.")
                continue

            # --- Fibonacci Zone Filter
            if not is_fib_retracement_valid(symbol, TIMEFRAME):
                print("❌ Fibo zone not valid.")
                continue

            # --- Run Technical Analysis
            ta_signal = retry_if_enabled(analyze_pair, symbol, TIMEFRAME)

            if not ta_signal:
                print(f"⏸️ No valid signal for {symbol}")
                continue

            print(f"✅ Signal found for {symbol}: {ta_signal}")

            # Log signal
            log_signal_to_csv(symbol, ta_signal)

            # Send signal
            send_telegram_alert(ta_signal)

            # Update PnL if signal has all required info
            required_keys = ['direction', 'entry_price', 'exit_price', 'lot_size']
            if all(key in ta_signal for key in required_keys):
                update_pnl_stats(
                    symbol=symbol,
                    direction=ta_signal['direction'],
                    entry_price=ta_signal['entry_price'],
                    exit_price=ta_signal['exit_price'],
                    lot_size=ta_signal['lot_size']
                )

            print(f"✅ Signal sent and logged for {symbol}.")

        except Exception as e:
            print(f"❗ Error on {symbol}: {e}")

    print(f"[{datetime.now()}] ✅ All signals processed.\n")
