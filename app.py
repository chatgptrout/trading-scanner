import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Nifty 50 Terminal")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { 
        padding: 12px; border-radius: 8px; border: 1px solid #333; 
        text-align: center; margin-bottom: 10px; background-color: #111;
    }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Top Bar Logic (Indices & Commodities)
def get_master_signals():
    tickers = {
        "NIFTY 50": "^NSEI", "SENSEX": "^BSESN", 
        "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", 
        "GOLD": "GC=F", "SILVER": "SI=F"
    }
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="2d", interval="5m")
            if not data.empty:
                cmp = round(data['Close'].iloc[-1], 2)
                high, low = data['High'].max(), data['Low'].min()
                prev_close = data['Close'].iloc[-2]
                if name == "NAT GAS":
                    if cmp > (high * 0.995): status, color = "🚀 BREAKOUT", "#00ff00"
                    elif cmp < (low * 1.005): status, color = "⚠️ CRASHING", "#ff0000"
                    else: status, color = "SIDEWAYS", "#ffca28"
                else:
                    status, color = ("BULLISH", "#2ecc71") if cmp > prev_close else ("BEARISH", "#e74c3c")
                results.append({"name": name, "cmp": cmp, "status": status, "color": color})
        except: continue
    return results

# 3. FULL NIFTY 50 STOCK LIST
nifty50_full = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", 
    "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", 
    "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", 
    "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", 
    "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "LTIM", "M&M", 
    "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", 
    "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", 
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]

def get_table_data():
    rows = []
    # Batch download for 50 stocks
    data = yf.download([t + ".NS" for t in nifty50_full], period="2d", group_by='ticker', progress=False)
    for t in nifty50_full:
        try:
            df = data[t + ".NS"]
            if df.empty: continue
            cmp, open_p = round(df['Close'].iloc[-1], 2), df['Open'].iloc[-1]
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > df['Close'].iloc[-2] else "Negative"
            rows.append({
                "Action": action, "Symbol": t, "Entry": round(open_p, 2), "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Trend": trend, "Valuation": "Attractive" if trend == "Positive" else "Fair"
            })
        except: continue
    return pd.DataFrame(rows)

# --- DISPLAY ---
st.title("📟 Santosh Nifty 50 Live Terminal")
st.write(f"Scanning 50 Stocks... Last Update: {datetime.now().strftime('%H:%M:%S')}")

# A. TOP SIGNALS (Indices & Commodities)
sigs = get_master_signals()
if sigs:
    cols = st.columns(6)
    for i, s in enumerate(sigs):
        with cols[i]:
            st.markdown(f"<div class='signal-card'><small>{s['name']}</small><h3 style='color:{s['color']}; margin:5px 0;'>{s['status']}</h3><b>{s['cmp']}</b></div>", unsafe_allow_html=True)

st.markdown("---")

# B. BREADTH & TABLE
df = get_table_data()
if not df.empty:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Nifty 50 Breadth")
        pos, neg = len(df[df['Trend'] == 'Positive']), len(df[df['Trend'] == 'Negative'])
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[pos, neg], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("📊 Motilal Trade Guide (Full Nifty 50)")
        def style_rows(val):
            if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
            if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
            return ''
        st.table(df.style.map(style_rows, subset=['Action']))

# 4. AUTO REFRESH
time.sleep(60)
st.rerun()
