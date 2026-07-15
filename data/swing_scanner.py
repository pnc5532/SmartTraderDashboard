from concurrent.futures import ThreadPoolExecutor

from data.sector_stocks import get_fno_stocks
from data.volume_scanner import check_volume_condition
from data.swing_breakout import check_swing_breakout


def scan_stock(stock):

    symbol = stock["symbol"]

    print(f"\nScanning: {symbol}")

    # ----------------------------------
    # Live Volume / Price
    # ----------------------------------

    volume = check_volume_condition(symbol)

    if volume is None:
        print(f"{symbol} -> Volume FAILED")
        return None

    # ----------------------------------
    # Swing Breakout
    # ----------------------------------

    breakout = check_swing_breakout(symbol)

    if breakout is None:
        print(f"{symbol} -> Breakout FAILED")
        return None

    print(f"{symbol} -> Breakout Data : {breakout}")

    # ----------------------------------
    # Price Change
    # ----------------------------------

    price_change = (
        (volume["close"] - volume["prev_close"])
        / volume["prev_close"]
    ) * 100

    score = 0

    # ==================================
    # PRICE STRENGTH (30 Marks)
    # ==================================

    if price_change >= 5:
        score += 30
    elif price_change >= 3:
        score += 25
    elif price_change >= 1:
        score += 15

    # ==================================
    # BREAKOUT STRENGTH (30 Marks)
    # ==================================

    if breakout["breakout30"]:
        score += 30
    elif breakout["breakout20"]:
        score += 20

    # ==================================
    # VOLUME STRENGTH (20 Marks)
    # ==================================

    if breakout["volume_ratio"] >= 3:
        score += 20
    elif breakout["volume_ratio"] >= 2:
        score += 15
    elif breakout["volume_ratio"] >= 1.5:
        score += 10

    # ==================================
    # TREND QUALITY (20 Marks)
    # ==================================

    if breakout["breakout30"] and breakout["volume_ratio"] >= 2:
        score += 20
    elif breakout["breakout20"]:
        score += 10

    print(f"{symbol} -> Final Score : {score}")

    # ==================================
    # Trend Stage
    # ==================================

    if score >= 90:

        stage = "🟢 Stage 1"

        action = "✅ Fresh Entry"

        holding = "7-15 Days"

        confidence = "95%"

    elif score >= 75:

        stage = "🟡 Stage 2"

        action = "➕ Add on Dip"

        holding = "5-10 Days"

        confidence = "85%"

    elif score >= 60:

        stage = "🟠 Stage 3"

        action = "📈 Trail SL"

        holding = "2-5 Days"

        confidence = "75%"

    else:

        stage = "🔴 Stage 4"

        action = "❌ Exit / Avoid"

        holding = "-"

        confidence = "40%"

    return {

        "Stock": symbol,

        "Score": score,

        "Price %": round(price_change, 2),

        "Volume Ratio": breakout["volume_ratio"],

        "Trend Stage": stage,

        "Action": action,

        "Holding": holding,

        "Confidence": confidence,

    }


def get_swing_candidates():

    stocks = get_fno_stocks()

    if stocks is None or stocks.empty:
        return []

    stock_list = [row for _, row in stocks.iterrows()]

    with ThreadPoolExecutor(max_workers=12) as executor:

        rows = list(executor.map(scan_stock, stock_list))

    rows = [r for r in rows if r is not None]

    rows.sort(key=lambda x: x["Score"], reverse=True)

    print("\n========== TOP 20 SWING STOCKS ==========\n")

    for row in rows[:20]:
        print(row)

    return rows[:20]