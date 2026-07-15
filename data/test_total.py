from nselib import capital_market

summary, data = capital_market.total_traded_stocks()

print(data[data["symbol"] == "LTM"])