from nselib import capital_market

data = capital_market.price_volume_and_deliverable_position_data(
    symbol="TCS",
    period="3M"
)

print(type(data))
print(data)