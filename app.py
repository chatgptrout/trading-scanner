import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Tradex Master", initial_sidebar_state="collapsed")

# Tradex Style UI (White Theme with Power Logic)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .tradex-header { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
    .status-live { background-color: #ff4b4b; color: white; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .priority-tag { background-color: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #bbdefb; }
    .index-card { background-color: #f8f9fa; border: 1px solid #eee; padding: 10px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI Calculation
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# 3. Data Engine (Indices + Stocks)
def get_master_data():
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F"}
    power_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "POWERINDIA", "DLF", "GNFC"]
    
    # Indices status
    idx_results = []
    for name, sym in indices.items():
        try:
            d = yf.Ticker(sym).history(period="1d", interval="5m")
            if not d.empty:
                cmp, prev = round(d['Close'].iloc[-1], 2), d['Close'].iloc[-2]
                col = "#2ecc71" if cmp > prev else "#e74c3c"
                idx_results.append({"name": name, "cmp": cmp, "col": col})
        except: continue

    # Power Signals with Tradex Style Messages
    tickers = [t + ".NS" if t != "POWERINDIA" else t for t in power_list]
    raw = yf.download(tickers, period="5d", interval="5m", group_by='ticker', progress=False)
    
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

            # Tradex Power Filter
            if cmp >= (h * 0.997) or cmp <= (l * 1.003):
                msg = f"REVERSAL POSSIBLE FROM {h}" if cmp >= h else f"BEARISH BELOW {l}"
                signals.append({"S": t, "L": msg, "RSI": rsi, "P": "HIGH" if rsi > 70 or rsi < 30 else "MEDIUM"})
        except: continue
        
    return idx_results, signals, bulls, bears

# --- DISPLAY ---
idx_res, sig_res, bulls, bears = get_master_data()

# Header
st.markdown(f"""
    <div class='tradex-header'>
        <div><b>TRADEX</b> <span class='status-live'>LIVE</span></div>
        <div style='color:#888;'>{datetime.now().strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

# Top Indices Cards
cols = st.columns(len(idx_res))
for i, x in enumerate(idx_res):
    with cols[i]:
        st.markdown(f"<div class='index-card'><small style='color:#888'>{x['name']}</small><h4 style='color:{x['col']}; margin:0'>{x['cmp']}</h4></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.subheader("Market Breadth") #
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[bulls, bears], hole=.7, marker_colors
