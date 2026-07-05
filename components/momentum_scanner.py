import streamlit as st
import pandas as pd

from data.sector_mapping import SECTORS
from data.volume_scanner import check_volume_condition
from data.breakout_scanner import check_breakout


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
            # Volume > 2X Avg20
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
            # Signal Logic
            # -------------------------

            if score >= 75:

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

            rows.append({

                "Stock": symbol,

                "Score": score,

                "Volume": "✅" if volume["pass_avg20"] else "❌",

                "15D Vol": "✅" if volume["pass_high15"] else "❌",

                "Bull": "🟢" if breakout["bull_breakout"] else "-",

                "Bear": "🔴" if breakout["bear_breakdown"] else "-",

                "Signal": signal,

                "Reason": ", ".join(reason)

            })

    if len(rows) == 0:

        st.warning("No Momentum Stocks Found.")
        return

    df = pd.DataFrame(rows)

    df = df.sort_values(
        by="Score",
        ascending=False
    )

    st.success(f"Scanned {len(df)} Stocks")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )