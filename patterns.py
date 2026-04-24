"""Candlestick pattern detection logic."""


def candle_parts(candle):
    """Return the body, total range, upper wick, and lower wick for one candle."""
    open_price = float(candle["Open"])
    high_price = float(candle["High"])
    low_price = float(candle["Low"])
    close_price = float(candle["Close"])

    body = abs(close_price - open_price)
    total_range = high_price - low_price
    upper_wick = high_price - max(open_price, close_price)
    lower_wick = min(open_price, close_price) - low_price

    return body, total_range, upper_wick, lower_wick


def is_bullish(candle):
    """Return True if the candle closed above its open."""
    return float(candle["Close"]) > float(candle["Open"])


def is_bearish(candle):
    """Return True if the candle closed below its open."""
    return float(candle["Close"]) < float(candle["Open"])


def is_hammer(candle):
    """Detect a Hammer candle.

    Rules:
    - Lower wick >= 2 x body
    - Upper wick <= 0.5 x body
    """
    body, total_range, upper_wick, lower_wick = candle_parts(candle)

    # A candle with no range cannot form a useful pattern.
    if total_range == 0 or body == 0:
        return False

    return lower_wick >= 2 * body and upper_wick <= 0.5 * body


def is_shooting_star(candle):
    """Detect a Shooting Star candle.

    Rules:
    - Upper wick >= 2 x body
    - Lower wick <= 0.5 x body
    """
    body, total_range, upper_wick, lower_wick = candle_parts(candle)

    if total_range == 0 or body == 0:
        return False

    return upper_wick >= 2 * body and lower_wick <= 0.5 * body


def is_inverted_hammer(candle):
    """Detect an Inverted Hammer candle.

    Rules:
    - Upper wick >= 2 x body
    - Lower wick <= 0.5 x body
    """
    body, total_range, upper_wick, lower_wick = candle_parts(candle)

    if total_range == 0 or body == 0:
        return False

    return upper_wick >= 2 * body and lower_wick <= 0.5 * body


def is_hanging_man(candle):
    """Detect a Hanging Man candle.

    Rules:
    - Lower wick >= 2 x body
    - Upper wick <= 0.5 x body
    """
    body, total_range, upper_wick, lower_wick = candle_parts(candle)

    if total_range == 0 or body == 0:
        return False

    return lower_wick >= 2 * body and upper_wick <= 0.5 * body


def is_doji(candle):
    """Detect a Doji candle.

    Rule:
    - Body <= 10% of total candle range
    """
    body, total_range, _, _ = candle_parts(candle)

    if total_range == 0:
        return False

    return body <= 0.10 * total_range


def has_small_body(candle):
    """Return True if the candle has a small body compared with its range."""
    body, total_range, _, _ = candle_parts(candle)

    if total_range == 0:
        return False

    return body <= 0.30 * total_range


def candle_midpoint(candle):
    """Return the midpoint between a candle's open and close prices."""
    return (float(candle["Open"]) + float(candle["Close"])) / 2


def is_bullish_engulfing(previous_candle, current_candle):
    """Detect a Bullish Engulfing pattern.

    Rules:
    - Previous candle bearish
    - Current candle bullish
    - Current candle body fully engulfs previous candle body
    """
    previous_open = float(previous_candle["Open"])
    previous_close = float(previous_candle["Close"])
    current_open = float(current_candle["Open"])
    current_close = float(current_candle["Close"])

    return (
        is_bearish(previous_candle)
        and is_bullish(current_candle)
        and current_open <= previous_close
        and current_close >= previous_open
    )


def is_bearish_engulfing(previous_candle, current_candle):
    """Detect a Bearish Engulfing pattern.

    Rules:
    - Previous candle bullish
    - Current candle bearish
    - Current candle body fully engulfs previous candle body
    """
    previous_open = float(previous_candle["Open"])
    previous_close = float(previous_candle["Close"])
    current_open = float(current_candle["Open"])
    current_close = float(current_candle["Close"])

    return (
        is_bullish(previous_candle)
        and is_bearish(current_candle)
        and current_open >= previous_close
        and current_close <= previous_open
    )


