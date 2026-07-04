from data.sector_mapping import SECTORS


def get_scanner_conditions():

    return {
        "Top Sector": True,
        "F&O Stock": True,
        "Volume > 2x Avg(20)": False,
        "Break 2 Day High": False,
        "OI Change > 7%": False,
        "Above VWAP": False,
        "Relative Strength": False
    }