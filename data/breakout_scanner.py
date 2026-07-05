from nselib import capital_market
import pandas as pd


def check_breakout(symbol):

    try:

        data = capital_market.price_volume_data(
            symbol=symbol,
            period="1M"
        )

        high = pd.to_numeric(
            data["HighPrice"]
            .astype(str)
            .str.replace(",", "", regex=False),
            errors="coerce"
        )

        low = pd.to_numeric(
            data["LowPrice"]
            .astype(str)
            .str.replace(",", "", regex=False),
            errors="coerce"
        )

        high = high.dropna()
        low = low.dropna()

        if len(high) < 3 or len(low) < 3:
            return None

        # Today's High & Low
        today_high = high.iloc[0]
        today_low = low.iloc[0]

        # Previous 2 Days
        prev2_high = high.iloc[1:3].max()
        prev2_low = low.iloc[1:3].min()

        return {

            "bull_breakout": today_high > prev2_high,

            "bear_breakdown": today_low < prev2_low,

            "today_high": today_high,

            "today_low": today_low,

            "prev2_high": prev2_high,

            "prev2_low": prev2_low

        }

    except Exception as e:

        print(f"{symbol} : {e}")

        return None