from functools import lru_cache
from nselib import capital_market

@lru_cache(maxsize=300)
def get_price_volume(symbol):
    return capital_market.price_volume_data(
        symbol=symbol,
        period="1M"
    )