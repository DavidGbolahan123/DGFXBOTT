import pandas as pd
from config import *
from technical_analysis import analyze_pair
from fibonacci import calculate_fibonacci_levels, check_fibonacci_rr
from trendline_detection import apply_trendline_filter
from candlestick_patterns import detect_candlestick_pattern
from smart_money_detection import analyze_smart_money
from smart_money_detection import detect_bos, detect_order_blocks, detect_fvg, detect_liquidity_grabs  # Placed at top (cleaner)

def generate_signal(symbol, df):
    signal = {
        "symbol": symbol,
        "signal": None,
        "rsi": None,
        "trend": None,
        "fibonacci_rr_ok": None,
        "smc_valid": None,
        "candlestick": None,
        "trendline_break": None,
        "tp": None,
        "sl": None,
        "reason": []
    }

    if df is None or len(df) < 100:
        signal["reason"].append("Not enough data")
        return signal

    # === 1. Technical Analysis ===
    rsi, macd_signal, ema_trend = analyze_technical_indicators(df)
    signal["rsi"] = rsi
    signal["trend"] = ema_trend

    # === 2. Fibonacci SL/TP & Risk/Reward ===
    fib_result = calculate_fibonacci_levels(df, ema_trend)
    fib_ok = check_fibonacci_rr(fib_result)
    signal["fibonacci_rr_ok"] = fib_ok
    signal["tp"] = fib_result.get("tp")
    signal["sl"] = fib_result.get("sl")

    # === 3. Smart Money Concept ===
    if ENABLE_SMC_FILTER:
        smc_pass = detect_smart_money_concept(df)
        signal["smc_valid"] = smc_pass
        if not smc_pass:
            signal["reason"].append("SMC filter failed")

    # === 4. Trendline Detection ===
    if ENABLE_TRENDLINE_DETECTION:
        trend_break = detect_trendlines(df)
        signal["trendline_break"] = trend_break
        if not trend_break:
            signal["reason"].append("No trendline breakout")

    # === 5. Candlestick Pattern Confirmation ===
    if ENABLE_CANDLESTICK_FILTER and REQUIRED_PATTERN_CONFIRMATION:
        candle_pattern = detect_candlestick_pattern(df)
        signal["candlestick"] = candle_pattern
        if candle_pattern == "None":
            signal["reason"].append("No valid candlestick pattern")

    # === 6. Final Signal Decision ===
    if (
        ema_trend in ["uptrend", "downtrend"] and
        (macd_signal == "buy" if ema_trend == "uptrend" else macd_signal == "sell") and
        fib_ok and
        (not ENABLE_SMC_FILTER or signal["smc_valid"]) and
        (not ENABLE_TRENDLINE_DETECTION or signal["trendline_break"]) and
        (not ENABLE_CANDLESTICK_FILTER or signal["candlestick"] != "None")
    ):
        signal["signal"] = "buy" if ema_trend == "uptrend" else "sell"
        signal["reason"].append("Valid signal conditions met")
    else:
        signal["signal"] = None
        signal["reason"].append("Signal conditions not fully met")

    return signal


# ✅ This should be outside the above function
def generate_signals(symbol, timeframe="H1", df_override=None):
    if df_override is not None:
        df = df_override
    else:
        df = get_ohlcv(symbol, timeframe)  # Make sure this returns a DataFrame

    if df is None or not hasattr(df, '__len__') or len(df) < 30:
        print(f"[❌] Insufficient or invalid data for {symbol}")
        return None

    # Proceed with signal logic
    # bos = detect_bos(df)
    # ob = detect_order_blocks(df)
    # fvg = detect_fvg(df)
    # etc...
    return {
        "symbol": symbol,
        "signal": "BUY",  # Replace with actual result
        "details": "Test signal output"
    }
