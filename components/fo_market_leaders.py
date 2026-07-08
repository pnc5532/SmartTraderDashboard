import streamlit as st

from data.fo_market_leaders import get_fo_market_leaders


def show_fo_market_leaders():

    st.subheader("🏆 F&O Market Leaders")

    gainers, losers = get_fo_market_leaders()

    if gainers is None:
        st.error("Unable to load F&O Market Leaders")
        return

    col1, col2 = st.columns(2)

    with col1:

        st.success("🚀 Top 10 Gainers")

        st.dataframe(
            gainers[
                [
                    "symbol",
                    "lastPrice",
                    "pchange"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

    with col2:

        st.error("🔻 Top 10 Losers")

        st.dataframe(
            losers[
                [
                    "symbol",
                    "lastPrice",
                    "pchange"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )