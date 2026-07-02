import yfinance as yf

def get_market_data():
    symbols = {
        "NIFTY 50": "^NSEI",
        "BANK NIFTY": "^NSEBANK",
        "SENSEX": "^BSESN",
        "INDIA VIX": "^INDIAVIX"
    }

    market = {}

    for name, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")

            if len(hist) >= 2:
                current = hist["Close"].iloc[-1]
                previous = hist["Close"].iloc[-2]
                change = current - previous
                change_percent = (change / previous) * 100

                market[name] = {
                    "price": round(current, 2),
                    "change": round(change, 2),
                    "percent": round(change_percent, 2)
                }
            else:
                market[name] = None

        except Exception:
            market[name] = None

    return market