def is_morning_star(first_candle, second_candle, third_candle):
    """Detect a Morning Star pattern.

    Rules:
    - Candle 1 bearish
    - Candle 2 small body
    - Candle 3 bullish
    - Candle 3 closes above midpoint of candle 1
    """
    third_close = float(third_candle["Close"])

    return (
        is_bearish(first_candle)
        and has_small_body(second_candle)
        and is_bullish(third_candle)
        and third_close > candle_midpoint(first_candle)
    )


def is_evening_star(first_candle, second_candle, third_candle):
    """Detect an Evening Star pattern.

    Rules:
    - Candle 1 bullish
    - Candle 2 small body
    - Candle 3 bearish
    - Candle 3 closes below midpoint of candle 1
    """
    third_close = float(third_candle["Close"])

    return (
        is_bullish(first_candle)
        and has_small_body(second_candle)
        and is_bearish(third_candle)
        and third_close < candle_midpoint(first_candle)
    )


def is_piercing_pattern(previous_candle, current_candle):
    """Detect a Piercing Pattern.

    Rules:
    - Previous candle bearish
    - Current candle bullish
    - Current candle opens below previous close
    - Current candle closes above midpoint of previous candle
    """
    current_open = float(current_candle["Open"])
    current_close = float(current_candle["Close"])
    previous_close = float(previous_candle["Close"])

    return (
        is_bearish(previous_candle)
        and is_bullish(current_candle)
        and current_open < previous_close
        and current_close > candle_midpoint(previous_candle)
    )


def is_dark_cloud_cover(previous_candle, current_candle):
    """Detect a Dark Cloud Cover pattern.

    Rules:
    - Previous candle bullish
    - Current candle bearish
    - Current candle opens above previous close
    - Current candle closes below midpoint of previous candle
    """
    current_open = float(current_candle["Open"])
    current_close = float(current_candle["Close"])
    previous_close = float(previous_candle["Close"])

    return (
        is_bullish(previous_candle)
        and is_bearish(current_candle)
        and current_open > previous_close
        and current_close < candle_midpoint(previous_candle)
    )


def is_marubozu_bullish(candle):
    """Detect a Bullish Marubozu candle.

    Rules:
    - Current candle bullish
    - Upper wick and lower wick are very small
    - Body is at least 80% of total candle range
    """
    body, total_range, upper_wick, lower_wick = candle_parts(candle)

    if total_range == 0:
        return False

    return (
        is_bullish(candle)
        and upper_wick <= 0.10 * total_range
        and lower_wick <= 0.10 * total_range
        and body >= 0.80 * total_range
    )


def is_marubozu_bearish(candle):
    """Detect a Bearish Marubozu candle.

    Rules:
    - Current candle bearish
    - Upper wick and lower wick are very small
    - Body is at least 80% of total candle range
    """
    body, total_range, upper_wick, lower_wick = candle_parts(candle)

    if total_range == 0:
        return False

    return (
        is_bearish(candle)
        and upper_wick <= 0.10 * total_range
        and lower_wick <= 0.10 * total_range
        and body >= 0.80 * total_range
    )


def detect_patterns(first_candle, second_candle, current_candle):
    """Return a list of all detected pattern names for the current candle."""
    detected_patterns = []

    if is_hammer(current_candle):
        detected_patterns.append("Hammer")

    if is_shooting_star(current_candle):
        detected_patterns.append("Shooting Star")

    if is_inverted_hammer(current_candle):
        detected_patterns.append("Inverted Hammer")

    if is_hanging_man(current_candle):
        detected_patterns.append("Hanging Man")

    if is_doji(current_candle):
        detected_patterns.append("Doji")

    if is_bullish_engulfing(second_candle, current_candle):
        detected_patterns.append("Bullish Engulfing")

    if is_bearish_engulfing(second_candle, current_candle):
        detected_patterns.append("Bearish Engulfing")

    if is_morning_star(first_candle, second_candle, current_candle):
        detected_patterns.append("Morning Star")

    if is_evening_star(first_candle, second_candle, current_candle):
        detected_patterns.append("Evening Star")

    if is_piercing_pattern(second_candle, current_candle):
        detected_patterns.append("Piercing Pattern")

    if is_dark_cloud_cover(second_candle, current_candle):
        detected_patterns.append("Dark Cloud Cover")

    if is_marubozu_bullish(current_candle):
        detected_patterns.append("Bullish Marubozu")

    if is_marubozu_bearish(current_candle):
        detected_patterns.append("Bearish Marubozu")

    return detected_patterns
