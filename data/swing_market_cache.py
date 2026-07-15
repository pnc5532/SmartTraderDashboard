from functools import lru_cache
import yfinance as yf


@lru_cache(maxsize=300)
def get_swing_price_volume(symbol):

    ticker = f"{symbol}.NS"

    df = yf.download(
        ticker,
        period="3mo",
        interval="1d",
        progress=False,
        auto_adjust=False,
    )

    if df.empty:
        return None

    # MultiIndex remove
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    df = df.rename(columns={
        "High": "HighPrice",
        "Low": "LowPrice",
        "Close": "ClosePrice",
        "Volume": "TotalTradedQuantity"
    })

    df = df.iloc[::-1].reset_index(drop=True)

    return df