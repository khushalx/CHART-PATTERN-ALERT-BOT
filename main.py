"""NIFTY 5-minute candlestick Telegram alert bot using Yahoo Finance."""

import time

import pandas as pd
import yfinance as yf

from config import INTERVAL, LOOP_SECONDS, SYMBOL, TEST_MODE
from patterns import detect_patterns
from telegram_bot import send_telegram_message


def fetch_nifty_candles():
    """Fetch the latest NIFTY 5-minute candle data from Yahoo Finance."""
    print("Fetching data from Yahoo...")

    data = yf.download(
        tickers=SYMBOL,
        period="1d",
        interval=INTERVAL,
        progress=False,
        auto_adjust=False,
    )

    if data.empty:
        print("No data received from Yahoo.")
        return data

    # yfinance sometimes returns grouped columns. Flatten them if needed.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Remove rows with missing values so pattern checks receive clean candles.
    return data.dropna()


def get_last_completed_candles(data):
    """Return the last three completed candles and the latest completed time.

    The newest row from yfinance can be the candle currently forming. To avoid
    using an unfinished candle, this bot ignores the last row and analyzes the
    second-last row as the latest completed candle.
    """
    if data.empty:
        return None, None, None, None

    completed_data = data.iloc[:-1]

    # Three completed candles are needed for Morning Star and Evening Star.
    if len(completed_data) < 3:
        return None, None, None, None

    first_candle = completed_data.iloc[-3]
    second_candle = completed_data.iloc[-2]
    current_candle = completed_data.iloc[-1]
    current_candle_time = completed_data.index[-1]

    return first_candle, second_candle, current_candle, current_candle_time


def format_candle_time(candle_time):
    """Convert the candle timestamp to a readable IST time string."""
    if hasattr(candle_time, "tz_convert"):
        if candle_time.tzinfo is None:
            candle_time = candle_time.tz_localize("Asia/Kolkata")
        else:
            candle_time = candle_time.tz_convert("Asia/Kolkata")

    return candle_time.strftime("%Y-%m-%d %H:%M")


def run_bot():
    """Run the NIFTY alert bot forever."""
    last_alerted_candle_time = None

    print("NIFTY yfinance alert bot started.")
    print("Press Ctrl+C to stop.")

    if TEST_MODE:
        send_telegram_message("✅ Bot started successfully. Telegram is working.")
        print("Test message sent")

    while True:
        try:
            data = fetch_nifty_candles()
            first_candle, second_candle, current_candle, candle_time = get_last_completed_candles(data)

            if current_candle is None:
                print("Not enough completed candles to analyze.")
                time.sleep(LOOP_SECONDS)
                continue

            readable_time = format_candle_time(candle_time)
            print(f"Analyzing candle: {readable_time}")

            # Avoid duplicate alerts for the same candle timestamp.
            if candle_time == last_alerted_candle_time:
                print("This candle was already alerted.")
                time.sleep(LOOP_SECONDS)
                continue

            patterns = detect_patterns(first_candle, second_candle, current_candle)

            if patterns:
                pattern_names = ", ".join(patterns)
                print(f"Detected: {pattern_names}")

                message = f"NIFTY 5m Alert: {pattern_names} at {readable_time}"
                if send_telegram_message(message):
                    last_alerted_candle_time = candle_time
            else:
                print("No pattern found")

        except Exception as error:
            print(f"Unexpected error: {error}")

        time.sleep(LOOP_SECONDS)


if __name__ == "__main__":
    run_bot()
