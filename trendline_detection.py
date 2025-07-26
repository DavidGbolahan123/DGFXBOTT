import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from config import ENABLE_TRENDLINE_DETECTION, TRENDLINE_LOOKBACK, SUPPORT_RESISTANCE_WINDOW

def apply_trendline_filter(df, signal_type):
    if not ENABLE_TRENDLINE_DETECTION:
        return {"trend": None, "breakout": False}

    highs = df['high'].values[-TRENDLINE_LOOKBACK:]
    lows = df['low'].values[-TRENDLINE_LOOKBACK:]
    closes = df['close'].values[-TRENDLINE_LOOKBACK:]
    times = np.arange(len(highs))

    # Fit upward and downward trendlines using linear regression
    low_fit = np.polyfit(times, lows, 1)
    high_fit = np.polyfit(times, highs, 1)

    support_line = np.poly1d(low_fit)(times)
    resistance_line = np.poly1d(high_fit)(times)

    last_close = closes[-1]
    last_support = support_line[-1]
    last_resistance = resistance_line[-1]

    breakout = False
    trend = None

    if last_close > last_resistance:
        breakout = True
        trend = 'bullish'
    elif last_close < last_support:
        breakout = True
        trend = 'bearish'
    else:
        trend = 'sideways'

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, closes, label='Close', color='black')
    ax.plot(times, support_line, label='Support', linestyle='--', color='green')
    ax.plot(times, resistance_line, label='Resistance', linestyle='--', color='red')
    ax.set_title("Trendline Detection")
    ax.legend()

    # Save to local file (e.g., trendlines.png)
    image_path = "trendlines.png"
    fig.savefig(image_path)
    plt.close(fig)

    return {
        "trend": trend,
        "breakout": breakout,
        "support_line": support_line[-1],
        "resistance_line": resistance_line[-1],
        "chart": image_path
    }

def detect_trend_direction(data):
    # Defensive coding for robustness
    if isinstance(data, str):
        print("⚠️ Received string instead of DataFrame in detect_trend_direction()")
        return "unknown"

    if not isinstance(data, pd.DataFrame):
        print(f"⚠️ Invalid type for trend detection: {type(data)}")
        return "unknown"

    if 'close' not in data.columns:
        print("⚠️ 'close' column missing in data passed to detect_trend_direction()")
        return "unknown"

    try:
        if data['close'].iloc[-1] > data['close'].iloc[-5]:
            return "uptrend"
        elif data['close'].iloc[-1] < data['close'].iloc[-5]:
            return "downtrend"
        else:
            return "sideways"
    except Exception as e:
        print(f"⚠️ Error in trend detection: {e}")
        return "unknown"
