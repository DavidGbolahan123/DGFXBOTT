# data_fetcher.py

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from config import (
    CURRENCY_PAIRS,
    TIMEFRAME,
    MT5_TIMEFRAME_MAP,
    NUM_CANDLES
)

def initialize_mt5():
    """Initialize connection to MetaTrader 5."""
    if not mt5.initialize():
        raise RuntimeError(f"MT5 Initialization failed: {mt5.last_error()}")
    print("✅ MetaTrader 5 initialized.")

def shutdown_mt5():
    """Shutdown connection to MetaTrader 5."""
    mt5.shutdown()
    print("🛑 MetaTrader 5 shutdown.")

def fetch_candle_data(symbol: str, timeframe: str = TIMEFRAME, bars: int = NUM_CANDLES) -> pd.DataFrame:
    """
    Fetch historical candle data for a given symbol and timeframe.
    
    Args:
        symbol (str): Symbol to fetch data for.
        timeframe (str): Timeframe string (e.g., '15m', '1H').
        bars (int): Number of bars to fetch.

    Returns:
        pd.DataFrame: OHLCV candle data.
    """
    mt5_timeframe = MT5_TIMEFRAME_MAP.get(timeframe)
    if not mt5_timeframe:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, bars)

    if rates is None or len(rates) == 0:
        raise ValueError(f"Failed to fetch data for {symbol} at {timeframe}")

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

def fetch_all_pairs_data(timeframe: str = TIMEFRAME, bars: int = NUM_CANDLES) -> dict:
    """
    Fetch candle data for all configured currency pairs.

    Args:
        timeframe (str): Timeframe to use for all pairs.
        bars (int): Number of candles to fetch.

    Returns:
        dict: Dictionary mapping symbol -> candle DataFrame.
    """
    data = {}
    for symbol in CURRENCY_PAIRS:
        try:
            df = fetch_candle_data(symbol, timeframe, bars)
            data[symbol] = df
        except Exception as e:
            print(f"[❌] Error fetching data for {symbol}: {e}")
    return data

def get_latest_price(symbol: str) -> float:
    """
    Get the latest ask price for a symbol.

    Args:
        symbol (str): Trading symbol.

    Returns:
        float: Latest ask price.
    """
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise ValueError(f"Could not retrieve latest price for {symbol}")
    return tick.ask
