from nselib import derivatives
from datetime import datetime, timedelta

def get_fii_dii_data():
    try:
        trade_date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
        return derivatives.fii_derivatives_statistics(trade_date)
    except Exception as e:
        print(e)
        return None