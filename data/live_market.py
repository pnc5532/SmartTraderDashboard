from nselib import capital_market

_live_cache = None


def get_live_market():

    global _live_cache

    if _live_cache is None:

        summary, data = capital_market.total_traded_stocks()

        data["symbol"] = data["symbol"].astype(str)

        _live_cache = data.set_index("symbol")

    return _live_cache


def get_live_stock(symbol):

    try:

        data = get_live_market()

        row = data.loc[symbol]

        return {

            "close": float(row["lastPrice"]),

            "prev_close": float(row["previousClose"]),

            "price_change": float(row["pchange"]),

            "today_volume": float(row["totalTradedVolume"])

        }

    except:

        return None


def clear_live_cache():

    global _live_cache

    _live_cache = None
    