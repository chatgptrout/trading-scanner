import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Turbo Terminal", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { padding: 12px; border-radius: 8px; border: 1px solid #333; text-align: center; background-color: #111; margin-bottom: 10px; }
    .priority-high { color: white; background-color: #d32f2f; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 11px; }
    .priority-medium { color: black; background-color: #ffca28; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 11px; }
    .stTable td { font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Optimized Data Fetching (Caching for speed)
@st.cache_data(ttl=60)
def fetch_market_data(tickers):
    # Batch download for maximum speed
    return yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)

# 3. Watchlist (Nifty 100 + Commodities)
main_indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC", "HAL", "BEL", "TRENT", "ADANIENT", "POWERGRID"]

# --- APP LOGIC ---
st.title("📟 Santosh Turbo Command Center")
current_time = datetime.now().strftime('%H:%M:%S')
st.write(f"Turbo Mode Active | Last Sync: {current_time}")

# A. TOP BAR TREND CARDS
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

# B. DATA PROCESSING
all_tickers = [t + ".NS" for t in power_list]
raw_data = fetch_market_data(all_tickers)

signals, bulls, bears = [], 0, 0

for t in power_list:
    try:
        df = raw_data[t + ".NS"].dropna()
        if df.empty: continue
        h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
        prev_c = df['Close'].iloc[-2]
        
        # Breadth Count
        if cmp > prev_c: bulls += 1
        else: bears += 1
        
        # Power Filter Logic
        if cmp >= (h * 0.998) or cmp <= (l * 1.002):
            priority = "HIGH" if (cmp >= h or cmp <= l) else "MEDIUM"
            sig, lvl, color = ("BULLISH", f"ABOVE {h}", "#2ecc71") if cmp > (h+l)/2 else ("BEARISH", f"BELOW {l}", "#e74c3c")
            signals.append({"SCRIPT": t, "SIGNAL": sig, "LEVELS": lvl, "PRIORITY": priority, "COLOR": color})
    except: continue

# C. UI LAYOUT
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.subheader("Market Breadth") #
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Option Levels") #
    st.caption("NIFTY SENTIMENT")
    st.write("🎯 **PCR:** 0.92")
    st.write("🛡️ **Support:** 25650")

with col_right:
    st.subheader("🔥 Tradex Power Signals") #
    if signals:
        # Table Header
        h1, h2, h3, h4 = st.columns([1.5, 1, 2, 1])
        h1.write("**SCRIPT**"); h2.write("**SIGNAL**"); h3.write("**LEVELS**"); h4.write("**PRIORITY**")
        st.markdown("---")
        for s in signals:
            r1, r2, r3, r4 = st.columns([1.5, 1, 2, 1])
            r1.write(f"**{s['SCRIPT']}**")
            r2.markdown(f"<span style='color:{s['COLOR']}; font-weight:bold;'>SIGNAL</span>", unsafe_allow_html=True)
            r3.write(f"**{s['LEVELS']}**")
            p_class = "priority-high" if s['PRIORITY'] == "HIGH" else "priority-medium"
            r4.markdown(f"<span class='{p_class}'>{s['PRIORITY']}</span>", unsafe_allow_html=True)
    else:
        st.info("Searching for Action... No levels triggered in watchlist.")

# 4. Auto Refresh
time.sleep(60)
st.rerun()
