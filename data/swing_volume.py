import pandas as pd
from data.swing_market_cache import get_swing_price_volume


def check_swing_volume(symbol):

    try:

        data = get_swing_price_volume(symbol)

        volume = pd.to_numeric(
            data["TotalTradedQuantity"],
            errors="coerce"
        )

        close = pd.to_numeric(
            data["ClosePrice"],
            errors="coerce"
        )

        volume = volume.dropna().reset_index(drop=True)
        close = close.dropna().reset_index(drop=True)

        if len(volume) < 21:
            return None

        # Last completed trading day
        yesterday_volume = volume.iloc[0]

        # Previous 20 trading days average
        avg20 = volume.iloc[1:21].mean()

        ratio = round(yesterday_volume / avg20, 2)

        return {

            "volume": yesterday_volume,
            "avg20": avg20,
            "ratio": ratio,

            "close": close.iloc[0],
            "prev_close": close.iloc[1]

        }

    except Exception as e:

        print(symbol, e)

        return None