import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from config import (
    SYMBOLS_TO_MONITOR,
    BACKTEST_START_DATE,
    BACKTEST_END_DATE,
    LOT_SIZE,
    STOP_LOSS_USD,
    TAKE_PROFIT_USD,
    STRATEGY_SUPPORT_RESISTANCE,
    STRATEGY_FIBONACCI,
    STRATEGY_CANDLE_PATTERNS,
    STRATEGY_SMART_MONEY,
    STRATEGY_TRENDLINE,
    STRATEGY_RSI,
    STRATEGY_MACD,
    STRATEGY_EMA,
    STRATEGY_VOLUME_FILTER,
    MIN_RR_RATIO
)
from utils.signal_utils import generate_signal_from_ohlc

def backtest_symbol(symbol):
    print(f"\n[Backtest] Starting backtest for {symbol}...")

    if not mt5.initialize():
        print("[MT5] Initialization failed.")
        return

    rates = mt5.copy_rates_range(
        symbol,
        mt5.TIMEFRAME_H1,
        datetime.strptime(BACKTEST_START_DATE, "%Y-%m-%d"),
        datetime.strptime(BACKTEST_END_DATE, "%Y-%m-%d")
    )

    if rates is None or len(rates) == 0:
        print(f"[MT5] No historical data found for {symbol}")
        return

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    total_trades = 0
    wins = 0
    losses = 0
    pnl = 0.0

    for i in range(100, len(df)):
        ohlc_data = df.iloc[i-100:i]  # Use 100 bars for signal context

        signal = generate_signal_from_ohlc(
            ohlc_data,
            symbol=symbol,
            apply_sr=STRATEGY_SUPPORT_RESISTANCE,
            apply_fib=STRATEGY_FIBONACCI,
            apply_candle=STRATEGY_CANDLE_PATTERNS,
            apply_smart_money=STRATEGY_SMART_MONEY,
            apply_trendline=STRATEGY_TRENDLINE,
            apply_rsi=STRATEGY_RSI,
            apply_macd=STRATEGY_MACD,
            apply_ema=STRATEGY_EMA,
            volume_filter=STRATEGY_VOLUME_FILTER,
            rr_threshold=MIN_RR_RATIO
        )

        if signal:
            total_trades += 1
            entry_price = df.iloc[i]['close']
            direction = signal['direction']
            sl_usd = STOP_LOSS_USD
            tp_usd = TAKE_PROFIT_USD

            # Calculate pip value based on symbol type (e.g. JPY, crypto)
            pip_value = 10 if 'JPY' in symbol else 1  # rough logic, customize as needed
            sl_pips = sl_usd / (LOT_SIZE * pip_value)
            tp_pips = tp_usd / (LOT_SIZE * pip_value)

            if direction == "BUY":
                stop_loss = entry_price - sl_pips
                take_profit = entry_price + tp_pips
            else:
                stop_loss = entry_price + sl_pips
                take_profit = entry_price - tp_pips

            # Simulate outcome
            high = df.iloc[i+1]['high']
            low = df.iloc[i+1]['low']

            if direction == "BUY":
                if low <= stop_loss:
                    losses += 1
                    pnl -= sl_usd
                elif high >= take_profit:
                    wins += 1
                    pnl += tp_usd
            else:
                if high >= stop_loss:
                    losses += 1
                    pnl -= sl_usd
                elif low <= take_profit:
                    wins += 1
                    pnl += tp_usd

    winrate = (wins / total_trades) * 100 if total_trades else 0
    print(f"[Backtest] {symbol} | Trades: {total_trades}, Wins: {wins}, Losses: {losses}, Winrate: {winrate:.2f}%, PnL: ${pnl:.2f}")

    mt5.shutdown()

def run_backtests():
    for symbol in SYMBOLS_TO_MONITOR:
        backtest_symbol(symbol)

if __name__ == "__main__":
    run_backtests()
