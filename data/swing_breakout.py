import pandas as pd
from data.swing_market_cache import get_swing_price_volume


def check_swing_breakout(symbol):

    try:

        data = get_swing_price_volume(symbol)

        if data is None or len(data) < 45:
            return None

        high = pd.to_numeric(data["HighPrice"], errors="coerce")
        low = pd.to_numeric(data["LowPrice"], errors="coerce")
        close = pd.to_numeric(data["ClosePrice"], errors="coerce")
        volume = pd.to_numeric(data["TotalTradedQuantity"], errors="coerce")

        high = high.reset_index(drop=True)
        low = low.reset_index(drop=True)
        close = close.reset_index(drop=True)
        volume = volume.reset_index(drop=True)

        # Today's values
        today_close = close.iloc[0]
        today_volume = volume.iloc[0]

        # Previous Highs
        high20 = high.iloc[1:21].max()
        high30 = high.iloc[1:31].max()

        # Previous Volume
        avg20_volume = volume.iloc[1:21].mean()

        return {

            "breakout20": today_close > high20,

            "breakout30": today_close > high30,

            "volume_ratio": round(today_volume / avg20_volume, 2),

            "today_close": today_close,

            "high20": high20,

            "high30": high30

        }

    except Exception as e:

        print(symbol, e)

        return None