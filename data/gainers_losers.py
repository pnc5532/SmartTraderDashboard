from nselib import capital_market

def get_top_gainers():
    try:
        summary, df = capital_market.total_traded_stocks()

        gainers = df.sort_values(
            by="pchange",
            ascending=False
        ).head(10)

        return gainers[
            ["symbol", "lastPrice", "pchange"]
        ]

    except Exception as e:
        print(e)
        return None


def get_top_losers():
    try:
        summary, df = capital_market.total_traded_stocks()

        losers = df.sort_values(
            by="pchange"
        ).head(10)

        return losers[
            ["symbol", "lastPrice", "pchange"]
        ]

    except Exception as e:
        print(e)
        return None