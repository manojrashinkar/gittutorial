import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Google Sheet Viewer", layout="wide")

st.title("📊 Google Sheet Data Viewer")

# Base Google Sheet URL (your sheet ID)
sheet_id = "1TYUWQmnerEHVyw7ykSIcmsfmb-3qaX4lghx9X9n6aJE"

# Define available sheet tabs (gid values) manually
# You can add more gids if your sheet has multiple tabs
sheets = {
    "Sheet1": "0",   # usually the first sheet is gid=0
    # "Sheet2": "123456789",  # example if you have other tabs
}

# Sidebar for sheet selection
sheet_name = st.sidebar.selectbox("Select Sheet Tab", list(sheets.keys()))
gid = sheets[sheet_name]

# Construct CSV export link
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Cached loader for better performance
@st.cache_data(ttl=60)  # refresh cache every 60 seconds
def load_data(url):
    return pd.read_csv(url)

# Load data
try:
    df = load_data(sheet_url)
    st.success(f"Loaded data from **{sheet_name}** ✅")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load Google Sheet: {e}")
