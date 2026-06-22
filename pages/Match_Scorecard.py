import streamlit as st
import pandas as pd
from utils.api import get_scorecard, get_live_matches

st.set_page_config(
    page_title="Match Scorecard",
    page_icon="🏏",
    layout="wide"
)

# Page Header
st.title("🏏 Match Scorecard")
st.caption("Powered by Cricbuzz LiveStats")

# Fetch Live Matches
matches = get_live_matches()

if not matches:
    st.error("No live matches available.")
    st.stop()

# Match Mapping
match_map = {}

for match in matches:
    match_map[f"{match['team1']} vs {match['team2']}"] = match["match_Id"]

# Dropdown
selected_match = st.selectbox(
    "Select Match",
    list(match_map.keys())
)

# Fetch Scorecard
matchId = match_map[selected_match]
scorecard = get_scorecard(matchId)

if not scorecard:
    st.error("Unable to fetch scorecard.")
    st.stop()

innings = scorecard[0]

# Match Header
st.header(f"🏏 {selected_match}")

st.divider()

# Summary Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Team", innings["batteamname"])

with col2:
    st.metric(
        "Score",
        f"{innings['score']}/{innings['wickets']}"
    )

with col3:
    st.metric("Overs", innings["overs"])

with col4:
    st.metric("Run Rate", innings["runrate"])

st.divider()

# ---------------- BATTING ---------------- #

st.subheader("🏏 Batting Scorecard")

batting_data = []

for batter in innings["batsman"]:
    batting_data.append({
        "Name": batter["name"],
        "Runs": batter["runs"],
        "Balls": batter["balls"],
        "4s": batter["fours"],
        "6s": batter["sixes"],
        "SR": batter["strkrate"]
    })

batting_df = pd.DataFrame(batting_data)

st.dataframe(
    batting_df,
    hide_index=True, 
    width = "stretch"
)

st.divider()

# ---------------- BOWLING ---------------- #

st.subheader("🎯 Bowling Scorecard")

bowler_data = []

for bowler in innings["bowler"]:
    bowler_data.append({
        "Name": bowler["name"],
        "Overs": bowler["overs"],
        "Maidens": bowler["maidens"],
        "Runs": bowler["runs"],
        "Wickets": bowler["wickets"],
        "Economy": bowler["economy"]
    })

bowler_df = pd.DataFrame(bowler_data)

st.dataframe(
    bowler_df,
    hide_index=True,
    width = "stretch"
)