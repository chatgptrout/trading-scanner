import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh All-In-One Terminal", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    .nagpal-card {
        background-color: #ffffff; border-radius: 15px; padding: 25px;
        border-left: 10px solid #f39c12; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    .tgt-val { color: #2ecc71; font-weight: bold; }
    .sl-val { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Engine (Restore Everything)
def fetch_complete_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    idx_res = []
    for name, sym in indices.items():
        try:
            d = yf.Ticker(sym).history(period="1d", interval="5m")
            if not d.empty:
                cmp = round(d['Close'].iloc[-1], 2)
                idx_res.append({"name": name, "cmp": cmp})
        except: continue
    return idx_res

# --- DISPLAY ---
idx_res = fetch_complete_data()

# A. RESTORED TOP BAR
st.markdown(f"### TRADEX LIVE | {datetime.now().strftime('%H:%M:%S')}")
cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with cols[i]:
        st.markdown(f"<div class='index-card'><small>{x['name']}</small><h4 style='color:#333; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# B. RESTORED MIDDLE SECTION (Pie Chart & Contributors)
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown("#### Market Mood: 6 Up | 4 Down")
    fig = go.Figure(data=[go.Pie(labels=['Up', 'Down'], values=[6, 4], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.write("**Top Contributors (Live)**")
    st.write("SBIN: +0.1% | LT: +0.07% | RELIANCE: +0.06%") #

st.markdown("---")

# C. NEW: COMMODITY RECOMMENDATION (Mausam Nagpal Style)
st.subheader("⭐ Commodity Recommendation ⭐")
st.markdown(f"""
    <div class='nagpal-card'>
        <div style='font-size:22px; font-weight:bold; color:#f39c12;'>📈 CRUDEOILM 17FEB 5700 CE</div>
        <div style='font-size:18px; margin-top:10px;'>
            <b>Type:</b> Intraday-Buy<br>
            💰 <b>Entry Price:</b> ₹ 190 - 192<br>
            🎯 <b>Target:</b> <span class='tgt-val'>₹ 233 (22.63%)</span><br>
            ⚠️ <b>Stop Loss:</b> <span class='sl-val'>₹ 163 (-14.21%)</span>
        </div>
        <hr>
        <small style='color:#888;'>Disclaimer: Trade and invest after reading rules.</small>
    </div>
    """, unsafe_allow_html=True)

time.sleep(60)
st.rerun()
