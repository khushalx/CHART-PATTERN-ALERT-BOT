"""Configuration for the NIFTY yfinance alert bot."""

# Telegram bot details.
TELEGRAM_BOT_TOKEN = "8761621363:AAHsjOQsJfxjxvxkaabZkwbABUUB1NflPoA"
TELEGRAM_CHAT_ID = "5727759531"

# Send a one-time Telegram test message when the bot starts.
TEST_MODE = True

# Yahoo Finance settings for NIFTY 50 5-minute candles.
SYMBOL = "^NSEI"
INTERVAL = "5m"

# Run the bot once every 5 minutes.
LOOP_SECONDS = 5 * 60
