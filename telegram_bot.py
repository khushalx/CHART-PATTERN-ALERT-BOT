"""Telegram message sender for the NIFTY alert bot."""

import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(message):
    """Send a text message to the configured Telegram chat."""
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("Telegram bot token is not configured. Message was not sent.")
        return False

    if TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID":
        print("Telegram chat ID is not configured. Message was not sent.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("Telegram message sent successfully.")
        return True
    except requests.RequestException as error:
        print(f"Failed to send Telegram message: {error}")
        return False
