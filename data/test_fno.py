from nselib import capital_market

stocks = capital_market.fno_equity_list()

print(type(stocks))
print(stocks)