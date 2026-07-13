import streamlit as st
import pandas as pd
import time

from concurrent.futures import ThreadPoolExecutor

from data.sector_mapping import SECTORS
from data.volume_scanner import check_volume_condition
from data.breakout_scanner import check_breakout


# --------------------------------------------------
# Scan Single Stock
# --------------------------------------------------
def scan_stock(symbol):

    try:

        volume = check_volume_condition(symbol)

        if volume is None:
            return None

        breakout = check_breakout(symbol)

        if breakout is None:
            return None

        ratio = volume["ratio"]

        if ratio < 2:
            return None

        today_volume = volume["today"]
        avg20_volume = volume["avg20"]

        price_change = (
            (volume["close"] - volume["prev_close"])
            / volume["prev_close"]
        ) * 100

        # ------------------------
        # Action
        # ------------------------

        if breakout["bull_breakout"] and price_change > 0:

            action = "🟢 BUY CE"

        elif breakout["bear_breakdown"] and price_change < 0:

            action = "🔴 BUY PE"

        else:

            action = "👀 WATCH"

        # ------------------------
        # Volume Status
        # ------------------------

        if ratio >= 3:

            status = "🔥 Extreme"

        elif ratio >= 2.5:

            status = "🟢 High"

        else:

            status = "🟡 Good"

        # ------------------------
        # Price Trend
        # ------------------------

        if price_change >= 3:

            price_signal = "🟢 Strong"

        elif price_change > 0:

            price_signal = "🟡 Positive"

        else:

            price_signal = "🔴 Weak"

        return {

            "Stock": symbol,

            "Ratio": ratio,

            "Volume Ratio": f"{ratio:.2f}x",

            "Price %": f"{price_change:.2f}%",

            "Price Trend": price_signal,

            "Today's Volume": f"{today_volume:,.0f}",

            "20 Day Avg": f"{avg20_volume:,.0f}",

            "Volume Status": status,

            "Action": action

        }

    except Exception as e:

        print(symbol, e)

        return None


# --------------------------------------------------
# Main Scanner
# --------------------------------------------------
def show_volume_momentum_scanner():

    st.subheader("📈 Volume Momentum Scanner")

    sector = st.selectbox(

        "Select Sector",

        list(SECTORS.keys()),

        key="volume_scanner_sector"

    )

    stocks = SECTORS[sector]

    start = time.perf_counter()

    with st.spinner("🔍 Scanning Stocks..."):

        max_workers = min(8, len(stocks))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            rows = list(
                executor.map(
                    scan_stock,
                    stocks
                )
            )

    rows = [r for r in rows if r is not None]

    end = time.perf_counter()

    st.success(
        f"✅ Scanned {len(stocks)} Stocks in {end-start:.2f} sec"
    )

    if len(rows) == 0:

        st.warning("No Qualified Stocks Found")

        return

    df = pd.DataFrame(rows)

    df = df.sort_values(

        by="Ratio",

        ascending=False

    )

    df.insert(

        0,

        "Rank",

        range(1, len(df) + 1)

    )

    df.drop(

        columns=["Ratio"],

        inplace=True

    )

    st.success(
        f"🎯 {len(df)} Qualified Stocks Found"
    )

    st.dataframe(

        df,

        hide_index=True,

        use_container_width=True

    )