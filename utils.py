# utils.py

def is_bullish_engulfing(open1, close1, open2, close2):
    return close1 < open1 and close2 > open2 and open2 < close1 and close2 > open1

def is_bearish_engulfing(open1, close1, open2, close2):
    return close1 > open1 and close2 < open2 and open2 > close1 and close2 < open1

# Add more candle pattern utils if needed
