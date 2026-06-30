import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

st.title("🏏 Cricbuzz LiveStats")
st.caption("Real-Time Cricket Analytics Dashboard")
st.info("Run `streamlit run Home.py` for the primary CricInsight Streamlit entrypoint.")
st.write("Use the sidebar to navigate between live matches, match details, and scorecards.")
