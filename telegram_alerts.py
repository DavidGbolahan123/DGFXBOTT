import requests

# Replace these with your own bot token and chat ID
TELEGRAM_BOT_TOKEN = "7067823429:AAGNC-E4gI8CaM0KlbonziViY17g4otB54A"
TELEGRAM_CHAT_ID = "2069276522"  # <-- Replace this

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")
