from nselib import capital_market

summary, data = capital_market.total_traded_stocks()

row = data[data["symbol"] == "TCS"]

print(row[[
    "symbol",
    "lastPrice",
    "totalTradedVolume",
    "pchange"
]])