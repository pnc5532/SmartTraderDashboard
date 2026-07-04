from sector_mapping import SECTORS
from volume_scanner import check_volume_condition

# NIFTY BANK Sector Stocks
stocks = SECTORS["NIFTY BANK"]

print(f"Scanning {len(stocks)} NIFTY BANK Stocks...\n")

for symbol in stocks:

    result = check_volume_condition(symbol)

    if result is None:
        continue

    print("=" * 40)
    print(symbol)
    print(result)