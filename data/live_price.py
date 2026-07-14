import yfinance as yf


def get_live_price(symbol):

    try:

        ticker = yf.Ticker(symbol + ".NS")

        data = ticker.history(period="2d", interval="1d")

        if len(data) < 2:
            return None

        close = float(data["Close"].iloc[-1])
        prev_close = float(data["Close"].iloc[-2])

        return {
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