import streamlit as st
import pandas as pd
import time

from concurrent.futures import ThreadPoolExecutor

from data.sector_mapping import SECTORS
from data.volume_scanner import check_volume_condition
from data.breakout_scanner import check_breakout
from data.signal_time import update_signal_time


def scan_stock(symbol):

    try:

        volume = check_volume_condition(symbol)

        if volume is None:
            return None

        breakout = check_breakout(symbol)

        if breakout is None:
            return None

        price_change = volume["price_change"]

        score = 0
        reason = []

        # -------------------------
        # PRICE STRENGTH
        # -------------------------

        if price_change >= 5:
            score += 40
            reason.append("🔥 Strong Price")

        elif price_change >= 3:
            score += 30
            reason.append("📈 Price Up")

        elif price_change >= 1:
            score += 15
            reason.append("🟢 Positive")

        elif price_change <= -5:
            score += 40
            reason.append("🔻 Strong Fall")

        elif price_change <= -3:
            score += 30
            reason.append("📉 Price Down")

        elif price_change <= -1:
            score += 15
            reason.append("🔴 Negative")

        # -------------------------
        # VOLUME
        # -------------------------

        if volume["pass_avg20"]:
            score += 20
            reason.append("2X Volume")

        if volume["pass_high15"]:
            score += 10
            reason.append("15D High Volume")

        if volume["ratio"] >= 3:
            score += 10
            reason.append("3X Volume")

        elif volume["ratio"] >= 2.5:
            score += 5
            reason.append("2.5X Volume")

        # -------------------------
        # BREAKOUT
        # -------------------------

        if breakout["bull_breakout"]:
            score += 30
            reason.append("Bull Break")

        if breakout["bear_breakdown"]:
            score += 30
            reason.append("Bear Break")

        # -------------------------
        # SIGNAL
        # -------------------------

        if (
            breakout["bull_breakout"]
            and price_change > 0
            and score >= 70
        ):

            signal = "🟢 BUY CE"

        elif (
            breakout["bear_breakdown"]
            and price_change < 0
            and score >= 70
        ):

            signal = "🔴 BUY PE"

        elif score >= 50:

            signal = "👀 WATCH"

        else:

            signal = "❌ IGNORE"

        signal_time = update_signal_time(
            symbol,
            signal
        )

        return {

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

        }

    except Exception as e:

        print(symbol, e)

        return None

def show_momentum_scanner():

    st.subheader("🎯 Momentum Scanner")

    sector = st.selectbox(
        "📂 Select Sector",
        list(SECTORS.keys()),
        key="scanner_sector"
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

        st.warning("No Momentum Stocks Found.")

        return

    df = pd.DataFrame(rows)

    # -------------------------
    # Numeric Columns
    # -------------------------

    df["PriceNum"] = (
        df["Price %"]
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    df["VolNum"] = (
        df["Vol Ratio"]
        .str.replace("x", "", regex=False)
        .astype(float)
    )

    # -------------------------
    # Signal Priority
    # -------------------------

    signal_priority = {

        "🟢 BUY CE": 4,

        "🔴 BUY PE": 4,

        "👀 WATCH": 3,

        "❌ IGNORE": 1

    }

    df["SignalRank"] = df["Signal"].map(signal_priority)

    # -------------------------
    # Final Sorting
    # -------------------------

    df = df.sort_values(

        by=[
            "SignalRank",
            "Score",
            "PriceNum",
            "VolNum"
        ],

        ascending=[
            False,
            False,
            False,
            False
        ]

    )

    # -------------------------
    # Rank
    # -------------------------

    df.insert(
        0,
        "Rank",
        range(1, len(df) + 1)
    )

    # -------------------------
    # Cleanup
    # -------------------------

    df.drop(
        columns=[
            "SignalRank",
            "PriceNum",
            "VolNum"
        ],
        inplace=True
    )

    st.success(
        f"🎯 {len(df)} Momentum Stocks Found"
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )