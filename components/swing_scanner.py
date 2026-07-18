import streamlit as st
import pandas as pd
import time

from data.swing_scanner import get_swing_candidates
from data.swing_lifecycle_scanner import run_scanner


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

    st.divider()

    st.subheader("🚀 Swing Lifecycle Scanner")

    start = time.time()

    lifecycle_df = run_scanner()

    end = time.time()

    st.success(f"✅ Lifecycle Scan Completed in {end-start:.2f} sec")

    if lifecycle_df is None or lifecycle_df.empty:
        st.warning("No Swing Lifecycle Opportunity Found")
    else:
        st.success(f"Top {len(lifecycle_df)} Swing Lifecycle Candidates")

    st.dataframe(
        lifecycle_df,
        hide_index=True,
        use_container_width=True
    )