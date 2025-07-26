import numpy as np

def calculate_fibonacci_levels(high, low):
    """
    Calculates the standard Fibonacci retracement levels.
    Returns a dictionary of retracement levels.
    """
    diff = high - low
    return {
        "0.0%": high,
        "23.6%": high - 0.236 * diff,
        "38.2%": high - 0.382 * diff,
        "50.0%": high - 0.5 * diff,
        "61.8%": high - 0.618 * diff,
        "78.6%": high - 0.786 * diff,
        "100.0%": low,
    }

def is_fib_retracement_valid(price, high, low, tolerance=5):
    """
    Checks if current price is close to any significant Fibonacci level.
    Tolerance is in pips (or points).
    """
    fib_levels = calculate_fibonacci_levels(high, low)
    for level_name, level_price in fib_levels.items():
        if abs(price - level_price) <= tolerance:
            return True, level_name
    return False, None

def get_recent_high_low(rates, window=100):
    """
    Get recent swing high and low from candle data.
    """
    highs = [bar.high for bar in rates[-window:]]
    lows = [bar.low for bar in rates[-window:]]
    return max(highs), min(lows)

def get_fibonacci_signal(price, rates, window=100, tolerance=5):
    """
    Check if current price aligns with a significant Fibonacci level.
    Returns level name if valid.
    """
    high, low = get_recent_high_low(rates, window)
    valid, level = is_fib_retracement_valid(price, high, low, tolerance)
    return level if valid else None

def check_fibonacci_rr(entry_price, stop_loss, take_profit):
    """
    Check if Risk:Reward ratio is at least 1:2
    For example: SL = 50 pips, TP = 100 pips (R:R = 1:2)
    """
    try:
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        if risk == 0:
            return False
        rr_ratio = reward / risk
        print(f"🔍 R:R = {rr_ratio:.2f} | Entry: {entry_price}, SL: {stop_loss}, TP: {take_profit}")
        return rr_ratio >= 2.0  # Accept only if R:R is 1:2 or more
    except Exception as e:
        print(f"[⚠️] Error checking Fibonacci RR: {e}")
        return False
