# utils/signal_utils.py

def generate_signal(data, config=None):
    # Dummy logic for now – replace this with your actual signal logic
    if data.get("trend") == "bullish":
        return {
            "signal": "BUY",
            "reason": "Uptrend detected",
            "confidence": 0.8
        }
    elif data.get("trend") == "bearish":
        return {
            "signal": "SELL",
            "reason": "Downtrend detected",
            "confidence": 0.75
        }
    else:
        return {
            "signal": "HOLD",
            "reason": "No clear trend",
            "confidence": 0.5
        }
