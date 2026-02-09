import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Tradex Live", initial_sidebar_state="collapsed")

# Professional UI Styling (Based on your images)
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; color: #333; }
    .index-card { background-color: #ffffff; border: 1px solid #ddd; padding: 10px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .nagpal-card {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 25px;
        border-left: 12px solid #2ecc71;
    }
    .stock-card { border-left-color: #2ecc71; }
    .option-card { border-left-color: #1c92d2; }
    .comm-card { border-left-color: #f39c12; }
    .call-label { font-size: 14px; font-weight: bold; color: #888; text-transform: uppercase; }
    .strike-title { font-size: 24px; font-weight: bold; margin: 10px 0; color: #222; }
    .entry-box { background: #f9f9f9; padding: 10px; border-radius: 8px; border: 1px dashed #ccc; font-size: 18px; font-weight: bold; display: inline-block; }
    .tgt-text { color: #2ecc71; font-weight: bold; font-size: 20px; }
    .sl-text { color: #e74c3c; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Advanced Data Logic
@st.cache_data(ttl=60)
def fetch_all_market_signals():
    # Indices Data
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    idx_data = []
    for name, sym in indices.items():
        try:
            d = yf.Ticker(sym).history(period="1d", interval="5m")
            if not d.empty:
                idx_data.append({"name": name, "cmp": round(d['Close'].iloc[-1], 2)})
        except: continue

    # Mock signals following Mausam Nagpal patterns
    calls = {
        "stock": {"name": "POWERINDIA", "entry": "22780", "sl": "22350", "tgt": "23200"},
        "option": {"name": "NIFTY 22500 CE", "entry": "148", "sl": "115", "tgt": "220"},
        "commodity": {"name": "CRUDEOILM 17FEB 5700 CE", "entry": "195 - 200", "sl": "163", "tgt": "240"}
    }
    return idx_data, calls

# --- DISPLAY ENGINE ---
idx_res, calls = fetch_all_market_signals()

# Header Section
st.markdown(f"### 🛡️ SANTOSH TRADEX LIVE | {datetime.now().strftime('%H:%M:%S')}")

# 1. TOP BAR: LIVE INDICES
i_cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with i_cols[i]:
        st.markdown(f"<div class='index-card'><small>{x['name']}</small><h4 style='margin:0;'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# 2. MAIN TRIPLE TOWER CALLS (Upar se Niche)
st.subheader("📢 Live Pro-Signals (All Markets)")

# A. STOCK CASH CALL
st.markdown(f"""
    <div class='nagpal-card stock-card'>
        <div class='call-label'>⭐ Stock Cash Call</div>
        <div class='strike-title'>🚀 BUY {calls['stock']['name']}</div>
        <div class='entry-box'>ENTRY ABOVE: ₹{calls['stock']['entry']}</div>
        <div style='margin-top:15px;'>
            <span class='sl-text'>🛑 STOP LOSS: {calls['stock']['sl']}</span> | 
            <span class='tgt-text'>🎯 TARGET: {calls['stock']['tgt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# B. OPTION PREMIUM CALL
st.markdown(f"""
    <div class='nagpal-card option-card'>
        <div class='call-label' style='color:#1c92d2;'>⭐ Option Premium Call</div>
        <div class='strike-title' style='color:#1c92d2;'>🚀 BUY {calls['option']['name']}</div>
        <div class='entry-box'>ENTRY ABOVE: ₹{calls['option']['entry']}</div>
        <div style='margin-top:15px;'>
            <span class='sl-text'>🛑 STOP LOSS: {calls['option']['sl']}</span> | 
            <span class='tgt-text' style='color:#1c92d2;'>🎯 TARGET: {calls['option']['tgt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# C. COMMODITY SPECIAL CALL
st.markdown(f"""
    <div class='nagpal-card comm-card'>
        <div class='call-label' style='color:#f39c12;'>⭐ Commodity Special Call</div>
        <div class='strike-title' style='color:#f39c12;'>🚀 BUY {calls['commodity']['name']}</div>
        <div class='entry-box'>ENTRY RANGE: ₹{calls['commodity']['entry']}</div>
        <div style='margin-top:15px;'>
            <span class='sl-text'>🛑 STOP LOSS: {calls['commodity']['sl']}</span> | 
            <span class='tgt-text' style='color:#f39c12;'>🎯 TARGET: {calls['commodity']['tgt']}</span>
        </div>
        <hr>
        <small style='color:#888;'>Commodity Market is LIVE till 11:30 PM ✔️</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 3. BOTTOM: MARKET MOOD (RESTORED)
st.subheader("📊 Market Sentiment")
col_l, col_r = st.columns(2)
with col_l:
    fig = go.Figure(data=[go.Pie(labels=['Bullish', 'Bearish'], values=[7, 3], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.write("**Top Contributors:**")
    st.write("RELIANCE: +0.12% | TCS: +0.1% | HDFCBANK: +0.08%")

time.sleep(10) # Fast refresh for live market
st.rerun()
