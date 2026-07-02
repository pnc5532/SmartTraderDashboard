import streamlit as st
import streamlit.components.v1 as components


def show_chart():

    st.subheader("📈 Live Trading Chart")

    html = """
    <iframe
    src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=NSE%3ANIFTY&interval=15&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark"
    width="100%"
    height="600"
    frameborder="0">
    </iframe>
    """

    components.html(html, height=620)