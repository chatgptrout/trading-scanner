import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Index Mover Pro", initial_sidebar_state="collapsed")

# Professional White UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .tradex-header { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px; display: flex; justify-content: space-between; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    .contributor-item { display: flex; justify-content: space-between; padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 13px; border-left: 4px solid #eee; }
    .rocker-box { border: 1px solid #eee; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Logic
@st.cache_data(ttl=60)
def fetch_master_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    # Top 10 heavyweights for Index Mover logic
    heavyweights = ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "ITC", "AXISBANK", "LT", "SBIN", "BHARTIARTL"]
    
    # A. Index Bar
    idx_res = []
    for name, sym in indices.items():
        try:
            d = yf.Ticker(sym).history(period="1d", interval="5m")
            if not d.empty:
                cmp = round(d['Close'].iloc[-1], 2)
                prev = d['Close'].iloc[-2]
                col = "#2ecc71" if cmp > prev else "#e74c3c"
                idx_res.append({"name": name, "cmp": cmp, "col": col})
        except: continue

    # B. Contributors & Rockers
    tickers = [t + ".NS" for t in heavyweights]
    raw = yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)
    
    contributors, bulls, bears = [], 0, 0
    for t in heavyweights:
        try:
            df = raw[t + ".NS"].dropna()
            if df.empty: continue
            cmp = df['Close'].iloc[-1]
            chg = round(((cmp - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100, 2)
            if chg > 0: bulls += 1
            else: bears += 1
            contributors.append({"name": t, "chg": chg, "col": "#2ecc71" if chg > 0 else "#e74c3c"})
        except: continue
    
    return idx_res, sorted(contributors, key=lambda x: x['chg'], reverse=True), bulls, bears

# --- DISPLAY ---
idx_res, contributors, bulls, bears = fetch_master_data()

st.markdown(f"<div class='tradex-header'><div><b>TRADEX</b> <span style='background:#ff4b4b; color:white; padding:2px 8px; border-radius:4px;'>LIVE</span></div><div>{datetime.now().strftime('%H:%M:%S')}</div></div>", unsafe_allow_html=True)

# 1. RESTORED Index Bar
i_cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with i_cols[i]:
        st.markdown(f"<div class='index-card'><small style='color:#888'>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# 2. Market Rockers
r1, r2, r3 = st.columns(3)
with r1: st.markdown(f"<div class='rocker-box' style='background:#f1f8f6;'><h2 style='color:#198754; margin:0;'>{bulls} Up</h2><small>Bullish Sentiment</small></div>", unsafe_allow_html=True)
with r2: st.markdown(f"<div class='rocker-box' style='background:#fff5f5;'><h2 style='color:#dc3545; margin:0;'>{bears} Down</h2><small>Bearish Pressure</small></div>", unsafe_allow_html=True)
with r3: st.markdown(f"<div class='rocker-box' style='background:#f8f9fa;'><h2 style='color:#333; margin:0;'>{bulls+bears} Scanned</h2><small>Market Rockers Live</small></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Index Mover & Contributors Section
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📊 Index Mover (Nifty)")
    if (bulls+bears) > 0:
        fig = go.Figure(data=[go.Pie(labels=['Gainers', 'Losers'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=350, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Top Contributors")
    for c in contributors:
        border_col = c['col']
        st.markdown(f"""
            <div class='contributor-item' style='border-left-color:{border_col};'>
                <span><b>{c['name']}</b></span>
                <span style='color:{c['col']}; font-weight:bold;'>{'+' if c['chg'] > 0 else ''}{c['chg']}%</span>
            </div>
            """, unsafe_allow_html=True)

time.sleep(60)
st.rerun()
