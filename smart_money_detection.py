import config
import numpy as np
import pandas as pd
import MetaTrader5 as mt5


def detect_bos(df):
    """
    Detect Break of Structure (BOS) - change in market structure.
    """
    bos_signals = []
    for i in range(2, len(df)):
        prev_high = df['high'][i - 2]
        curr_high = df['high'][i - 1]
        prev_low = df['low'][i - 2]
        curr_low = df['low'][i - 1]

        if curr_high > prev_high and curr_low > prev_low:
            bos_signals.append('bullish_bos')
        elif curr_high < prev_high and curr_low < prev_low:
            bos_signals.append('bearish_bos')
        else:
            bos_signals.append(None)
    return [None, None] + bos_signals


def detect_order_blocks(df):
    """
    Simple logic for detecting order blocks (based on engulfing candles).
    """
    ob_signals = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if curr['close'] > curr['open'] and prev['close'] < prev['open'] and curr['open'] < prev['close']:
            ob_signals.append('bullish_ob')
        elif curr['close'] < curr['open'] and prev['close'] > prev['open'] and curr['open'] > prev['close']:
            ob_signals.append('bearish_ob')
        else:
            ob_signals.append(None)
    return [None] + ob_signals


def detect_fvg(df):
    """
    Detect Fair Value Gaps (FVG): Imbalance between candle bodies and wicks.
    """
    fvg_signals = []
    for i in range(2, len(df)):
        prev = df.iloc[i - 2]
        curr = df.iloc[i]

        if prev['high'] < curr['low']:
            fvg_signals.append('bullish_fvg')
        elif prev['low'] > curr['high']:
            fvg_signals.append('bearish_fvg')
        else:
            fvg_signals.append(None)
    return [None, None] + fvg_signals


def detect_liquidity_grabs(df):
    """
    Detect potential stop hunt or liquidity grab patterns.
    """
    liquidity_signals = []
    for i in range(2, len(df)):
        prev_low = df['low'][i - 1]
        curr_low = df['low'][i]

        prev_high = df['high'][i - 1]
        curr_high = df['high'][i]

        if curr_low < prev_low and df['close'][i] > df['open'][i]:
            liquidity_signals.append('bullish_liquidity_grab')
        elif curr_high > prev_high and df['close'][i] < df['open'][i]:
            liquidity_signals.append('bearish_liquidity_grab')
        else:
            liquidity_signals.append(None)
    return [None, None] + liquidity_signals


def get_ohlcv(symbol, timeframe, bars=500):
    """
    Fetch OHLCV data from MT5 and return as DataFrame.
    """
    timeframe_map = {
        '1m': mt5.TIMEFRAME_M1,
        '5m': mt5.TIMEFRAME_M5,
        '15m': mt5.TIMEFRAME_M15,
        '30m': mt5.TIMEFRAME_M30,
        '1h': mt5.TIMEFRAME_H1,
        'H1': mt5.TIMEFRAME_H1,
        '4h': mt5.TIMEFRAME_H4,
        'H4': mt5.TIMEFRAME_H4,
        '1d': mt5.TIMEFRAME_D1,
        'D1': mt5.TIMEFRAME_D1
    }

    tf = timeframe_map.get(timeframe)
    if tf is None:
        print(f"⛔ Unsupported timeframe: {timeframe}")
        return None

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
    if rates is None:
        print(f"⚠️ Failed to fetch data for {symbol}")
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df


def analyze_smart_money(symbol, timeframe):
    """
    Perform full smart money concept analysis using enabled config flags.
    Returns: Dict with latest signal info.
    """
    df = get_ohlcv(symbol, timeframe)

    if df is None or len(df) < 50:
        print(f"[❌] Insufficient data for {symbol}")
        return None

    signals = {
        'bos': None,
        'order_block': None,
        'fvg': None,
        'liquidity_grab': None,
        'overall_smc_signal': None
    }

    if config.ENABLE_SMC_FILTER:
        if getattr(config, "USE_BOS", False):
            df['bos'] = detect_bos(df)
            signals['bos'] = df['bos'].iloc[-1]

        if getattr(config, "USE_ORDER_BLOCKS", False):
            df['order_block'] = detect_order_blocks(df)
            signals['order_block'] = df['order_block'].iloc[-1]

        if getattr(config, "USE_FVG", False):
            df['fvg'] = detect_fvg(df)
            signals['fvg'] = df['fvg'].iloc[-1]

        if getattr(config, "USE_LIQUIDITY_GRABS", False):
            df['liquidity_grab'] = detect_liquidity_grabs(df)
            signals['liquidity_grab'] = df['liquidity_grab'].iloc[-1]

        bullish_count = sum(1 for v in signals.values() if isinstance(v, str) and 'bullish' in v)
        bearish_count = sum(1 for v in signals.values() if isinstance(v, str) and 'bearish' in v)

        if bullish_count > bearish_count:
            signals['overall_smc_signal'] = 'bullish'
        elif bearish_count > bullish_count:
            signals['overall_smc_signal'] = 'bearish'
        else:
            signals['overall_smc_signal'] = 'neutral'

    return signals

