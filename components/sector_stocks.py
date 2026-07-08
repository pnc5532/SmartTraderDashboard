import streamlit as st
from data.sector_stocks import get_fno_stocks
from data.sector_mapping import SECTORS
from data.sector_mapping import SECTORS, HEATMAP_TO_SECTOR


def show_sector_stocks():

    # कोई sector select नहीं हुआ
    if "selected_sector" not in st.session_state:
        return

    heatmap_sector = st.session_state["selected_sector"]

    sector = HEATMAP_TO_SECTOR.get(
        heatmap_sector,
        heatmap_sector
    )

    st.subheader(f"📋 {sector} Stocks")

    data = get_fno_stocks()

    symbols = SECTORS.get(sector, [])

    data = data[data["symbol"].isin(symbols)]

    st.success(f"{len(data)} Stocks Found")

    st.dataframe(
        data,
        hide_index=True,
        width="stretch"
    )