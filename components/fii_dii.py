import streamlit as st
from data.fii_dii import get_fii_dii_data

def show_fii_dii():
    st.success("FII Component Loaded")
    st.divider()
    st.subheader("🏦 FII Derivatives Activity")

    data = get_fii_dii_data()

    if data is None:
        st.error("Unable to load FII Data")
        return

    st.dataframe(data, use_container_width=True)