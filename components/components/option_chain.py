import streamlit as st
from data.option_chain import get_option_chain


def show_option_chain():

    st.subheader("📈 Live Option Chain")

    data = get_option_chain()

    if data is None:
        st.error("Unable to load Option Chain")
        return

    st.dataframe(
        data,
        hide_index=True,
        use_container_width=True
    )