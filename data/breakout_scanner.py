from nselib import capital_market


def check_breakout(symbol):

    try:

        data = capital_market.price_volume_data(
            symbol=symbol,
            period="1M"
        )

        high = data["HighPrice"].astype(float)
        low = data["LowPrice"].astype(float)

        today_high = high.iloc[0]
        today_low = low.iloc[0]

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

        print(symbol, e)

        return None