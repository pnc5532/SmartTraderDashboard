import streamlit as st

from components.swing_scanner import show_swing_scanner

st.set_page_config(
    page_title="Swing Opportunity Scanner",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Swing Opportunity Scanner")

st.markdown("""
### 📈 Find F&O Stocks with Multi-Day Momentum
Identify stocks that may continue their trend for the next few trading sessions.
""")

st.divider()

show_swing_scanner()