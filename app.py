import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Nifty50 Scanner")

# Professional Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    th { background-color: #222 !important; color: #ffca28 !important; border: 1px solid #444 !important; }
    td { border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NIFTY 50 TICKER LIST ---
nifty50_tickers = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", 
    "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", 
    "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", 
    "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", 
    "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "LTIM", "M&M", 
    "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", 
    "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", 
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]

def fetch_nifty_data(tickers):
    rows = []
    # Adding .NS for Yahoo Finance
    formatted_tickers = [t + ".NS" for t in tickers]
    
    # Batch download for speed
    data = yf.download(formatted_tickers, period="2d", group_by='ticker', interval="1m", progress=False)
    
    for t in tickers:
        try:
            df = data[t + ".NS"]
            if df.empty: continue
            
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = round(df['Open'].iloc[0], 2) # Today's open
            prev_close = df['Close'].iloc[-2]
            high = df['High'].max()
            low = df['Low'].min()
            
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > prev_close else "Negative"
            
            rows.append({
                "Action": action,
                "Symbol": t,
                "Entry": open_p,
                "Stop Loss": round(low * 0.998, 2) if action == "BUY EXIT" else round(high * 1.002, 2),
                "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Financial Trend": trend,
                "Valuation": "Attractive" if trend == "Positive" else "Fair"
            })
        except: continue
    return pd.DataFrame(rows)

# --- UI EXECUTION ---
st.title("📟 Santosh Nifty 50 Live Terminal")
st.write(f"Scanning 50 Stocks... Last Update: {datetime.now().strftime('%H:%M:%S')}")

df_nifty = fetch_nifty_data(nifty50_tickers)

if not df_nifty.empty:
    # 1. Circular Chart (IntradayPulse Style)
    pos_count = len(df_nifty[df_nifty['Financial Trend'] == 'Positive'])
    neg_count = len(df_nifty[df_nifty['Financial Trend'] == 'Negative'])
    
    fig = go.Figure(data=[go.Pie(
        labels=['Positive', 'Negative'], 
        values=[pos_count, neg_count],
        hole=.7,
        marker_colors=['#2ecc71', '#e74c3c']
    )])
    fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # 2. Detailed Table (Motilal Style)
    def color_rows(val):
        if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
        if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
        return ''

    st.subheader("📊 Intraday Trade Guide")
    st.table(df_nifty.style.map(color_rows, subset=['Action']))

# 3. Auto-Refresh Logic
time.sleep(60)
st.rerun()
