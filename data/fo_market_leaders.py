from nselib import capital_market


def get_fo_market_leaders():

    try:

        summary, data = capital_market.total_traded_stocks()

        # केवल F&O Stocks
        from data.sector_stocks import get_fno_stocks

        fno = get_fno_stocks()

        symbols = fno["symbol"].tolist()

        data = data[data["symbol"].isin(symbols)]

        data["pchange"] = data["pchange"].astype(float)

        gainers = data.sort_values(
            by="pchange",
            ascending=False
        ).head(10)

        losers = data.sort_values(
            by="pchange",
            ascending=True
        ).head(10)

        return gainers, losers

    except Exception as e:

        print(e)

        return None, None