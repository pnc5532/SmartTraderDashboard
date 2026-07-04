from nselib import capital_market

data = capital_market.price_volume_data(
    symbol="SBIN",
    period="1M"
)

print(data.columns.tolist())