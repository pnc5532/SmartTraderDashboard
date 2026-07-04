import streamlit as st
from components.chart import show_chart
from data.global_markets import get_global_markets
from components.heatmap import show_heatmap
from data.gainers_losers import get_top_gainers, get_top_losers
from data.market_data import get_market_data
from streamlit_autorefresh import st_autorefresh
from components.market_breadth import show_market_breadth
from components.fii_dii import show_fii_dii
from components.sector_stocks import show_sector_stocks
from components.option_chain import show_option_chain
from components.momentum_scanner import show_momentum_scanner
from data.market_breadth import get_market_breadth


st.set_page_config(
    page_title="Smart Trader Dashboard",
    page_icon="📈",
    layout="wide"
)
st_autorefresh(interval=300000, key="refresh")

st.title("📈 Smart Trader Dashboard")
st.markdown("""
    ### 📊 Professional Trading Terminal
    Real-time Market • FII Activity • Global Markets • Trading Dashboard
""")

st.subheader("📊 Live Market Indices")

market = get_market_data()

col1, col2, col3, col4 = st.columns(4)

# NIFTY 50
if market.get("NIFTY 50"):
    col1.metric(
        "NIFTY 50",
        market["NIFTY 50"]["price"],
        f'{market["NIFTY 50"]["change"]} ({market["NIFTY 50"]["percent"]}%)'
    )
else:
    col1.metric("NIFTY 50", "N/A")

# BANK NIFTY
if market.get("BANK NIFTY"):
    col2.metric(
        "BANK NIFTY",
        market["BANK NIFTY"]["price"],
        f'{market["BANK NIFTY"]["change"]} ({market["BANK NIFTY"]["percent"]}%)'
    )
else:
    col2.metric("BANK NIFTY", "N/A")

# SENSEX
if market.get("SENSEX"):
    col3.metric(
        "SENSEX",
        market["SENSEX"]["price"],
        f'{market["SENSEX"]["change"]} ({market["SENSEX"]["percent"]}%)'
    )
else:
    col3.metric("SENSEX", "N/A")

# INDIA VIX
if market.get("INDIA VIX"):
    col4.metric(
        "INDIA VIX",
        market["INDIA VIX"]["price"],
        f'{market["INDIA VIX"]["change"]} ({market["INDIA VIX"]["percent"]}%)'
    )
else:
    col4.metric("INDIA VIX", "N/A")

st.divider()

st.success("✅ Live Market Data Loaded Successfully")
import datetime

st.write("Last Refresh:", datetime.datetime.now().strftime("%H:%M:%S"))
from datetime import datetime
import pytz

india_time = datetime.now(pytz.timezone("Asia/Kolkata"))

if india_time.weekday() < 5 and (
    (india_time.hour > 9 or (india_time.hour == 9 and india_time.minute >= 15))
    and
    (india_time.hour < 15 or (india_time.hour == 15 and india_time.minute <= 30))
):
    st.success("🟢 Market Open")
else:
    st.error("🔴 Market Closed")

st.caption(f"Last Updated: {india_time.strftime('%d-%m-%Y %H:%M:%S')}")
st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🟢 Top Gainers")

    gainers = get_top_gainers()

    if gainers is not None:
        st.dataframe(gainers, use_container_width=True)
    else:
        st.error("Unable to load Top Gainers.")

with right:
    st.subheader("🔴 Top Losers")

    losers = get_top_losers()

    if losers is not None:
        st.dataframe(losers, use_container_width=True)
    else:
        st.error("Unable to load Top Losers.")

st.divider()

show_fii_dii()

st.subheader("🌍 Global Markets")

global_data = get_global_markets()

col1, col2, col3, col4, col5 = st.columns(5)

markets = [
    ("Dow Jones", col1),
    ("Nasdaq", col2),
    ("S&P 500", col3),
    ("Nikkei 225", col4),
    ("Hang Seng", col5)
]

for name, col in markets:
    if global_data.get(name):
        col.metric(
            name,
            global_data[name]["price"],
            f'{global_data[name]["change"]} ({global_data[name]["percent"]}%)'
        )
    else:
        col.metric(name, "N/A")

show_heatmap()

st.divider()

show_momentum_scanner()

st.divider()

show_sector_stocks()

st.divider()

show_market_breadth()

st.divider()

show_chart()

st.divider()

#show_option_chain()
