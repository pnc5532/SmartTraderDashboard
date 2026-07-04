from nselib import capital_market

data = capital_market.price_volume_data(
    symbol="AUBANK",
    period="1M"
)

print("===== COLUMNS =====")
print(data.columns)

print("\n===== FIRST 5 ROWS =====")
print(data.head())