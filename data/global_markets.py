import yfinance as yf

def get_global_markets():

    symbols = {
        "Dow Jones": "^DJI",
        "Nasdaq": "^IXIC",
        "S&P 500": "^GSPC",
        "Nikkei 225": "^N225",
        "Hang Seng": "^HSI"
    }

    data = {}

    for name, symbol in symbols.items():

        try:
            hist = yf.Ticker(symbol).history(period="2d")

            current = hist["Close"].iloc[-1]
            previous = hist["Close"].iloc[-2]

            change = current - previous
            percent = (change / previous) * 100

            data[name] = {
                "price": round(current, 2),
                "change": round(change, 2),
                "percent": round(percent, 2)
            }

        except:
            data[name] = None

    return data