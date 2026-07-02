import streamlit as st
from data.market_breadth import get_market_breadth


def show_market_breadth():

    st.subheader("📊 Market Breadth")

    data = get_market_breadth()

    col1, col2, col3 = st.columns(3)

    if data:

        col1.metric("🟢 Advances", data["advances"])
        col2.metric("🔴 Declines", data["declines"])
        col3.metric("⚪ Unchanged", data["unchanged"])

    else:

        st.error("Unable to load Market Breadth.")