import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.caption("Real-Time Cricket Analytics Dashboard")

st.markdown("""
Welcome to **Cricbuzz LiveStats**, a real-time cricket analytics dashboard built using the Cricbuzz API.

This project allows users to:

- 📡 View live cricket matches
- 📋 Explore detailed match scorecards
- 📊 Analyze player statistics
- 🗄 Execute SQL analytics queries
- ✏ Perform CRUD operations on the database

Use the navigation panel on the left to explore each module.
""")

st.divider()

st.subheader("🚀 Project Features")

col1, col2 = st.columns(2)

with col1:
    st.success("📡 Live Match Details")
    st.success("📋 Match Scorecards")
    st.success("📊 Top Player Statistics")

with col2:
    st.success("🗄 SQL Analytics")
    st.success("✏ CRUD Operations")
    st.success("📈 Interactive Dashboard")

st.divider()

st.subheader("🛠 Tech Stack")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.info("🐍 Python")

with col2:
    st.info("🎈 Streamlit")

with col3:
    st.info("🌐 RapidAPI")

with col4:
    st.info("🐼 Pandas")

with col5:
    st.info("🗄 MySQL")

st.divider()

st.subheader("📈 Project Workflow")

st.markdown("""
📡 **Cricbuzz API**

⬇️

🐍 **Python Backend**

⬇️

📊 **Data Processing**

⬇️

🗄 **MySQL Database**

⬇️

🎈 **Streamlit Dashboard**
""")

st.divider()

st.caption(
    "Developed using Python, Streamlit, RapidAPI and MySQL | Cricbuzz LiveStats")