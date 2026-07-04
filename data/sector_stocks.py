from nselib import capital_market


def get_fno_stocks():

    """
    Official NSE F&O Stocks
    """

    return capital_market.fno_equity_list()