import streamlit as st
from data.sector_stocks import get_fno_stocks
from data.sector_mapping import SECTORS


def show_sector_stocks():

    st.subheader("📋 NSE F&O Stocks")

    data = get_fno_stocks()

    sector = st.selectbox(
        "🏦 Select Sector",
        ["All"] + list(SECTORS.keys())
    )

    if sector != "All":
        symbols = SECTORS[sector]
        data = data[data["symbol"].isin(symbols)]

    search = st.text_input(
        "🔍 Search F&O Stock",
        placeholder="Type stock symbol..."
    )

    if search:
        data = data[
            data["symbol"].str.contains(search.upper(), na=False)
        ]

    st.write(f"Total F&O Stocks : {len(data)}")

    st.dataframe(
    data,
    hide_index=True,
    width="stretch"
)