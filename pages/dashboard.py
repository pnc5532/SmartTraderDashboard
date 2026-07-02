import streamlit as st
from datetime import datetime, time
from data.market_data import get_market_data

st.title("📊 Smart Trader Dashboard")

market = get_market_data()

col1, col2, col3, col4 = st.columns(4)

indices = [
    ("NIFTY 50", col1),
    ("BANK NIFTY", col2),
    ("SENSEX", col3),
    ("INDIA VIX", col4),
]

for name, col in indices:
    if market.get(name):
        col.metric(
            name,
            market[name]["price"],
            f'{market[name]["change"]} ({market[name]["percent"]}%)'
        )
    else:
        col.metric(name, "N/A")

st.divider()

current_time = datetime.now().time()

if time(9, 15) <= current_time <= time(15, 30):
    st.success("🟢 Market Status : OPEN")
else:
    st.error("🔴 Market Status : CLOSED")

st.caption(
    f"Last Updated : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.divider()

st.subheader("📈 Market Summary")

st.info("Top Gainers, Losers, Heatmap, FII/DII and Option Chain will be added in the next version.")