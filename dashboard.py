import streamlit as st
import time

st.set_page_config(page_title="📈 Breakout Dashboard", layout="wide")

st.title("📊 Daily Breakout Stock Report")

# Auto-refresh every 5 minutes (300 seconds)
countdown = 300  # 5 minutes
st_autorefresh = st.experimental_rerun if 'autorefresh' in st.session_state else None

if 'last_refreshed' not in st.session_state:
    st.session_state.last_refreshed = time.time()

if time.time() - st.session_state.last_refreshed > countdown:
    st.session_state.last_refreshed = time.time()
    st.experimental_rerun()

# Display HTML report
try:
    with open("index.html", "r", encoding="utf-8") as file:
        html = file.read()
    st.components.v1.html(html, height=900, scrolling=True)
except FileNotFoundError:
    st.error("HTML report not found. Please generate it first.")
