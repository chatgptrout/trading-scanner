import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Triple Terminal", initial_sidebar_state="collapsed")

# Professional UI Styling (Nagpal Style for all)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .nagpal-card {
        background-color: #ffffff; border-radius: 12px; padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;
        border-left: 10px solid #2ecc71;
    }
    .stock-card { border-left-color: #2ecc71; }
    .option-card { border-left-color: #1c92d2; }
    .comm-card { border-left-color: #f39c12; }
    .tgt-text { color: #2ecc71; font-weight: bold; }
    .sl-text { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for Triple Calls
def get_all_market_calls():
    return {
        "stock": {"name": "POWERINDIA", "type": "Cash-Buy", "entry": "22745", "tgt": "23050", "sl": "22350"},
        "option": {"name": "NIFTY 22500 CE", "type": "Option-Buy", "entry": "145 - 150", "tgt": "210", "sl": "110"},
        "commodity": {"name": "CRUDEOILM 17FEB 5700 CE", "type": "Comm-Buy", "entry": "190 - 192", "tgt": "233", "sl": "163"}
    }

# --- DISPLAY ENGINE ---
calls = get_all_market_calls()

# A. TOP: INDICES BAR (Restored)
st.markdown(f"### 🚀 SANTOSH ALL-IN-ONE | {datetime.now().strftime('%H:%M:%S')}")
st.write("NIFTY: 22450 | BANKNIFTY: 47800 | CRUDE: 63.50 | GOLD: 5040")

st.markdown("---")

# B. MIDDLE: TRIPLE CALLS (Upar se Niche)
st.subheader("📢 Live Pro-Signals (All Markets)")

# 1. STOCK CALL
st.markdown(f"""
    <div class='nagpal-card stock-card'>
        <div style='color:#2ecc71; font-weight:bold;'>⭐ STOCK CASH CALL ⭐</div>
        <div style='font-size:20px; font-weight:bold;'>📈 {calls['stock']['name']} ({calls['stock']['type']})</div>
        <b>Entry:</b> ₹ {calls['stock']['entry']} | <span class='tgt-text'>Tgt: {calls['stock']['tgt']}</span> | <span class='sl-text'>SL: {calls['stock']['sl']}</span>
    </div>
    """, unsafe_allow_html=True)

# 2. OPTION CALL
st.markdown(f"""
    <div class='nagpal-card option-card'>
        <div style='color:#1c92d2; font-weight:bold;'>⭐ OPTION PREMIUM CALL ⭐</div>
        <div style='font-size:20px; font-weight:bold;'>📈 {calls['option']['name']} ({calls['option']['type']})</div>
        <b>Entry:</b> ₹ {calls['option']['entry']} | <span class='tgt-text'>Tgt: {calls['option']['tgt']}</span> | <span class='sl-text'>SL: {calls['option']['sl']}</span>
    </div>
    """, unsafe_allow_html=True)

# 3. COMMODITY CALL
st.markdown(f"""
    <div class='nagpal-card comm-card'>
        <div style='color:#f39c12; font-weight:bold;'>⭐ COMMODITY SPECIAL CALL ⭐</div>
        <div style='font-size:20px; font-weight:bold;'>📈 {calls['commodity']['name']} ({calls['commodity']['type']})</div>
        <b>Entry:</b> ₹ {calls['commodity']['entry']} | <span class='tgt-text'>Tgt: {calls['commodity']['tgt']}</span> | <span class='sl-text'>SL: {calls['commodity']['sl']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# C. BOTTOM: SENTIMENT & PIE CHART (Restored)
col_l, col_r = st.columns(2)
with col_l:
    st.write("#### Market Mood Meter")
    fig = go.Figure(data=[go.Pie(labels=['Bullish', 'Bearish'], values=[7, 3], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.write("**Quick Logic:** Teeno markets ke best calls ab aapke samne line se hain. Nifty band hone ke baad bhi Commodity call raat tak chalta rahega.")

time.sleep(60)
st.rerun()
