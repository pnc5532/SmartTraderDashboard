import streamlit as st
import pandas as pd

from data.swing_scanner import get_swing_candidates


def show_swing_scanner():

    st.subheader("🏆 Swing Opportunity Scanner")

    st.success("Swing Scanner Loaded")

    rows = get_swing_candidates()

    st.write(rows)

    if len(rows) == 0:

        st.warning("No Swing Opportunity Found")

        return

    df = pd.DataFrame(rows)

    st.success(f"Top {len(df)} Swing Candidates")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )