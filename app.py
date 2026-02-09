import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config (Full Width)
st.set_page_config(layout="wide", page_title="Santosh Final Master", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    .telegram-call {
        background-color: #ffffff; border-radius: 12px; padding: 15px; 
        border-left: 10px solid #2ecc71; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .call-header { color: #1c92d2; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Logic (Fetch everything together)
def fetch_complete_market_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    watch_list = ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "POWERGRID", "LT", "SBIN", "TATAMOTORS", "POWERINDIA"]
    
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

    tickers = [t + ".NS" if t != "POWERINDIA" else t for t in watch_list]
    raw = yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)
    
    contributors, bulls, bears = [], 0, 0
    for t in watch_list:
        try:
            name = t + ".NS" if t != "POWERINDIA" else t
            df = raw[name].dropna()
            if df.empty: continue
            cmp = df['Close'].iloc[-1]
            chg = round(((cmp - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100, 2)
            if chg > 0: bulls += 1
            else: bears += 1
            contributors.append({"name": t, "chg": chg, "col": "#2ecc71" if chg > 0 else "#e74c3c"})
        except: continue
        
    return idx_res, sorted(contributors, key=lambda x: x['chg'], reverse=True), bulls, bears

# --- DISPLAY ENGINE (Everything Restored) ---
idx_res, contributors, bulls, bears = fetch_complete_market_data()

# Header
st.markdown(f"### TRADEX LIVE | {datetime.now().strftime('%H:%M:%S')}")

# 1. TOP INDEX BAR (RESTORED)
i_cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with i_cols[i]:
        st.markdown(f"<div class='index-card'><small>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# 2. MAIN BODY
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown(f"### Market Mood: <span style='color:#2ecc71;'>{bulls} Up</span> | <span style='color:#e74c3c;'>{bears} Down</span>", unsafe_allow_html=True)
    
    # RESTORED Pie Chart
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=350, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    # RESTORED Contributor List
    st.write("**Top Contributors**")
    for c in contributors[:6]:
        st.markdown(f"<div style='display:flex; justify-content:space-between; border-bottom:1px solid #eee; padding:5px;'><span>{c['name']}</span><b style='color:{c['col']}'>{c['chg']}%</b></div>", unsafe_allow_html=True)

with col_right:
    st.subheader("🔥 Live Pro Calls")
    
    # Example Call Logic (Restored & Integrated)
    if contributors:
        top_s = contributors[0]
        st.markdown(f"""
            <div class='telegram-call'>
                <div class='call-header'>Mausam Nagpal Ⓡ</div>
                <div style='font-weight:bold; font-size:16px;'>Buy {top_s['name']} Option</div>
                <div style='margin:5px 0;'>Cmp {top_s['chg']}% Breakout</div>
                <div style='color:#e74c3c; font-weight:bold;'>Sl: Trail below Level</div>
                <div style='color:#2ecc71; font-weight:bold;'>Target: OPEN 🎯</div>
                <hr>
                <small style='color:#888;'>Call generated via Santosh Turbo Strategy</small>
            </div>
            """, unsafe_allow_html=True)

time.sleep(60)
st.rerun()
