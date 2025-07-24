# 📊 Streamlit Dashboard for Startup Matching (Single CSV Version)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the only file used
explain_df = pd.read_csv("founder_provider_explanation.csv")

st.set_page_config(page_title="Startup Match Dashboard", layout="wide")
st.title("🚀 Founder-Service Provider Match Dashboard")

# Sidebar filters
search_text = st.sidebar.text_input("🔎 Search ID (Founder or Provider)")
reason_filter = st.sidebar.text_input("🧠 Filter by Reason (e.g. skill✅)")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Filtered Explorer", "📈 Visualize a Founder", "🎯 Perfect Matches"])

# TAB 1: Filtered Explorer
with tab1:
    st.subheader("🔍 Match Table Explorer")

    filtered = explain_df.copy()

    if search_text:
        filtered = filtered[
            filtered["Founder ID"].str.contains(search_text, case=False) |
            filtered["Provider ID"].str.contains(search_text, case=False)
        ]

    if reason_filter:
        filtered = filtered[filtered["Reason"].str.contains(reason_filter, case=False)]

    filtered = filtered.sort_values(by="Score", ascending=False)
    st.dataframe(filtered, use_container_width=True)

# TAB 2: Bar Chart for a Founder
with tab2:
    st.subheader("📊 Visualize Top Matches for a Founder")

    founder_ids = explain_df["Founder ID"].unique().tolist()
    selected_founder = st.selectbox("Select Founder", founder_ids)

    founder_data = explain_df[explain_df["Founder ID"] == selected_founder]
    top_matches = founder_data.sort_values(by="Score", ascending=False).head(3)

    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["#ff4b4b", "#ffa500", "#4caf50"]
    ax.bar(top_matches["Provider ID"], top_matches["Score"], color=colors[:len(top_matches)])
    ax.set_ylim(0, 110)
    ax.set_ylabel("Score")
    ax.set_title(f"Top Matches for {selected_founder}")
    st.pyplot(fig)

    st.markdown("🧠 **Match Reasons:**")
    st.table(top_matches[["Provider ID", "Score", "Reason"]])

# TAB 3: Perfect Matches (Score = 100)
with tab3:
    st.subheader("🎯 Perfect Matches — Score 100")

    top_100_df = explain_df[explain_df["Score"] == 100.0]
    st.dataframe(top_100_df, use_container_width=True)
    st.success(f"Total Perfect Matches: {len(top_100_df)}")

st.caption("Built by Mahavishnu 💡 ScaleDux AI Intern Challenge")
