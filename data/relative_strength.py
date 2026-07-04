from nselib import capital_market
from datetime import datetime, timedelta


def get_relative_strength(symbol):

    try:

        to_date = datetime.today()
        from_date = to_date - timedelta(days=7)

        df = capital_market.price_volume_data(
            symbol,
            from_date.strftime("%d-%m-%Y"),
            to_date.strftime("%d-%m-%Y")
        )

        if df is None or len(df) < 2:
            return None

        latest = float(str(df.iloc[0]["ClosePrice"]).replace(",", ""))
        previous = float(str(df.iloc[1]["ClosePrice"]).replace(",", ""))

        change = ((latest - previous) / previous) * 100

        return round(change, 2)

    except Exception:
        return None