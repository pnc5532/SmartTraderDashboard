import streamlit as st
from data.sector_heatmap import get_sector_data


def show_heatmap():

    st.subheader("🔥 NSE Sector Heatmap")

    data = get_sector_data()

    if data is None:
        st.error("Unable to load Sector Data")
        return

    # Sort sectors by performance
    ranking = data.sort_values("percentChange", ascending=False)

    # Strongest / Weakest
    best = ranking.iloc[0]
    worst = ranking.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🏆 Strongest Sector",
        best["index"],
        f"{best['percentChange']:.2f}%"
    )

    c2.metric(
        "📉 Weakest Sector",
        worst["index"],
        f"{worst['percentChange']:.2f}%"
    )

    avg_change = ranking["percentChange"].mean()

    if avg_change > 0:
        sentiment = "🟢 Bullish"
    elif avg_change < 0:
        sentiment = "🔴 Bearish"
    else:
        sentiment = "🟡 Neutral"

    c3.metric(
        "📊 Market Sentiment",
        sentiment
    )

    st.divider()

    st.subheader("🏆 Sector Ranking")

    st.dataframe(
        ranking[["index", "percentChange"]],
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    st.subheader("🟩 Sector Heatmap")

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, (_, row) in enumerate(ranking.iterrows()):

        card = f"""
### {row['index']}

**{row['percentChange']:.2f}%**

Breadth : {row['advances']} ↑ / {row['declines']} ↓
"""

        if row["percentChange"] >= 0:
            cols[i % 3].success(card)
        else:
            cols[i % 3].error(card)