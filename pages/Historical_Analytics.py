import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

st.set_page_config(page_title="Historical Analytics", page_icon="📈", layout="wide")

st.title("📈 Historical Analytics")
st.markdown("Analyze stored cricket match data and synchronization statistics.")

# Sidebar Filters
st.sidebar.header("Filters")
format_filter = st.sidebar.selectbox("Match Format", options=["All", "T20", "ODI", "TEST"])
venue_id_filter = st.sidebar.number_input("Venue ID", min_value=0, value=0, step=1)

# Build query params
params = {}
if format_filter != "All":
    params["format"] = format_filter
if venue_id_filter > 0:
    params["venue_id"] = venue_id_filter

# Fetch Summary Data
@st.cache_data(ttl=60)
def fetch_summary(params):
    try:
        response = requests.get(f"{API_URL}/analytics/summary", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch analytics summary: {e}")
        return None

# Fetch Team Analytics Data
@st.cache_data(ttl=60)
def fetch_team_analytics():
    try:
        response = requests.get(f"{API_URL}/analytics/teams")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch team analytics: {e}")
        return []

summary_data = fetch_summary(params)

if summary_data:
    st.subheader("Key Performance Indicators (KPIs)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", summary_data.get("total_matches", 0))
    col2.metric("Total Teams", summary_data.get("total_teams", 0))
    col3.metric("Total Venues", summary_data.get("total_venues", 0))
    
    st.markdown("---")
    st.subheader("Sync Statistics")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Records Processed", summary_data.get("records_processed", 0))
    
    last_sync = summary_data.get("last_sync_time")
    if last_sync:
        # Basic formatting
        last_sync = last_sync.replace("T", " ")[:19]
    else:
        last_sync = "N/A"
        
    col5.metric("Last Sync Time", last_sync)
    
    avg_duration = summary_data.get("average_sync_duration")
    col6.metric("Avg Sync Duration", f"{avg_duration:.2f}s" if avg_duration is not None else "N/A")


st.markdown("---")
st.subheader("Team Analytics")

team_data = fetch_team_analytics()

if team_data:
    df = pd.DataFrame(team_data)
    
    # Display table
    st.dataframe(df, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            df.head(10), 
            x="team_name", 
            y="matches_played", 
            title="Top 10 Teams by Matches Played",
            labels={"team_name": "Team", "matches_played": "Matches Played"}
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        # Pie chart for top 10 percentage contribution
        fig2 = px.pie(
            df.head(10),
            names="team_name",
            values="percentage_contribution",
            title="Contribution Share (Top 10 Teams)",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No team analytics data available.")
