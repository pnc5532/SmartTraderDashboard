import pandas as pd
from data.swing_market_cache import get_swing_price_volume


def analyze_trend(symbol):

    try:

        data = get_swing_price_volume(symbol)

        if data is None or len(data) < 35:
            return None

        high = pd.to_numeric(data["HighPrice"], errors="coerce").reset_index(drop=True)
        close = pd.to_numeric(data["ClosePrice"], errors="coerce").reset_index(drop=True)

        breakout_age = 999

        # Data latest -> oldest hai
        # Last 10 trading days me breakout kab hua?
        for age in range(11):

            today_close = close.iloc[age]

            prev20_high = high.iloc[age + 1: age + 21].max()

            if today_close > prev20_high:
                breakout_age = age
                break

        if breakout_age <= 1:
            stage = "Stage 1"
            action = "Fresh Entry"
            holding = "7-15 Days"

        elif breakout_age <= 3:
            stage = "Stage 2"
            action = "Add on Dip"
            holding = "5-10 Days"

        elif breakout_age <= 7:
            stage = "Stage 3"
            action = "Trail SL"
            holding = "2-5 Days"

        else:
            stage = "Stage 4"
            action = "Avoid Fresh Entry"
            holding = "-"

        return {
            "breakout_age": breakout_age,
            "trend_stage": stage,
            "action": action,
            "holding": holding
        }

    except Exception as e:

        print(symbol, e)

        return None