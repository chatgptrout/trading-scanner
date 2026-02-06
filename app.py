import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(layout="wide", page_title="Santosh All-In-One Terminal")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { padding: 10px; border-radius: 8px; border: 1px solid #333; text-align: center; background-color: #111; margin-bottom: 10px; }
    .priority-high { color: white; background-color: #d32f2f; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; }
    .priority-medium { color: black; background-color: #ffca28; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 1. TOP BAR DATA (Indices & Commodities)
def get_top_bar():
    tickers = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="1d", interval="5m")
            if not data.empty:
                cmp = round(data['Close'].iloc[-1], 2)
                prev_close = data['Close'].iloc[-2]
                status, color = ("BULLISH", "#2ecc71") if cmp > prev_close else ("BEARISH", "#e74c3c")
                if name == "NAT GAS": status, color = ("SIDEWAYS", "#ffca28") if abs(cmp-prev_close) < 0.01 else (status, color)
                results.append({"name": name, "status": status, "cmp": cmp, "color": color})
        except: continue
    return results

# 2. BREADTH & POWER SIGNALS
power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC", "HAL", "BEL"]

def get_master_data():
    tickers = [t + ".NS" for t in power_list]
    data = yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)
    signals, bulls, bears = [], 0, 0
    for t in power_list:
        try:
            df = data[t + ".NS"].dropna()
            if df.empty: continue
            h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
            if cmp > df['Close'].iloc[-2]: bulls += 1
            else: bears += 1
            if cmp >= (h * 0.998) or cmp <= (l * 1.002):
                priority = "HIGH" if (cmp >= h or cmp <= l) else "MEDIUM"
                sig, lvl, col = ("BULLISH", f"ABOVE {h}", "#2ecc71") if cmp > (h+l)/2 else ("BEARISH", f"BELOW {l}", "#e74c3c")
                signals.append({"SCRIPT": t, "SIGNAL": sig, "LEVELS": lvl, "PRIORITY": priority, "COLOR": col})
        except: continue
    return signals, bulls, bears

# --- DISPLAY ---
st.title("📟 Santosh Master Trading Command Center")

# A. TOP BAR
top_sigs = get_top_bar()
if top_sigs:
    cols = st.columns(len(top_sigs))
    for i, s in enumerate(top_sigs):
        with cols[i]:
            st.markdown(f"<div class='signal-card'><small>{s['name']}</small><h3 style='color:{s['color']}; margin:5px 0;'>{s['status']}</h3><b>{s['cmp']}</b></div>", unsafe_allow_html=True)

st.markdown("---")

# B. MIDDLE SECTION
signals, bulls, bears = get_master_data()
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.subheader("Market Breadth") #
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=280, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🔥 Tradex Power Signals") #
    if signals:
        c1, c2, c3, c4 = st.columns([1.5, 1, 2, 1])
        c1.write("**SCRIPT**"); c2.write("**SIGNAL**"); c3.write("**LEVELS**"); c4.write("**PRIORITY**")
        for s in signals:
            r1, r2, r3, r4 = st.columns([1.5, 1, 2, 1])
            r1.write(f"**{s['SCRIPT']}**")
            r2.markdown(f"<span style='color:{s['COLOR']}; font-weight:bold;'>SIGNAL</span>", unsafe_allow_html=True)
            r3.write(f"**{s['LEVELS']}**")
            p_tag = "priority-high" if s['PRIORITY'] == "HIGH" else "priority-medium"
            r4.markdown(f"<span class='{p_tag}'>{s['PRIORITY']}</span>", unsafe_allow_html=True)
    else: st.info("Scanning for Action... No levels triggered yet.")

time.sleep(60)
st.rerun()
