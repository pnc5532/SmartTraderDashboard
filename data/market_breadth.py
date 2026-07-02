from nselib import capital_market

def get_market_breadth():
    try:
        summary, df = capital_market.total_traded_stocks()

        return {
            "advances": summary["Advances"],
            "declines": summary["Declines"],
            "unchanged": summary["Unchange"]
        }

    except Exception as e:
        print(e)
        return None