import streamlit as st
import pandas as pd

from data.sector_mapping import SECTORS
from data.volume_scanner import check_volume_condition
from data.breakout_scanner import check_breakout


def show_volume_momentum_scanner():

    st.subheader("📈 Volume Momentum Scanner")

    sector = st.selectbox(
        "Select Sector for Scanner",
        list(SECTORS.keys()),
        key="volume_scanner_sector"
    )

    stocks = SECTORS[sector]

    rows = []

    with st.spinner("🔍 Scanning Stocks..."):

        for symbol in stocks:

            # -------------------------
            # Volume Data
            # -------------------------

            volume = check_volume_condition(symbol)

            if volume is None:
                continue

            # -------------------------
            # Breakout Data
            # -------------------------

            breakout = check_breakout(symbol)

            if breakout is None:
                continue

            ratio = volume["ratio"]

            # Only show Volume Ratio >= 2
            if ratio < 2:
                continue

            today_volume = volume["today"]
            avg20_volume = volume["avg20"]

            # -------------------------
            # Price Change
            # -------------------------

            price_change = (
                (volume["close"] - volume["prev_close"])
                / volume["prev_close"]
            ) * 100

            # -------------------------
            # Action
            # -------------------------

            if breakout["bull_breakout"] and price_change > 0:

                action = "🟢 BUY CE"

            elif breakout["bear_breakdown"] and price_change < 0:

                action = "🔴 BUY PE"

            else:

                action = "👀 WATCH"

            # -------------------------
            # Volume Status
            # -------------------------

            if ratio >= 3:

                status = "🔥 Extreme"

            elif ratio >= 2.5:

                status = "🟢 High"

            else:

                status = "🟡 Good"

            # -------------------------
            # Price Trend
            # -------------------------

            if price_change >= 3:

                price_signal = "🟢 Strong"

            elif price_change > 0:

                price_signal = "🟡 Positive"

            else:

                price_signal = "🔴 Weak"

            # -------------------------
            # Add Row
            # -------------------------

            rows.append({

                "Stock": symbol,

                "Ratio": ratio,

                "Volume Ratio": f"{ratio:.2f}x",

                "Price %": f"{price_change:.2f}%",

                "Price Trend": price_signal,

                "Today's Volume": f"{today_volume:,.0f}",

                "20 Day Avg": f"{avg20_volume:,.0f}",

                "Volume Status": status,

                "Action": action

            })

    if len(rows) == 0:

        st.warning("No Qualified Stocks Found")
        return

    df = pd.DataFrame(rows)

    # Sort by Highest Volume Ratio
    df = df.sort_values(
        by="Ratio",
        ascending=False
    )

    # Rank
    df.insert(0, "Rank", range(1, len(df) + 1))

    # Remove helper column
    df = df.drop(columns=["Ratio"])

    st.success(f"✅ {len(df)} Qualified Stocks Found")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )