import streamlit as st
import pandas as pd
import time

from data.swing_scanner import get_swing_candidates


def show_swing_scanner():

    st.subheader("🏆 Swing Opportunity Scanner")

    start = time.time()

    rows = get_swing_candidates()

    end = time.time()

    st.success(f"✅ Scan Completed in {end-start:.2f} sec")

    if not rows:
        st.warning("No Swing Opportunity Found")
        return

    df = pd.DataFrame(rows)

    st.success(f"Top {len(df)} Swing Candidates")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )