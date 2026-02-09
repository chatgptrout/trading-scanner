import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Ultimate Signal", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .call-box {
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center;
    }
    .stock-box { background-color: #f1f8f6; border: 2px solid #2ecc71; }
    .option-box { background-color: #f0f7ff; border: 2px solid #1c92d2; }
    .label { font-size: 14px; color: #666; font-weight: bold; }
    .value { font-size: 20px; font-weight: bold; color: #333; }
    .buy-btn { background: #2ecc71; color: white; padding: 2px 10px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for Both Calls
def get_master_calls():
    # A. Stock Cash Call
    stock_p = 22700.0  # Powerindia Example
    # B. Option Premium Call
    opt_p = 760.0      # Premium Price Example
    
    return {
        "stock": {"name": "POWERINDIA", "entry": 22745, "sl": 22350, "tgt": 23050},
        "option": {"name": "POWERINDIA 22500 CE", "entry": 780, "sl": 600, "tgt": 950}
    }

# --- DISPLAY ---
calls = get_master_calls()

# A. TOP SECTION: CLEAR CALLS
st.markdown("### 🚀 Live Trading Signals (Stock + Option)")
c_stock, c_opt = st.columns(2)

with c_stock:
    st.markdown(f"""
        <div class='call-box stock-box'>
            <div class='buy-btn'>STOCK CASH</div>
            <div style='font-size:22px; font-weight:bold; margin:10px 0;'>BUY {calls['stock']['name']}</div>
            <div class='label'>ENTRY ABOVE: <span class='value'>₹{calls['stock']['entry']}</span></div>
            <div class='label'>STOP LOSS: <span class='value' style='color:#e74c3c;'>₹{calls['stock']['sl']}</span></div>
            <div class='label'>TARGET: <span class='value' style='color:#2ecc71;'>₹{calls['stock']['tgt']}</span></div>
        </div>
        """, unsafe_allow_html=True)

with c_opt:
    st.markdown(f"""
        <div class='call-box option-box'>
            <div class='buy-btn' style='background:#1c92d2;'>OPTION PREMIUM</div>
            <div style='font-size:22px; font-weight:bold; margin:10px 0;'>BUY {calls['option']['name']}</div>
            <div class='label'>ENTRY ABOVE: <span class='value'>₹{calls['option']['entry']}</span></div>
            <div class='label'>STOP LOSS: <span class='value' style='color:#e74c3c;'>₹{calls['option']['sl']}</span></div>
            <div class='label'>TARGET: <span class='value' style='color:#2ecc71;'>₹{calls['option']['tgt']}</span></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# B. BOTTOM SECTION: OLD DASHBOARD (RESTORED)
st.subheader("📊 Market Sentiment")
col_l, col_r = st.columns([1, 1])
with col_l:
    st.write("### Market Mood: 6 Up | 2 Down")
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[6, 2], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.write("**Quick Check:** Sabse upar Stock aur Option dono ki clear levels hain. Pehle Stock level check karein, fir Option premium mein entry lein.")

time.sleep(60)
st.rerun()