import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Ultimate Dashboard", initial_sidebar_state="collapsed")

# Custom CSS for Professional Layout
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    .rocker-box { border: 1px solid #eee; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    .trade-alert-card { 
        background-color: #ffffff; border-radius: 10px; padding: 15px; 
        border-left: 8px solid #2ecc71; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; 
    }
    .trade-alert-sell { border-left-color: #e74c3c; }
    .vol-tag { background: #d1e7dd; color: #157347; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Advanced Data Logic (Indices + Multi-Signals + Volume)
@st.cache_data(ttl=60)
def fetch_master_dashboard_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    watch_list = ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "POWERGRID", "LT", "SBIN", "TATAMOTORS", "ADANIENT"]
    
    # A. Index Bar Results
    idx_res = []
    for name, sym in indices.items():
        try:
            d = yf.Ticker(sym).history(period="1d", interval="5m")
            if not d.empty:
                cmp, prev = round(d['Close'].iloc[-1], 2), d['Close'].iloc[-2]
                col = "#2ecc71" if cmp > prev else "#e74c3c"
                idx_res.append({"name": name, "cmp": cmp, "col": col})
        except: continue

    # B. Signals & Contributors
    tickers = [t + ".NS" for t in watch_list]
    raw = yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)
    signals, contributors, bulls, bears = [], [], 0, 0
    
    for t in watch_list:
        try:
            df = raw[t + ".NS"].dropna()
            if df.empty: continue
            cmp = round(df['Close'].iloc[-1], 2)
            chg = round(((cmp - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100, 2)
            
            # Volume Check
            avg_v, cur_v = df['Volume'].tail(20).mean(), df['Volume'].iloc[-1]
            vol_ok = True if cur_v > (avg_v * 1.5) else False
            
            if chg > 0: bulls += 1
            else: bears += 1
            contributors.append({"name": t, "chg": chg, "col": "#2ecc71" if chg > 0 else "#e74c3c"})

            # Signal Logic
            if abs(chg) > 0.1:
                side = "BUY" if chg > 0 else "SELL"
                sl = round(cmp * 0.99, 1) if side == "BUY" else round(cmp * 1.01, 1)
                t1 = round(cmp * 1.015, 1) if side == "BUY" else round(cmp * 0.985, 1)
                signals.append({"name": t, "side": side, "cmp": cmp, "sl": sl, "t1": t1, "vol": vol_ok})
        except: continue
        
    return idx_res, signals, sorted(contributors, key=lambda x: x['chg'], reverse=True), bulls, bears

# --- DASHBOARD DISPLAY ---
idx_data, signals, contributors, bulls, bears = fetch_master_dashboard_data()

# Header
st.markdown(f"<div style='display:flex; justify-content:space-between; padding:10px; border-bottom:2px solid #eee;'><b>SANTOSH TRADEX MASTER</b> <small>{datetime.now().strftime('%H:%M:%S')}</small></div>", unsafe_allow_html=True)

# 1. TOP INDEX BAR (Restore)
cols = st.columns(len(idx_data))
for i, x in enumerate(idx_data):
    with cols[i]:
        st.markdown(f"<div class='index-card'><small>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# 2. MARKET ROCKERS (Restore)
r1, r2, r3 = st.columns(3)
with r1: st.markdown(f"<div class='rocker-box' style='background:#f1f8f6;'><h2 style='color:#198754; margin:0;'>{bulls} Up</h2><small>Bullish Sentiment</small></div>", unsafe_allow_html=True)
with r2: st.markdown(f"<div class='rocker-box' style='background:#fff5f5;'><h2 style='color:#dc3545; margin:0;'>{bears} Down</h2><small>Bearish Pressure</small></div>", unsafe_allow_html=True)
with r3: st.markdown(f"<div class='rocker-box' style='background:#f8f9fa;'><h2 style='color:#333; margin:0;'>{bulls+bears} Scanned</h2><small>Total Stocks Scanned</small></div>", unsafe_allow_html=True)

# 3. MAIN CONTENT: Left (Pie + List) vs Right (Signals)
c_left, c_right = st.columns([1.2, 1])

with c_left:
    st.subheader("📊 Index Mover & Contributors") #
    fig = go.Figure(data=[go.Pie(labels=['Gainers', 'Losers'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=300, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    for c in contributors[:5]: # Top 5 Contributors
        st.markdown(f"<div style='display:flex; justify-content:space-between; padding:5px; border-bottom:1px solid #f5f5f5;'><span>{c['name']}</span><b style='color:{c['col']}'>{c['chg']}%</b></div>", unsafe_allow_html=True)

with c_right:
    st.subheader("🚀 Live Multi-Trade Alerts") #
    if signals:
        for s in signals[:4]: # Show top 4 signals
            s_class = "trade-alert-sell" if s['side'] == "SELL" else ""
            vol_html = "<span class='vol-tag'>VOL CONFIRMED</span>" if s['vol'] else ""
            st.markdown(f"""
                <div class='trade-alert-card {s_class}'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b>{s['side']} {s['name']}</b>
                        {vol_html}
                    </div>
                    <div style='margin-top:10px; font-size:14px;'>
                        <b>CMP: {s['cmp']}</b> | <span style='color:#e74c3c;'>SL: {s['sl']}</span> | <span style='color:#2ecc71;'>TGT: {s['t1']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Scanning for Volume Breakouts...")

time.sleep(60)
st.rerun()
