import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh All-Market Terminal", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .call-box { border-radius: 12px; padding: 15px; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .stock-box { background-color: #f1f8f6; border: 2px solid #2ecc71; }
    .option-box { background-color: #f0f7ff; border: 2px solid #1c92d2; }
    .commodity-box { background-color: #fffaf0; border: 2px solid #f39c12; }
    .label { font-size: 13px; color: #666; font-weight: bold; }
    .value { font-size: 18px; font-weight: bold; color: #333; }
    .header-tag { color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-bottom: 10px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for All Markets
def get_all_calls():
    # Example Levels
    return {
        "stock": {"name": "POWERINDIA", "entry": 22745, "sl": 22350, "tgt": 23050},
        "option": {"name": "POWERINDIA 22500 CE", "entry": 780, "sl": 600, "tgt": 950},
        "commodity": {"name": "CRUDE OIL", "entry": 63.50, "sl": 62.10, "tgt": 65.00} #
    }

# --- DISPLAY ENGINE ---
calls = get_all_calls()

# Header
st.markdown(f"### 🚀 SANTOSH MASTER SIGNALS | {datetime.now().strftime('%H:%M:%S')}")

# A. EQUITY & OPTIONS SECTION
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='call-box stock-box'><span class='header-tag' style='background:#2ecc71;'>STOCK CASH</span><br><b>BUY {calls['stock']['name']}</b><br><span class='label'>ABOVE:</span> <span class='value'>{calls['stock']['entry']}</span><br><span class='label'>SL:</span> <span class='value' style='color:#e74c3c;'>{calls['stock']['sl']}</span> | <span class='label'>TGT:</span> <span class='value' style='color:#2ecc71;'>{calls['stock']['tgt']}</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='call-box option-box'><span class='header-tag' style='background:#1c92d2;'>OPTION PREMIUM</span><br><b>BUY {calls['option']['name']}</b><br><span class='label'>ABOVE:</span> <span class='value'>{calls['option']['entry']}</span><br><span class='label'>SL:</span> <span class='value' style='color:#e74c3c;'>{calls['option']['sl']}</span> | <span class='label'>TGT:</span> <span class='value' style='color:#2ecc71;'>{calls['option']['tgt']}</span></div>", unsafe_allow_html=True)

# B. COMMODITY SECTION (NEW)
st.markdown("---")
st.subheader("🔥 Live Commodity Signals")
c_comm = st.columns(1)[0]
with c_comm:
    st.markdown(f"""
        <div class='call-box commodity-box'>
            <span class='header-tag' style='background:#f39c12;'>COMMODITY (CRUDE/GOLD/SILVER)</span>
            <div style='font-size:22px; font-weight:bold; margin:10px 0;'>BUY {calls['commodity']['name']}</div>
            <div style='display:flex; justify-content:center; gap:20px;'>
                <div><span class='label'>ENTRY ABOVE:</span> <span class='value'>${calls['commodity']['entry']}</span></div>
                <div><span class='label'>STOP LOSS:</span> <span class='value' style='color:#e74c3c;'>${calls['commodity']['sl']}</span></div>
                <div><span class='label'>TARGET:</span> <span class='value' style='color:#2ecc71;'>${calls['commodity']['tgt']}</span></div>
            </div>
            <small style='color:#888; margin-top:10px; display:block;'>Commodity Market is LIVE until 11:30 PM ✔️</small>
        </div>
        """, unsafe_allow_html=True)

# C. PURANA DATA (Back-up)
st.markdown("---")
col_l, col_r = st.columns([1, 1])
with col_l:
    st.write("### Market Mood & Rockers") #
    fig = go.Figure(data=[go.Pie(labels=['Up', 'Down'], values=[6, 4], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.write("**Top Indices Bar (Live):**")
    st.write("CRUDE OIL: 62.94 | GOLD: 5039.4 | SILVER: 81.5") #

time.sleep(60)
st.rerun()
