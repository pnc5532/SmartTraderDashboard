from data.sector_stocks import get_fno_stocks
from data.volume_scanner import check_volume_condition
from data.breakout_scanner import check_breakout


def get_swing_candidates():

    stocks = get_fno_stocks()

    if stocks is None:
        return []

    rows = []

    for _, stock in stocks.iterrows():

        symbol = stock["symbol"]

        volume = check_volume_condition(symbol)

        if volume is None:
            continue

        breakout = check_breakout(symbol)

        if breakout is None:
            continue

        price_change = (
            (volume["close"] - volume["prev_close"])
            / volume["prev_close"]
        ) * 100

        score = 0

        # -------------------------
        # Price Strength
        # -------------------------

        if price_change >= 5:
            score += 20

        elif price_change >= 3:
            score += 15

        elif price_change >= 1:
            score += 10

        # -------------------------
        # Volume
        # -------------------------

        if volume["ratio"] >= 2:
            score += 15

        elif volume["ratio"] >= 1.5:
            score += 10

        # -------------------------
        # Breakout
        # -------------------------

        if breakout["bull_breakout"]:
            score += 20

        elif breakout["bear_breakdown"]:
            score -= 20

        # -------------------------
        # Swing Signal
        # -------------------------

        if score >= 50:

            signal = "🚀 Strong Buy"

            holding = "5-15 Days"

            confidence = "90%"

        elif score >= 40:

            signal = "🔥 Buy"

            holding = "3-10 Days"

            confidence = "80%"

        elif score >= 30:

            signal = "🟢 Trend Continue"

            holding = "3-7 Days"

            confidence = "70%"

        elif score >= 20:

            signal = "👀 Watch"

            holding = "-"

            confidence = "55%"

        else:

            signal = "❌ Avoid"

            holding = "-"

            confidence = "30%"

        rows.append({

            "Stock": symbol,

            "Price %": round(price_change,2),

            "Volume Ratio": round(volume["ratio"],2),

            "Score": score,

            "Signal": signal,

            "Holding": holding,

            "Confidence": confidence

        })

    rows = sorted(
        rows,
        key=lambda x: x["Score"],
        reverse=True
    )

    return rows