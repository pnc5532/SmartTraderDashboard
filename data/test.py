from nselib import derivatives
from datetime import datetime, timedelta

# कल की तारीख (क्योंकि FII data अक्सर T+1 होता है)
trade_date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

print("Trade Date:", trade_date)

data = derivatives.fii_derivatives_statistics(trade_date)

print(data)