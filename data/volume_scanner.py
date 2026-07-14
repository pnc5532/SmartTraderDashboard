from data.market_cache import get_price_volume
from data.live_market import get_live_stock


def check_volume_condition(symbol):

    try:

        # Historical Data (20D Average & 15D High)
        data = get_price_volume(symbol)

        # Live Data
        live = get_live_stock(symbol)

        if live is None:
            return None

        volumes = (
            data["TotalTradedQuantity"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

        avg20 = volumes.head(20).mean()
        high15 = volumes.head(15).max()

        # Live Volume
        today = live["today_volume"]

        # Live Price
        close = live["close"]
        prev_close = live["prev_close"]

        ratio = round(today / avg20, 2)

        return {

            "today": today,

            "avg20": avg20,

            "high15": high15,

            "ratio": ratio,

            "pass_avg20": today >= avg20 * 2,

            "pass_high15": today >= high15,

            "close": close,

            "prev_close": prev_close,

            "price_change": live["price_change"]

        }

    except Exception as e:

        print(symbol, e)

        return None