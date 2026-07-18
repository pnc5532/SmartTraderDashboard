"""
Swing Lifecycle Scanner
Version: 2.0
"""

import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from data.sector_stocks import get_fno_stocks
from data.swing_volume import check_swing_volume
from data.swing_breakout import check_swing_breakout
from data.swing_trend import analyze_trend


def calculate_stage(df):
    if df is None or len(df) < 20:
        return "-"
    latest_high = df.iloc[0]["HighPrice"]
    for i in range(1, min(len(df), 21)):
        if latest_high >= df.iloc[i:]["HighPrice"].max():
            if i == 1:
                return "🟢 Stage 1"
            elif i <= 3:
                return "🟢 Stage 2"
            elif i <= 7:
                return "🟡 Stage 3"
            elif i <= 15:
                return "🟠 Stage 4"
            return "🔴 Stage 5"
    return "-"


def check_trend(df):
    if df is None or len(df) < 50:
        return 0
    latest = df.iloc[0]["ClosePrice"]
    ma20 = df.iloc[:20]["ClosePrice"].mean()
    ma50 = df.iloc[:50]["ClosePrice"].mean()
    score = 0
    if latest > ma20:
        score += 40
    if ma20 > ma50:
        score += 40
    if latest > ma50:
        score += 20
    return score


def calculate_volume_health(df):
    if df is None or len(df) < 20:
        return 0
    latest = df.iloc[0]
    avg = df.iloc[1:21]["TotalTradedQuantity"].mean()
    ratio = latest["TotalTradedQuantity"] / avg
    if ratio >= 3:
        return 100
    elif ratio >= 2:
        return 80
    elif ratio >= 1.5:
        return 60
    elif ratio >= 1:
        return 40
    return 20


def calculate_base_quality(df):
    if df is None or len(df) < 30:
        return 0
    base = df.iloc[1:21]
    highest = base["HighPrice"].max()
    lowest = base["LowPrice"].min()
    rng = ((highest - lowest) / lowest) * 100
    if rng <= 5:
        return 100
    elif rng <= 8:
        return 80
    elif rng <= 12:
        return 60
    elif rng <= 18:
        return 40
    return 20


def calculate_breakout_quality(df):
    if df is None or len(df) < 20:
        return 0
    latest = df.iloc[0]
    highest = df.iloc[1:21]["HighPrice"].max()
    pct = ((latest["ClosePrice"] - highest) / highest) * 100
    score = 0
    if pct >= 5:
        score += 40
    elif pct >= 3:
        score += 30
    elif pct >= 1:
        score += 20
    if latest["ClosePrice"] > latest["OpenPrice"]:
        score += 20
    rng = latest["HighPrice"] - latest["LowPrice"]
    if rng > 0:
        cp = (latest["ClosePrice"] - latest["LowPrice"]) / rng
        if cp >= 0.8:
            score += 20
    avg = df.iloc[1:21]["TotalTradedQuantity"].mean()
    vr = latest["TotalTradedQuantity"] / avg
    if vr >= 2:
        score += 20
    elif vr >= 1.5:
        score += 10
    return min(score, 100)


def calculate_swing_score(bq, trend, vol, base):
    return round(bq * 0.35 + trend * 0.30 + vol * 0.20 + base * 0.15, 1)


def get_action(score):
    if score >= 85:
        return "🟢 STRONG BUY"
    elif score >= 75:
        return "🟢 BUY"
    elif score >= 65:
        return "👀 WATCH"
    elif score >= 50:
        return "🟡 WAIT"
    return "🔴 AVOID"


def get_confidence(score):
    return f"{min(int(score),100)}%"


def get_swing_probability(score):
    if score >= 85:
        return "90%"
    elif score >= 75:
        return "80%"
    elif score >= 65:
        return "70%"
    elif score >= 50:
        return "55%"
    return "30%"


def get_holding(score):
    if score >= 85:
        return "8-12 Days"
    elif score >= 75:
        return "5-8 Days"
    elif score >= 65:
        return "3-5 Days"
    return "-"


def scan_stock(stock):

    symbol = stock["symbol"]

    volume = check_swing_volume(symbol)

    if volume is None:
        return None

    breakout = check_swing_breakout(symbol)

    if breakout is None:
        return None

    trend = analyze_trend(symbol)

    if trend is None:
        return None

    # ----------------------------------
    # Price Change
    # ----------------------------------

    price_change = (
        (volume["close"] - volume["prev_close"])
        / volume["prev_close"]
    ) * 100

    score = 0

    # ==================================
    # PRICE STRENGTH (15 Marks)
    # ==================================

    if price_change >= 6:
        score += 15

    elif price_change >= 4:
        score += 12

    elif price_change >= 2:
        score += 8

    elif price_change >= 1:
        score += 5

    # ==================================
    # BREAKOUT QUALITY (30 Marks)
    # ==================================

    if breakout["breakout30"]:
        score += 30

    elif breakout["breakout20"]:
        score += 20

    # ==================================
    # VOLUME QUALITY (25 Marks)
    # ==================================

    if breakout["volume_ratio"] >= 3:
        score += 25

    elif breakout["volume_ratio"] >= 2:
        score += 20

    elif breakout["volume_ratio"] >= 1.5:
        score += 15

    elif breakout["volume_ratio"] >= 1.2:
        score += 10

    # ==================================
    # TREND CONTINUATION (20 Marks)
    # ==================================

    if trend["trend_stage"] == "Stage 1":
        score += 20

    elif trend["trend_stage"] == "Stage 2":
        score += 15

    elif trend["trend_stage"] == "Stage 3":
        score += 8

    else:
        score += 0

    # ==================================
    # SWING POTENTIAL (10 Marks)
    # ==================================

    if (
        breakout["breakout30"]
        and breakout["volume_ratio"] >= 2
        and trend["trend_stage"] == "Stage 1"
    ):
        score += 10

    elif (
        breakout["breakout20"]
        and breakout["volume_ratio"] >= 1.5
    ):
        score += 5            

    # ==================================
    # ACTION
    # ==================================

    if score >= 90:
        action = "🟢 STRONG BUY"
        confidence = "95%"
        swing_probability = "90-95%"

    elif score >= 75:
        action = "🟢 BUY"
        confidence = "85%"
        swing_probability = "80-90%"

    elif score >= 60:
        action = "👀 WATCH"
        confidence = "75%"
        swing_probability = "65-80%"

    else:
        action = "❌ AVOID"
        confidence = "40%"
        swing_probability = "<60%"

    return {

        "Stock": symbol,

        "Score": score,

        "Price %": round(price_change, 2),

        "Volume Ratio": breakout["volume_ratio"],

        "Trend Stage": trend["trend_stage"],

        "Action": action,

        "Holding": trend["holding"],

        "Confidence": confidence,

        "Swing Probability": swing_probability,

    }

    # Aage score banayenge


def run_scanner():

    stocks = get_fno_stocks()

    if stocks is None or stocks.empty:
        return pd.DataFrame()

    stock_list = [row for _, row in stocks.iterrows()]

    with ThreadPoolExecutor(max_workers=12) as executor:
        rows = list(executor.map(scan_stock, stock_list))

    rows = [r for r in rows if r is not None]

    rows.sort(key=lambda x: x["Score"], reverse=True)

    return pd.DataFrame(rows[:20])
