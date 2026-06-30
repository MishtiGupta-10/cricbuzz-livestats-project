import streamlit as st
import requests

st.set_page_config(page_title="Admin Dashboard", page_icon="⚙️", layout="wide")

st.title("⚙️ Admin Dashboard - Data Sync Engine")
st.caption("Manage and monitor the background synchronization engine")

API_BASE = "http://localhost:8000/api/v1/sync"

def run_manual_sync():
    try:
        response = requests.post(f"{API_BASE}/run", timeout=30)
        if response.status_code == 200:
            st.success("Manual sync completed successfully!")
            st.json(response.json())
        elif response.status_code == 409:
            st.warning("A sync job is already running in the background.")
        else:
            st.error(f"Error triggering sync: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")

col1, col2 = st.columns(2)

# Get status
with col1:
    st.subheader("Sync Status")
    try:
        status_res = requests.get(f"{API_BASE}/status")
        if status_res.status_code == 200:
            status = status_res.json()
            st.metric("Scheduler Running", str(status.get("scheduler_running", False)))
            st.metric("Interval (Minutes)", status.get("interval_minutes", "N/A"))
            st.metric("Job Currently Running", str(status.get("job_running", False)))
        else:
            st.error("Failed to fetch status.")
    except Exception as e:
        st.error(f"Status Error: {e}")
        
    st.button("Trigger Manual Sync", on_click=run_manual_sync)

with col2:
    st.subheader("Stored Matches Overview")
    try:
        matches_res = requests.get("http://localhost:8000/api/v1/matches/stored")
        if matches_res.status_code == 200:
            matches = matches_res.json()
            st.metric("Total Matches Stored", len(matches))
            if len(matches) > 0:
                st.dataframe(matches)
    except Exception as e:
        st.error(f"Matches Error: {e}")

st.divider()

st.subheader("Recent Sync History")
try:
    history_res = requests.get(f"{API_BASE}/history")
    if history_res.status_code == 200:
        history = history_res.json()
        if history:
            st.table(history)
        else:
            st.info("No sync history found.")
except Exception as e:
    st.error(f"History Error: {e}")
