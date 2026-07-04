from nselib import capital_market


def check_volume_condition(symbol):

    try:

        data = capital_market.price_volume_data(
            symbol=symbol,
            period="1M"
        )

        volumes = (
            data["TotalTradedQuantity"]
            .str.replace(",", "")
            .astype(float)
        )

        today = volumes.iloc[0]

        avg20 = volumes.head(20).mean()

        high15 = volumes.head(15).max()

        return {

            "today": today,

            "avg20": avg20,

            "high15": high15,

            "ratio": round(today / avg20, 2),

            "pass_avg20": today >= avg20 * 2,

            "pass_high15": today >= high15

        }

    except Exception as e:

        print(symbol, e)

        return None