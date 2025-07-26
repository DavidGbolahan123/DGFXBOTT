# telegram_bot.py

import telegram
from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    ENABLE_TELEGRAM_ALERTS, TELEGRAM_RETRY_ATTEMPTS,
    TELEGRAM_BOT_NAME, TELEGRAM_SEND_CHART_IMAGE,
    TELEGRAM_BOT_STATUS_MESSAGE
)
import time
import logging
import os
from datetime import datetime

# Initialize bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    if not ENABLE_TELEGRAM_ALERTS:
        logging.info("[Telegram] Alerts disabled in config.")
        return

    for attempt in range(TELEGRAM_RETRY_ATTEMPTS):
        try:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            logging.info(f"[Telegram] Message sent successfully. Attempt {attempt+1}")
            return
        except Exception as e:
            logging.warning(f"[Telegram] Failed to send message. Attempt {attempt+1}. Error: {e}")
            time.sleep(2)


def send_chart_image(image_path, caption=""):
    if not TELEGRAM_SEND_CHART_IMAGE:
        return

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            try:
                bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=f, caption=caption)
                logging.info("[Telegram] Chart image sent successfully.")
            except Exception as e:
                logging.error(f"[Telegram] Failed to send chart image: {e}")
    else:
        logging.warning(f"[Telegram] Image path not found: {image_path}")


def send_bot_status():
    if TELEGRAM_BOT_STATUS_MESSAGE:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"✅ <b>{TELEGRAM_BOT_NAME} Status:</b> Online\n<b>Time:</b> {now}"
        send_telegram_message(message)


# Example usage
if __name__ == "__main__":
    send_bot_status()
    send_telegram_message("<b>DGFXBot:</b> This is a test alert from the upgraded bot.")