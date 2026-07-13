from data.market_cache import get_price_volume


def check_volume_condition(symbol):

    try:

        data = get_price_volume(symbol)

        volumes = (
            data["TotalTradedQuantity"]
            .str.replace(",", "")
            .astype(float)
        )

        today = volumes.iloc[0]
        avg20 = volumes.head(20).mean()
        high15 = volumes.head(15).max()

        close = float(str(data["ClosePrice"].iloc[0]).replace(",", ""))
        prev_close = float(str(data["PrevClose"].iloc[0]).replace(",", ""))

        return {

            "today": today,

            "avg20": avg20,

            "high15": high15,

            "ratio": round(today / avg20, 2),

            "pass_avg20": today >= avg20 * 2,

            "pass_high15": today >= high15,

            "close": close,

            "prev_close": prev_close,

            "price_change": round(
                ((close - prev_close) / prev_close) * 100,
                2
            )

        }

    except Exception as e:

        print(symbol, e)

        return None