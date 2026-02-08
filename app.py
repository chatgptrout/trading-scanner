import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Ultimate Tradex", initial_sidebar_state="collapsed")

# Custom UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .tradex-header { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px; display: flex; justify-content: space-between; }
    .status-live { background-color: #ff4b4b; color: white; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 8px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    .rocker-box { border: 1px solid #d1e7dd; padding: 10px; border-radius: 8px; text-align: center; }
    .swing-card { background-color: #fff; border: 1px solid #eee; padding: 12px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-top: 15px; }
    .priority-tag { background-color: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #bbdefb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Logic
def get_all_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC"]
    
    # A. Index Results
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

    # B. Power Signals
    tickers = [t + ".NS" if t != "POWERINDIA" else t for t in power_list]
    raw = yf.download(tickers, period="5d", interval="5m", group_by='ticker', progress=False)
    signals, bulls, bears = [], 0, 0
    for t in power_list:
        try:
            df = raw[t + ".NS" if t != "POWERINDIA" else t].dropna()
            if df.empty: continue
            h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
            if cmp > df['Close'].iloc[-2]: bulls += 1
            else: bears += 1
            if cmp >= (h * 0.998) or cmp <= (l * 1.002):
                msg = f"REVERSAL POSSIBLE FROM {h}" if cmp >= (h*0.999) else f"BEARISH BELOW {l}"
                signals.append({"S": t, "L": msg, "P": "MEDIUM"})
        except: continue
    return idx_res, signals, bulls, bears

# --- DISPLAY ---
idx_res, sig_res, bulls, bears = get_all_data()

st.markdown(f"<div class='tradex-header'><div><b>TRADEX</b> <span class='status-live'>LIVE</span></div><div>{datetime.now().strftime('%H:%M:%S')}</div></div>", unsafe_allow_html=True)

# 1. RESTORED Index Bar
i_cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with i_cols[i]:
        st.markdown(f"<div class='index-card'><small style='color:#888'>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("---")

# 2. Market Rockers
r1, r2, r3 = st.columns(3)
with r1: st.markdown(f"<div class='rocker-box' style='background:#f1f8f6;'><h2 style='color:#198754; margin:0;'>{bulls} Stocks Up</h2><small>Bullish Sentiment</small></div>", unsafe_allow_html=True)
with r2: st.markdown(f"<div class='rocker-box' style='background:#fff5f5; border-color:#f8d7da;'><h2 style='color:#dc3545; margin:0;'>{bears} Stocks Down</h2><small>Bearish Pressure</small></div>", unsafe_allow_html=True)
with r3: st.markdown(f"<div class='rocker-box' style='background:#f8f9fa; border-color:#eee;'><h2 style='color:#333; margin:0;'>{bulls+bears} Scanned</h2><small>Market Rockers Live</small></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Main Body
c_left, c_right = st.columns([1, 2.5])

with c_left:
    st.subheader("Market Breadth") # RESTORED
    if (bulls+bears) > 0:
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    # NEW Swing Spectrum Card
    st.markdown("<div class='swing-card'><b>Swing Spectrum</b><br><small style='color:#888'>Find BO & Reversal Stocks</small><hr style='margin:10px 0;'>✔️ Active Scanners Loaded</div>", unsafe_allow_html=True)

with c_right:
    st.subheader("🔥 Tradex Power Signals") # RESTORED
    if sig_res:
        h1, h2, h3 = st.columns([1.5, 3, 1])
        h1.write("**SCRIPT**"); h2.write("**LEVELS / MESSAGE**"); h3.write("**PRIORITY**")
        st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)
        for s in sig_res:
            r1, r2, r3 = st.columns([1.5, 3, 1])
            r1.write(f"**{s['S']}**")
            r2.write(f"✔️ {s['L']}") # Tick Mark ✔️
            r3.markdown(f"<span class='priority-tag'>{s['P']}</span>", unsafe_allow_html=True)
    else: st.info("Scanning Swing Spectrum... No high probability reversals yet.")

time.sleep(60)
st.rerun()
