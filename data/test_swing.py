from data.swing_market_cache import get_swing_price_volume

df = get_swing_price_volume("TCS")

print(df.head())

print("Rows =", len(df))