import streamlit as st
from utils.api import get_live_matches

st.title("🏏 Cricbuzz LiveStats")

matches = get_live_matches()

st.metric("Live Matches", len(matches))

if st.button("🔄 Refresh Scores"):
    st.success("Scores Updated!")

if not matches:
    st.warning("No live matches available right now.")

for match in matches:
    with st.container():
        st.subheader(f"{match['team1']} vs {match['team2']}")
        st.write(f"Match: {match['match_Desc']}")
        st.write(f"Status: {match['status']}")
        st.divider()