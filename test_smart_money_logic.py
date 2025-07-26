import pandas as pd
import numpy as np
from autosignal_sender import generate_signals  # Ensure it’s pointing to your updated logic
import datetime

# --- Sample OHLCV DataFrame for testing ---
def generate_sample_df():
    data = {
        'time': pd.date_range(end=datetime.datetime.now(), periods=50, freq='H'),
        'open': np.random.uniform(1.1000, 1.2000, 50),
        'high': np.random.uniform(1.2000, 1.2500, 50),
        'low': np.random.uniform(1.0800, 1.1000, 50),
        'close': np.random.uniform(1.1000, 1.2000, 50),
        'tick_volume': np.random.randint(100, 1000, 50)
    }
    df = pd.DataFrame(data)
    df = df.sort_values(by='time').reset_index(drop=True)
    return df

# --- Inject this sample DataFrame into your logic ---
def test_smart_money_logic():
    print("🧪 Running Smart Money Logic Test...")

    sample_df = generate_sample_df()
    print(sample_df.tail())  # Show the last few candles

    # Simulate calling your logic
    signal = generate_signals(symbol="TESTPAIR", timeframe="H1", df_override=sample_df)

    print("\n📈 Signal Output:")
    print(signal)

if __name__ == "__main__":
    test_smart_money_logic()
