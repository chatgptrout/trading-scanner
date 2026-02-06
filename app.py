import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Turbo Pro", initial_sidebar_state="collapsed")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { padding: 12px; border-radius: 8px; border: 1px solid #333; text-align: center; background-color: #111; margin-bottom: 10px; }
    .priority-high { color: white; background-color: #d32f2f; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 11px; }
    .priority-medium { color: black; background-color: #ffca28; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 11px; }
    .health-box { background-color: #1a1a1a; padding: 15px; border-left: 5px solid #ffca28; border-radius: 5px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Optimized Data Fetching
@st.cache_data(ttl=60)
def fetch_fast_data(tickers):
    return yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)

# Watchlist
main_indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC", "HAL", "BEL"]

# --- APP LAYOUT ---
st.title("📟 Santosh Master Turbo Terminal")
st.write(f"Turbo Mode ON | {datetime.now().strftime('%H:%M:%S')}")

# A. TOP BAR CARDS
top_cols = st.columns(len(main_indices))
for i, (name, sym) in enumerate(main_indices.items()):
    try:
        idx = yf.Ticker(sym).history(period="1d", interval="5m")
        if not idx.empty:
            cmp, prev = round(idx['Close'].iloc[-1], 2), idx['Close'].iloc[-2]
            status, col = ("BULLISH", "#2ecc71") if cmp > prev else ("BEARISH", "#e74c3c")
            with top_cols[i]:
                st.markdown(f"<div class='signal-card'><small>{name}</small><h3 style='color:{col}; margin:5px 0;'>{status}</h3><b>{cmp}</b></div>", unsafe_allow_html=True)
    except: continue

st.markdown("---")

# B. DATA PROCESSING
all_tickers = [t + ".NS" for t in power_list]
raw_data = fetch_fast_data(all_tickers)
signals, bulls, bears = [], 0, 0

for t in power_list:
    try:
        df = raw_data[t + ".NS"].dropna()
        if df.empty: continue
        h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
        if cmp > df['Close'].iloc[-2]: bulls += 1
        else: bears += 1
        
        # Power Filter
        if cmp >= (h * 0.9985) or cmp <= (l * 1.0015):
            prio = "HIGH" if (cmp >= h or cmp <= l) else "MEDIUM"
            sig, lvl, col = ("BULLISH", f"ABOVE {h}", "#2ecc71") if cmp > (h+l)/2 else ("BEARISH", f"BELOW {l}", "#e74c3c")
            signals.append({"S": t, "SIG": sig, "L": lvl, "P": prio, "C": col})
    except: continue

# C. MAIN DISPLAY
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.subheader("Market Breadth") #
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    # Health Box [cite: 2026-01-29]
    st.markdown("""
        <div class='health-box'>
            <h4 style='color:#ffca28; margin-top:0;'>🧘‍♂️ Santosh Health Tip</h4>
            <p style='font-size:14px;'>Bhai, dandruff se bachne ke liye <b>Almond Oil</b> lagana mat bhulna. 
            Scalp healthy rahegi toh focus trading par behtar rahega!</p>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.subheader("🔥 Tradex Power Signals") #
    if signals:
        h1, h2, h3, h4 = st.columns([1.5, 1, 2, 1])
        h1.write("**SCRIPT**"); h2.write("**SIGNAL**"); h3.write("**LEVELS**"); h4.write("**PRIORITY**")
        st.markdown("---")
        for s in signals:
            r1, r2, r3, r4 = st.columns([1.5, 1, 2, 1])
            r1.write(f"**{s['S']}**")
            r2.markdown(f"<span style='color:{s['C']}; font-weight:bold;'>SIGNAL</span>", unsafe_allow_html=True)
            r3.write(f"**{s['L']}**")
            p_cls = "priority-high" if s['P'] == "HIGH" else "priority-medium"
            r4.markdown(f"<span class='{p_cls}'>{s['P']}</span>", unsafe_allow_html=True)
    else: st.info("Scanning... No breakouts right now.")

time.sleep(60)
st.rerun()
