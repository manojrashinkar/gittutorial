import streamlit as st
import pandas as pd
import google.generativeai as genai

# -------------------------------
# 1. Page Config
# -------------------------------
st.set_page_config(page_title="📊 Google Sheet + Gemini Assistant", layout="wide")
st.title("📊 Google Sheet Data + 🤖 Gemini Q&A")

# -------------------------------
# 2. Load Google Sheet
# -------------------------------
sheet_id = "1TYUWQmnerEHVyw7ykSIcmsfmb-3qaX4lghx9X9n6aJE"
gid = "0"  # assuming first sheet
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(sheet_url)
    st.success("✅ Google Sheet loaded successfully")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load sheet: {e}")
    st.stop()

# -------------------------------
# 3. Gemini Setup
# -------------------------------
genai.configure(api_key="AIzaSyDoDmENk9roAGwMECQG41fR0ua_7l88qC4")  # Store key in .streamlit/secrets.toml

model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro

# Convert small preview of sheet to text for context
sheet_preview = df.head(50).to_csv(index=False)  # limit to 50 rows to avoid long prompt

# -------------------------------
# 4. User Query to Gemini
# -------------------------------
st.subheader("🔍 Ask a Question about the Sheet")
user_query = st.text_input("Type your question:")

if user_query:
    with st.spinner("Thinking..."):
        prompt = f"""
        You are a data assistant. Answer the user's question based only on the data below:

        Sheet Data (CSV Preview):
        {sheet_preview}

        User Question: {user_query}
        """

        response = model.generate_content(prompt)
        st.write("### 🤖 Gemini Answer")
        st.write(response.text)
