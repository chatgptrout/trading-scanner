import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config & Tradex White UI
st.set_page_config(layout="wide", page_title="Santosh Tradex Ultimate", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .tradex-header { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px; display: flex; justify-content: space-between; }
    .status-live { background-color: #ff4b4b; color: white; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .rocker-box { background-color: #f1f8f6; border: 1px solid #d1e7dd; padding: 10px; border-radius: 8px; text-align: center; }
    .swing-card { background-color: #fff; border: 1px solid #eee; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .priority-tag { background-color: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #bbdefb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Engine (RSI + Swing + Rockers)
@st.cache_data(ttl=60)
def get_bulk_data(tickers):
    return yf.download(tickers, period="5d", interval="5m", group_by='ticker', progress=False)

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- MAIN APP LOGIC ---
st.markdown(f"<div class='tradex-header'><div><b>TRADEX</b> <span class='status-live'>LIVE</span></div><div>{datetime.now().strftime('%H:%M:%S')}</div></div>", unsafe_allow_html=True)

# Top Row: Market Rockers & Indices
power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC"]
all_tickers = [t + ".NS" if t != "POWERINDIA" else t for t in power_list]
raw_data = get_bulk_data(all_tickers)

bulls, bears = 0, 0
swing_signals = []

for t in power_list:
    try:
        df = raw_data[t + ".NS" if t != "POWERINDIA" else t].dropna()
        if df.empty: continue
        h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
        prev_c = df['Close'].iloc[-2]
        rsi = round(calculate_rsi(df['Close']).iloc[-1], 2)
        
        # Rocker Logic
        if cmp > prev_c: bulls += 1
        else: bears += 1

        # Swing Spectrum & Reversal Logic
        if cmp >= (h * 0.998) or cmp <= (l * 1.002):
            msg = f"REVERSAL POSSIBLE FROM {h}" if cmp >= (h*0.999) else f"BEARISH BELOW {l}"
            swing_signals.append({"S": t, "L": msg, "RSI": rsi, "P": "HIGH" if rsi > 70 or rsi < 30 else "MEDIUM"})
    except: continue

# Display Rockers
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='rocker-box'><h3 style='color:#198754; margin:0;'>{bulls} Stocks Up</h3><small>Bullish Sentiment</small></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='rocker-box' style='background:#fff5f5; border-color:#f8d7da;'><h3 style='color:#dc3545; margin:0;'>{bears} Stocks Down</h3><small>Bearish Pressure</small></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='rocker-box' style='background:#f8f9fa;'><h3 style='color:#333; margin:0;'>{bulls+bears} Scanned</h3><small>Market Rockers Live</small></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Body
col_l, col_r = st.columns([1, 2.5])

with col_l:
    st.subheader("Market Breadth")
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Swing Spectrum Highlight
    st.markdown("<div class='swing-card'><b>Swing Spectrum</b><br><small>Find BO & Reversal Stocks</small><hr style='margin:10px 0;'>✔️ Active Scanners Loaded</div>", unsafe_allow_html=True)

with col_r:
    st.subheader("🔥 Tradex Power Signals")
    if swing_signals:
        h1, h2, h3, h4 = st.columns([1, 2, 0.8, 1])
        h1.write("**SCRIPT**"); h2.write("**LEVELS / MESSAGE**"); h3.write("**RSI**"); h4.write("**PRIORITY**")
        st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)
        for s in swing_signals:
            r1, r2, r3, r4 = st.columns([1, 2, 0.8, 1])
            r1.write(f"**{s['S']}**")
            r2.write(f"✔️ {s['L']}") # Tick Mark
            r3.write(f"{s['RSI']}")
            r4.markdown(f"<span class='priority-tag'>{s['P']}</span>", unsafe_allow_html=True)
    else: st.info("Scanning Swing Spectrum... No high probability reversals yet.")

time.sleep(60)
st.rerun()
