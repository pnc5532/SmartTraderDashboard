import streamlit as st
import pandas as pd

from data.sector_mapping import SECTORS
from data.volume_scanner import check_volume_condition


def show_volume_momentum_scanner():

    st.subheader("📈 Volume Momentum Scanner")

    sector = st.selectbox(
        "Select Sector for Scanner",
        list(SECTORS.keys()),
        key="volume_scanner_sector"
    )

    stocks = SECTORS[sector]

    rows = []

    with st.spinner("Scanning Stocks..."):

        for symbol in stocks:

            volume = check_volume_condition(symbol)

            if volume is None:
                continue

            if volume["pass_avg20"]:

                today_volume = volume["today"]
                avg20_volume = volume["avg20"]

                ratio = volume["ratio"]

                rows.append({

                    "Stock": symbol,

                    "Today's Volume": f"{today_volume:,.0f}",

                    "20 Day Avg": f"{avg20_volume:,.0f}",

                    "Volume Ratio": f"{ratio} X"

                })

    if len(rows) == 0:

        st.warning("No Qualified Stocks Found")
        return

    df = pd.DataFrame(rows)

    df["Sort"] = (
        df["Volume Ratio"]
        .str.replace(" X", "", regex=False)
        .astype(float)
    )

    df = df.sort_values(
        by="Sort",
        ascending=False
    )

    df = df.drop(columns=["Sort"])

    st.success(f"✅ {len(df)} Qualified Stocks Found")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )