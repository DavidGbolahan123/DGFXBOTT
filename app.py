import time
from autosignal_sender import generate_signals
from telegram_bot import send_telegram_message

def main():
    print("🔵 DGFXBot has started...")

    while True:
        try:
            print("\n🕵️ Starting new scan...")

            signals = generate_signals()
            if signals is None:
                signals = []
            print(f"📊 Total signals generated: {len(signals)}")

            if not signals:
                print("⚠️ No signals found at this time.")
                # Optional: Add inactivity alert logic here
            else:
                for signal in signals:
                    symbol = signal.get("symbol")
                    direction = signal.get("direction")
                    print(f"📢 Signal found: {symbol} - {direction}")
                    send_telegram_message(f"🚨 Signal: {symbol} - {direction}")

            # ✅ Forced test alert for BTCUSDm to test Telegram
            test_symbol = "BTCUSDm"
            print(f"🧪 Sending test signal for {test_symbol}")
            send_telegram_message(f"🚨 TEST SIGNAL: BUY {test_symbol}")

        except Exception as e:
            print(f"❌ Error during scanning: {e}")
            send_telegram_message(f"❌ Error in DGFXBot: {str(e)}")

        print("🛏️ Sleeping for 10 minutes...\n")
        time.sleep(600)  # Sleep for 10 minutes

if __name__ == "__main__":
    main()
