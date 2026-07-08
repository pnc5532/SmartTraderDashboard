import streamlit as st
import pandas as pd

from data.sector_mapping import SECTORS
from data.volume_scanner import check_volume_condition
from data.breakout_scanner import check_breakout
from data.signal_time import update_signal_time


def show_momentum_scanner():

    st.subheader("🎯 Momentum Scanner")

    sector = st.selectbox(
        "📂 Select Sector",
        list(SECTORS.keys()),
        key="scanner_sector"
    )

    stocks = SECTORS[sector]

    rows = []

    with st.spinner("🔍 Scanning Stocks..."):

        for symbol in stocks:

            volume = check_volume_condition(symbol)

            if volume is None:
                continue

            breakout = check_breakout(symbol)

            if breakout is None:
                continue

            score = 0
            reason = []

            # -------------------------
            # Price Change
            # -------------------------

            price_change = (
                (volume["close"] - volume["prev_close"])
                / volume["prev_close"]
            ) * 100

            # -------------------------
            # 2X Average Volume
            # -------------------------

            if volume["pass_avg20"]:

                score += 25
                reason.append("2X Volume")

            # -------------------------
            # Highest Volume in 15 Days
            # -------------------------

            if volume["pass_high15"]:

                score += 25
                reason.append("15D High Vol")

            # -------------------------
            # Bull Breakout
            # -------------------------

            if breakout["bull_breakout"]:

                score += 25
                reason.append("Bull Break")

            # -------------------------
            # Bear Breakdown
            # -------------------------

            if breakout["bear_breakdown"]:

                score += 25
                reason.append("Bear Break")

            # -------------------------
            # Price Strength Bonus
            # -------------------------

            if price_change >= 5:

                score += 20
                reason.append("Strong Price")

            elif price_change >= 3:

                score += 15
                reason.append("Price Up")

            elif price_change >= 1:

                score += 10
                reason.append("Positive Price")

            # -------------------------
            # Volume Ratio Bonus
            # -------------------------

            if volume["ratio"] >= 3:

                score += 10
                reason.append("3X Volume")

            elif volume["ratio"] >= 2.5:

                score += 5
                reason.append("2.5X Volume")

            # -------------------------
            # Signal
            # -------------------------

            if score >= 90:

                if breakout["bull_breakout"]:

                    signal = "🔥 STRONG BUY CE"

                elif breakout["bear_breakdown"]:

                    signal = "🔥 STRONG BUY PE"

                else:

                    signal = "🔥 STRONG"

            elif score >= 75:

                if breakout["bull_breakout"]:

                    signal = "🟢 BUY CE"

                elif breakout["bear_breakdown"]:

                    signal = "🔴 BUY PE"

                else:

                    signal = "🟢 ENTRY"

            elif score >= 50:

                signal = "🟡 READY"

            elif score >= 25:

                signal = "👀 WATCH"

            else:

                signal = "❌ IGNORE"

            signal_time = update_signal_time(
                symbol,
                signal
            )

            rows.append({

                "Stock": symbol,

                "Score": score,

                "Price %": f"{price_change:.2f}%",

                "Vol Ratio": f"{volume['ratio']:.2f}x",

                "Volume": "✅" if volume["pass_avg20"] else "❌",

                "15D Vol": "✅" if volume["pass_high15"] else "❌",

                "Bull": "🟢" if breakout["bull_breakout"] else "-",

                "Bear": "🔴" if breakout["bear_breakdown"] else "-",

                "Signal": signal,

                "Signal Time": signal_time,

                "Reason": ", ".join(reason)

            })

    if len(rows) == 0:

        st.warning("No Momentum Stocks Found.")
        return

    df = pd.DataFrame(rows)

    df = df.sort_values(
        by=["Score", "Stock"],
        ascending=[False, True]
    )

    st.success(f"Scanned {len(df)} Stocks")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )