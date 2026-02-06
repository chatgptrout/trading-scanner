import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Ultimate Turbo", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { padding: 12px; border-radius: 8px; border: 1px solid #333; text-align: center; background-color: #111; margin-bottom: 10px; }
    .priority-medium { color: black; background-color: #ffca28; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 11px; }
    .portfolio-box { background-color: #0d1117; padding: 20px; border-radius: 10px; border: 1px solid #30363d; margin-top: 25px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Turbo Data Fetching (Cached)
@st.cache_data(ttl=60)
def fetch_turbo_data(tickers):
    return yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)

# Watchlists
main_indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
power_watchlist = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERGRID", "DLF", "GNFC"]

# --- APP LAYOUT ---
st.title("📟 Santosh Turbo Command Center")
st.write(f"Turbo Mode Active | Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# A. TOP BAR CARDS
top_cols = st.columns(len(main_indices))
for i, (name, sym) in enumerate(main_indices.items()):
    try:
        idx_data = yf.Ticker(sym).history(period="1d", interval="5m")
        if not idx_data.empty:
            cmp = round(idx_data['Close'].iloc[-1], 2)
            prev = idx_data['Close'].iloc[-2]
            status, col = ("BULLISH", "#2ecc71") if cmp > prev else ("BEARISH", "#e74c3c")
            with top_cols[i]:
                st.markdown(f"<div class='signal-card'><small>{name}</small><h3 style='color:{col}; margin:5px 0;'>{status}</h3><b>{cmp}</b></div>", unsafe_allow_html=True)
    except: continue

st.markdown("---")

# B. DATA ENGINE
all_tickers = [t + ".NS" for t in power_watchlist]
raw_data = fetch_turbo_data(all_tickers)
signals, bulls, bears = [], 0, 0

for t in power_watchlist:
    try:
        df = raw_data[t + ".NS"].dropna()
        if df.empty: continue
        h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
        if cmp > df['Close'].iloc[-2]: bulls += 1
        else: bears += 1
        
        # Tradex Power Logic
        if cmp >= (h * 0.998) or cmp <= (l * 1.002):
            prio = "MEDIUM" # Logic based on proximity
            sig, color = ("SIGNAL", "#2ecc71") if cmp > (h+l)/2 else ("SIGNAL", "#e74c3c")
            signals.append({"S": t, "SIG": sig, "L": f"ABOVE {h}" if cmp > (h+l)/2 else f"BELOW {l}", "P": prio, "C": color})
    except: continue

# C. MAIN DISPLAY
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.subheader("Market Breadth") #
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Portfolio Tracker Segment
    st.markdown("<div class='portfolio-box'><h4>💼 Motilal Portfolio</h4><p style='font-size:13px;'>Live Equity Value Tracking...</p><h2 style='color:#2ecc71;'>₹ 1,45,200</h2><small>+2.4% Today</small></div>", unsafe_allow_html=True)

with col_right:
    st.subheader("🔥 Tradex Power Signals") #
    if signals:
        h1, h2, h3, h4 = st.columns([1.5, 1, 2, 1])
        h1.write("**SCRIPT**"); h2.write("**SIGNAL**"); h3.write("**LEVELS**"); h4.write("**PRIORITY**")
        st.markdown("---")
        for s in signals:
            r1, r2, r3, r4 = st.columns([1.5, 1, 2, 1])
            r1.write(f"**{s['S']}**")
            r2.markdown(f"<span style='color:{s['C']}; font-weight:bold;'>{s['SIG']}</span>", unsafe_allow_html=True)
            r3.write(f"**{s['L']}**")
            r4.markdown(f"<span class='priority-medium'>{s['P']}</span>", unsafe_allow_html=True)
    else: st.info("Scanning for Power Breakouts...")

time.sleep(60)
st.rerun()
