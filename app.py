import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config & Professional UI
st.set_page_config(layout="wide", page_title="Santosh Pro Terminal", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    .trade-card { 
        background-color: #ffffff; border-radius: 12px; padding: 20px; 
        border-left: 10px solid #2ecc71; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .trade-sell { border-left-color: #e74c3c; }
    .action-btn { background: #2ecc71; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Engine (Restoring All Old Features)
def fetch_master_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    watch_list = ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "POWERGRID", "LT", "SBIN"]
    
    # Indices
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

    # Signals Logic (Mausam Nagpal Style)
    tickers = [t + ".NS" for t in watch_list]
    raw = yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)
    
    signals, bulls, bears = [], 0, 0
    for t in watch_list:
        try:
            df = raw[t + ".NS"].dropna()
            if df.empty: continue
            cmp = round(df['Close'].iloc[-1], 2)
            chg = round(((cmp - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100, 2)
            
            if chg > 0: bulls += 1
            else: bears += 1

            # Decision Logic: Kab Buy/Sell karna hai
            avg_v = df['Volume'].tail(20).mean()
            if df['Volume'].iloc[-1] > (avg_v * 1.5): # Volume Breakout Condition
                action = "BUY" if chg > 0 else "SELL"
                sl = round(cmp * 0.99, 1) if action == "BUY" else round(cmp * 1.01, 1)
                tgt = round(cmp * 1.02, 1) if action == "BUY" else round(cmp * 0.98, 1)
                signals.append({"S": t, "A": action, "C": cmp, "SL": sl, "T": tgt})
        except: continue
        
    return idx_res, signals, bulls, bears

# --- DISPLAY ---
idx_res, sig_res, bulls, bears = fetch_master_data()

# 1. Purana Top Index Bar
i_cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with i_cols[i]:
        st.markdown(f"<div class='index-card'><small>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# 2. Body: Left (Chart/Rockers) vs Right (Buy/Sell Guide)
col_left, col_right = st.columns([1.2, 1])

with col_left:
    # Rockers Count
    st.markdown(f"### Market Rockers: <span style='color:#2ecc71;'>{bulls} Up</span> | <span style='color:#e74c3c;'>{bears} Down</span>", unsafe_allow_html=True)
    
    # Index Mover Pie Chart
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=350, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("⚡ Kab Buy/Sell Karein?")
    if sig_res:
        for s in sig_res:
            s_class = "trade-sell" if s['A'] == "SELL" else ""
            st.markdown(f"""
                <div class='trade-card {s_class}'>
                    <span class='action-btn'>{s['A']} ALERT</span>
                    <h3 style='margin:10px 0;'>{s['S']} at {s['C']}</h3>
                    <p>🛡️ <b>Stop Loss:</b> <span style='color:#e74c3c;'>{s['SL']}</span></p>
                    <p>🎯 <b>Target:</b> <span style='color:#2ecc71;'>{s['T']}</span></p>
                    <small>Rule: Enter only if volume is confirmed 🔥</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Searching for breakouts... Wait for signal.")

time.sleep(60)
st.rerun()
