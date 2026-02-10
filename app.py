import streamlit as st
import time
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="SANTOSH TRADER PRO", layout="wide")

# Custom CSS for "Deep Red & Dark" Theme (Trading Professional)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .metric-card { background-color: #1a1c23; border: 1px solid #333; padding: 15px; border-radius: 10px; text-align: center; }
    .stButton>button { width: 100%; background-color: #ff3131; color: white; border-radius: 5px; }
    .buy-signal { color: #00ff00; font-weight: bold; }
    .sell-signal { color: #ff3131; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
t1, t2 = st.columns([3, 1])
with t1:
    st.title("🛡️ SANTOSH TRADER PRO (v1.0)")
with t2:
    st.markdown(f"### ⏰ {datetime.now().strftime('%H:%M:%S')}")

# --- SECTION 1: LIVE INDEX TRACKER ---
st.subheader("📊 Market Sentiment")
i1, i2, i3 = st.columns(3)
with i1:
    st.markdown("<div class='metric-card'><b>NIFTY 50</b><br><span style='font-size:24px;'>25,962.65</span><br><small style='color:#00ff00;'>PCR: 1.12 (Bullish)</small></div>", unsafe_allow_html=True)
with i2:
    st.markdown("<div class='metric-card'><b>BANK NIFTY</b><br><span style='font-size:24px;'>53,840.10</span><br><small style='color:#ff3131;'>PCR: 0.85 (Neutral)</small></div>", unsafe_allow_html=True)
with i3:
    st.markdown("<div class='metric-card'><b>SENSEX</b><br><span style='font-size:24px;'>85,120.45</span><br><small style='color:#00ff00;'>PCR: 1.15 (Bullish)</small></div>", unsafe_allow_html=True)

# --- SECTION 2: CHARTINK SNIPER LIST ---
st.markdown("---")
st.subheader("🚀 Chartink Breakout Sniper")
st.write("Scanning Market for Rocket Signals...")

# Table for Breakouts
data = [
    {"Stock": "BSE", "Signal": "BUY", "Entry": "3150", "SL": "3110", "Target": "3200+"},
    {"Stock": "JINDALSTEL", "Signal": "BUY", "Entry": "1180", "SL": "1165", "Target": "1220"},
    {"Stock": "M&M", "Signal": "BUY", "Entry": "2845", "SL": "2810", "Target": "2910"}
]

col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
col_h1.write("**STOCK**")
col_h2.write("**SIGNAL**")
col_h3.write("**ENTRY**")
col_h4.write("**SL**")
col_h5.write("**TARGET**")

for s in data:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.write(s["Stock"])
    c2.markdown(f"<span class='buy-signal'>{s['Signal']}</span>", unsafe_allow_html=True)
    c3.write(s["Entry"])
    c4.write(s["SL"])
    c5.write(s["Target"])

# --- FOOTER ---
st.markdown("---")
if st.button("🔄 FORCE REFRESH DATA"):
    st.rerun()
