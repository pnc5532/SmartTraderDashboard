from nselib import capital_market

def get_sector_data():

    try:
        df = capital_market.market_watch_all_indices()

        sectors = [
            "NIFTY BANK",
            "NIFTY IT",
            "NIFTY AUTO",
            "NIFTY FMCG",
            "NIFTY PHARMA",
            "NIFTY METAL",
            "NIFTY REALTY",
            "NIFTY MEDIA",
            "NIFTY ENERGY",
            "NIFTY PSU BANK",
            "NIFTY FINANCIAL SERVICES"
        ]

        sector_df = df[df["index"].isin(sectors)]

        return sector_df[["index", "last", "percentChange", "advances", "declines"]]

    except Exception as e:
        print(e)
        return None