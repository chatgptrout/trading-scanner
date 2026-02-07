import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config & Professional UI
st.set_page_config(layout="wide", page_title="Santosh Tradex Master", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .tradex-header { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px; display: flex; justify-content: space-between; }
    .status-live { background-color: #ff4b4b; color: white; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    .priority-tag { background-color: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #bbdefb; }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI & Data Engine
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_master_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC"]
    
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

    all_tickers = [t + ".NS" if t != "POWERINDIA" else t for t in power_list]
    raw = yf.download(all_tickers, period="5d", interval="5m", group_by='ticker', progress=False)
    
    signals, bulls, bears = [], 0, 0
    for t in power_list:
        try:
            df = raw[t + ".NS" if t != "POWERINDIA" else t].dropna()
            if df.empty: continue
            h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
            df['RSI'] = calculate_rsi(df['Close'])
            rsi = round(df['RSI'].iloc[-1], 2)
            
            if cmp > df['Close'].iloc[-2]: bulls += 1
            else: bears += 1

            if cmp >= (h * 0.997) or cmp <= (l * 1.003):
                msg = f"REVERSAL POSSIBLE FROM {h}" if cmp >= h else f"BEARISH BELOW {l}"
                signals.append({"S": t, "L": msg, "RSI": rsi, "P": "HIGH" if rsi > 70 or rsi < 30 else "MEDIUM"})
        except: continue
        
    return idx_res, signals, bulls, bears

# --- DISPLAY ---
idx_res, sig_res, bulls, bears = get_master_data()

st.markdown(f"<div class='tradex-header'><div><b>TRADEX</b> <span class='status-live'>LIVE</span></div><div>{datetime.now().strftime('%H:%M:%S')}</div></div>", unsafe_allow_html=True)

# Top Indices
i_cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with i_cols[i]:
        st.markdown(f"<div class='index-card'><small>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2.5])

with col1:
    st.subheader("Market Breadth") # RESTORED
    if (bulls + bears) > 0:
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True) # FIXED ERROR HERE

with col2:
    st.subheader("🔥 Tradex Power Signals") # RESTORED
    if sig_res:
        c1, c2, c3, c4 = st.columns([1, 2, 0.8, 1])
        c1.write("**SCRIPT**"); c2.write("**LEVELS / MESSAGE**"); c3.write("**RSI**"); c4.write("**PRIORITY**")
        st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)
        for s in sig_res:
            r1, r2, r3, r4 = st.columns([1, 2, 0.8, 1])
            r1.write(f"**{s['S']}**")
            r2.write(f"✔️ {s['L']}") # Tick Mark Restored
            r3.write(f"{s['RSI']}")
            r4.markdown(f"<span class='priority-tag'>{s['P']}</span>", unsafe_allow_html=True)
    else:
        st.info("Scanning... No Power signals right now.")

time.sleep(60)
st.rerun()
