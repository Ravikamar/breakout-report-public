import streamlit as st
import pandas as pd
import requests
import time

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="BreakoutPulse", page_icon="📈", layout="wide")

# -----------------------
# Header
# -----------------------
st.markdown("""
    <h1 style='text-align: center;'>📈 BreakoutPulse - Live Breakout Tracker</h1>
    <p style='text-align: center; font-size: 18px; color: gray;'>Tracking potential stock breakouts every 5 minutes, live from the Indian stock market. All times shown in IST.</p>
""", unsafe_allow_html=True)

# -----------------------
# Fetch JSON from GitHub
# -----------------------
@st.cache_data(ttl=10)  # Automatically refresh data every 10 seconds
def load_data():
    url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/breakout_stocks.json"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to fetch data.")
        return pd.DataFrame()

df = load_data()

# -----------------------
# Show Summary Metrics
# -----------------------
if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Breakouts", len(df))
    col2.metric("Top Score", df["score"].max())
    col3.metric("Top Gap %", f"{df['gap_pct'].max():.2f}%")

    # -----------------------
    # Table Display
    # -----------------------
    st.markdown("### 📊 Breakout Details")
    df["symbol"] = df["symbol"].str.replace(r'<[^>]*>', '', regex=True)  # Remove HTML tags if any
    st.dataframe(df[[
        "symbol", "breakout_time", "type", "high_9_15", "low_9_15", 
        "ltp_at_breakout", "volume", "score", "gap_pct", "datr"
    ]])
else:
    st.info("Waiting for live breakout data...")

# -----------------------
# Footer (Optional)
# -----------------------
st.markdown("""
    <hr>
    <div style='text-align:center'>
        Built with ❤️ by <b>BreakoutPulse</b> team • Auto-refresh every 10 seconds
    </div>
""", unsafe_allow_html=True)
