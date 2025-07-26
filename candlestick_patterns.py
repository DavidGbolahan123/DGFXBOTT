import pandas as pd
import config

def detect_candlestick_pattern(df):
    if not config.ENABLE_CANDLESTICK_FILTER or df is None or len(df) < 3:
        return None

    last_candle = df.iloc[-1]
    prev_candle = df.iloc[-2]
    second_prev_candle = df.iloc[-3]

    body = abs(last_candle['close'] - last_candle['open'])
    range_candle = last_candle['high'] - last_candle['low']
    body_ratio = body / range_candle if range_candle else 0

    # Bullish Engulfing
    if (
        prev_candle['close'] < prev_candle['open'] and
        last_candle['close'] > last_candle['open'] and
        last_candle['open'] < prev_candle['close'] and
        last_candle['close'] > prev_candle['open']
    ):
        return 'bullish_engulfing'

    # Bearish Engulfing
    if (
        prev_candle['close'] > prev_candle['open'] and
        last_candle['close'] < last_candle['open'] and
        last_candle['open'] > prev_candle['close'] and
        last_candle['close'] < prev_candle['open']
    ):
        return 'bearish_engulfing'

    # Hammer
    if (
        body_ratio < 0.3 and
        (last_candle['low'] < min(last_candle['open'], last_candle['close'])) and
        (last_candle['high'] - max(last_candle['open'], last_candle['close']) < body * 0.5)
    ):
        return 'hammer'

    # Shooting Star
    if (
        body_ratio < 0.3 and
        (last_candle['high'] > max(last_candle['open'], last_candle['close'])) and
        (min(last_candle['open'], last_candle['close']) - last_candle['low'] < body * 0.5)
    ):
        return 'shooting_star'

    # Morning Star
    if (
        second_prev_candle['close'] < second_prev_candle['open'] and
        abs(prev_candle['close'] - prev_candle['open']) < body * 0.2 and
        last_candle['close'] > last_candle['open'] and
        last_candle['close'] > second_prev_candle['open']
    ):
        return 'morning_star'

    # Evening Star
    if (
        second_prev_candle['close'] > second_prev_candle['open'] and
        abs(prev_candle['close'] - prev_candle['open']) < body * 0.2 and
        last_candle['close'] < last_candle['open'] and
        last_candle['close'] < second_prev_candle['open']
    ):
        return 'evening_star'

    return None
