from nselib import derivatives


def get_option_chain(symbol="NIFTY"):

    try:
        data = derivatives.nse_live_option_chain(symbol)
        return data

    except Exception as e:
        print(e)
        return None