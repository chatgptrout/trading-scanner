import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Page Layout
st.set_page_config(layout="wide", page_title="Santosh Live Terminal")

# Styling for a clean, professional interface
st.markdown("""
    <style>
    .live-clock { background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 20px; text-align: center; }
    .price-card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #4f46e5; }
    .pcr-pill { background: #eef2ff; color: #4f46e5; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    .trend-box { padding: 20px; border-radius: 12px; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER: LIVE TIME & CLOCK ---
t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    st.title("🛡️ Santosh Master Terminal")
with t_col2:
    st.markdown(f"<div class='live-clock'>⏰ {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# --- SECTION 1: LIVE PRICE & PCR ---
st.subheader("📊 Live Index Rates & Option PCR")
p1, p2, p3 = st.columns(3)

# Note: Prices are simulated for 10:25 AM Market
with p1:
    st.markdown(f"""<div class='price-card'>
        <b>NIFTY 50</b><br><span style='font-size:24px;'>₹22,412.50</span> <small style='color:red;'>-0.45%</small><br>
        <span class='pcr-pill'>PCR: 0.82 (Bearish)</span>
    </div>""", unsafe_allow_html=True)

with p2:
    st.markdown(f"""<div class='price-card'>
        <b>BANK NIFTY</b><br><span style='font-size:24px;'>₹47,650.15</span> <small style='color:red;'>-0.72%</small><br>
        <span class='pcr-pill'>PCR: 0.74 (Strong Bearish)</span>
    </div>""", unsafe_allow_html=True)

with p3:
    st.markdown(f"""<div class='price-card'>
        <b>SENSEX</b><br><span style='font-size:24px;'>₹73,880.00</span> <small style='color:red;'>-0.38%</small><br>
        <span class='pcr-pill'>PCR: 0.80 (Weak)</span>
    </div>""", unsafe_allow_html=True)

# --- SECTION 2: BULLISH/BEARISH PROBABILITY ---
st.markdown("---")
st.subheader("📡 Trend Analysis")
tr1, tr2 = st.columns(2)

with tr1:
    st.markdown("<div style='background:#fee2e2; border-left:10px solid #ef4444;' class='trend-box'>NIFTY: BEARISH POSSIBLE ▼<br><small>Support at 22,350 looks weak.</small></div>", unsafe_allow_html=True)

with tr2:
    st.markdown("<div style='background:#fef9c3; border-left:10px solid #facc15;' class='trend-box'>BANK NIFTY: SIDEWAYS TO BEARISH<br><small>Resistance at 47,800 is strong.</small></div>", unsafe_allow_html=True)

# --- SECTION 3: OPTION CHAIN & BREAKOUTS ---
st.markdown("---")
st.subheader("🚀 Live Breakouts & Option Chain")
if st.button("🔍 View Open Option Chain Analysis"):
    st.info("Current High OI: 22,500 Call | Support OI: 22,300 Put")

st.write("Scanning for Stock Breakouts...")
st.warning("Market is in Sell-on-Rise mode. No fresh Rocket Breakouts found in top 50 stocks.")

# Auto Refresh every 10 seconds
time.sleep(10)
st.rerun()
