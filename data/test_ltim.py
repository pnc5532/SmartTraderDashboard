from market_cache import get_price_volume

data = get_price_volume("LTIM")

print(data[[
    "Date",
    "ClosePrice",
    "PrevClose",
    "HighPrice",
    "LowPrice",
    "TotalTradedQuantity"
]].head(5))