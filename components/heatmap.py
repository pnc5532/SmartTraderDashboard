import streamlit as st

def show_heatmap():

    st.subheader("🔥 NSE Sector Heatmap")

    col1, col2, col3, col4 = st.columns(4)

    col1.success("🏦 BANK")
    col2.success("💻 IT")
    col3.error("💊 PHARMA")
    col4.success("🚗 AUTO")

    col5, col6, col7, col8 = st.columns(4)

    col5.error("⚙️ METAL")
    col6.success("🏠 REALTY")
    col7.error("⚡ ENERGY")
    col8.success("📡 FMCG")