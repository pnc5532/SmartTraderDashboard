from nselib import capital_market

summary, df = capital_market.total_traded_stocks()

print(df.columns.tolist())