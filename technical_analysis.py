import pandas as pd
import numpy as np
from trendline_detection import detect_trend_direction
from support_resistance import is_near_support_or_resistance
from fibonacci import is_fib_retracement_valid
from candlestick_patterns import detect_candlestick_pattern
from indicator_utils import calculate_rsi, calculate_macd, calculate_ema

def analyze_pair(symbol, df):
    try:
        if not isinstance(df, pd.DataFrame) or df.empty:
            print(f"⚠️ Data error: Invalid DataFrame for {symbol}")
            return None

        if len(df) < 50:
            print(f"⚠️ Not enough data to analyze {symbol}")
            return None

        latest_data = df.iloc[-1]

        # === 1. Detect Trend ===
        trend = detect_trend_direction(df)
        if trend not in ["uptrend", "downtrend"]:
            print(f"🔍 No clear trend for {symbol}")
            return None

        # === 2. Support/Resistance ===
        support, resistance = is_near_support_or_resistance(df)
        near_support = support and trend == "uptrend"
        near_resistance = resistance and trend == "downtrend"

        if not (near_support or near_resistance):
            print(f"🛑 No S/R confluence for {symbol}")
            return None

        # === 3. RSI ===
        rsi = calculate_rsi(df['close'])
        latest_rsi = rsi.iloc[-1] if not rsi.empty else None

        if latest_rsi is None:
            print(f"⚠️ RSI missing for {symbol}")
            return None

        if trend == "uptrend" and latest_rsi > 70:
            print(f"🔻 Overbought RSI ({latest_rsi}) for {symbol}")
            return None
        if trend == "downtrend" and latest_rsi < 30:
            print(f"🔺 Oversold RSI ({latest_rsi}) for {symbol}")
            return None

        # === 4. EMA Confluence ===
        ema20 = calculate_ema(df['close'], 20)
        ema50 = calculate_ema(df['close'], 50)

        if ema20 is None or ema50 is None:
            print(f"⚠️ EMA calculation failed for {symbol}")
            return None

        price = latest_data['close']
        bullish_ema = price > ema20.iloc[-1] > ema50.iloc[-1]
        bearish_ema = price < ema20.iloc[-1] < ema50.iloc[-1]

        if trend == "uptrend" and not bullish_ema:
            print(f"📉 EMA not bullish for {symbol}")
            return None
        if trend == "downtrend" and not bearish_ema:
            print(f"📈 EMA not bearish for {symbol}")
            return None

        # === 5. MACD Confirmation ===
        macd_line, signal_line = calculate_macd(df['close'])
        if macd_line is None or signal_line is None:
            print(f"⚠️ MACD calc failed for {symbol}")
            return None

        if trend == "uptrend" and macd_line.iloc[-1] < signal_line.iloc[-1]:
            print(f"❌ MACD not confirming uptrend for {symbol}")
            return None
        if trend == "downtrend" and macd_line.iloc[-1] > signal_line.iloc[-1]:
            print(f"❌ MACD not confirming downtrend for {symbol}")
            return None

        # === 6. Candle Pattern ===
        pattern_confirmed = detect_candlestick_pattern(df)
        if not pattern_confirmed:
            print(f"🕯️ No strong candle pattern for {symbol}")
            return None

        # === 7. Fibonacci ===
        try:
            if not is_fib_retracement_valid(df, trend):
                print(f"📐 Fibonacci invalid for {symbol}")
                return None
        except Exception as e:
            print(f"⚠️ Fib error for {symbol}: {e}")
            return None

        # ✅ All checks passed
        print(f"✅ Signal detected for {symbol}: {trend.upper()}")
        return {
            'symbol': symbol,
            'trend': trend,
            'rsi': round(latest_rsi, 2),
            'support': support,
            'resistance': resistance,
            'confirmed_pattern': pattern_confirmed,
            'ema20': round(ema20.iloc[-1], 2),
            'ema50': round(ema50.iloc[-1], 2),
            'macd': round(macd_line.iloc[-1], 2),
            'signal_line': round(signal_line.iloc[-1], 2),
            'signal': 'buy' if trend == "uptrend" else 'sell'
        }

    except Exception as e:
        print(f"[❌ ERROR] Failed to analyze {symbol}: {e}")
        return None
