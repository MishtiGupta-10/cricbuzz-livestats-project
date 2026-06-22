import streamlit as st
from utils.api import get_live_matches, get_match_info

st.set_page_config(
    page_title="Match Details",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Match Details")
st.caption("Powered by Cricbuzz LiveStats")

matches = get_live_matches()
if not matches:
    st.error("No live matches available.")
    st.stop()

match_map = {}

for match in matches:
    match_map[f"{match['team1']} vs {match['team2']}"] = match["match_Id"]

selected_match = st.selectbox(
    "Select Match",
    list(match_map.keys())
)

st.divider()

matchId = match_map[selected_match]
match = get_match_info(matchId)

if not match :
    st.error("Unable to fetch match details.")
    st.stop()

# Match Header
st.header(f"{match['team1']} 🆚 {match['team2']}")
st.caption(f"{match['matchdesc']}")

# Status Section
st.success(f"State: {match['state']}")
st.info(f"Status: {match['status']}")

st.divider()


# Match Information
st.markdown("### 📋 Match Information")

col1, col2 = st.columns(2)

with col1:
    st.write("🏆 **Series**")
    st.write(match["seriesname"])

    st.write("")
    st.write("🏟️ **Venue**")
    st.write(match["venue"])

with col2:
    st.write("📍 **City**")
    st.write(match["city"])


