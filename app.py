import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Pro Terminal")

# Professional Dark UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; border: 1px solid #333 !important; }
    td { border: 1px solid #222 !important; padding: 12px !important; }
    .metric-card { background-color: #111; padding: 15px; border-radius: 10px; border-left: 5px solid #ffca28; }
    </style>
    """, unsafe_allow_html=True)

# Nifty 50 Ticker List
nifty50 = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", 
    "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", 
    "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", 
    "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", 
    "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "LTIM", "M&M", 
    "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", 
    "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", 
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]

def get_live_market_data():
    rows = []
    tickers = [t + ".NS" for t in nifty50]
    # Batch download for speed
    data = yf.download(tickers, period="2d", group_by='ticker', progress=False)
    
    for t in nifty50:
        try:
            df = data[t + ".NS"]
            if df.empty: continue
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = round(df['Open'].iloc[-1], 2)
            high = round(df['High'].iloc[-1], 2)
            low = round(df['Low'].iloc[-1], 2)
            prev_close = df['Close'].iloc[-2]
            
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > prev_close else "Negative"
            
            rows.append({
                "Action": action,
                "Symbol": t,
                "Entry Price": open_p,
                "Stop Loss": round(low * 0.998, 2) if action == "BUY EXIT" else round(high * 1.002, 2),
                "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Trend": trend,
                "Valuation": "Attractive" if trend == "Positive" else "Fair"
            })
        except: continue
    return pd.DataFrame(rows)

# --- EXECUTION ---
st.title("📟 Santosh Live Trading Dashboard")
st.write(f"Refreshed at: {datetime.now().strftime('%H:%M:%S')}")

df = get_live_market_data()

if not df.empty:
    # 1. TOP SECTION: IntradayPulse Visuals
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Index Mover (Donut Chart)
        pos = len(df[df['Trend'] == 'Positive'])
        neg = len(df[df['Trend'] == 'Negative'])
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[pos, neg], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<div class='metric-card'><b>Market Breadth</b></div>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Sentiment Placeholder (Like PCR Clock)
        pcr_val = round(pos/neg, 2) if neg > 0 else 1.0
        sentiment = "BULLISH" if pcr_val > 1 else "BEARISH"
        st.markdown(f"""
            <div class='metric-card'>
                <b>Market Sentiment</b><br>
                <h1 style='color:{"#2ecc71" if sentiment=="BULLISH" else "#e74c3c"}'>{sentiment}</h1>
                <p>Calculated PCR: {pcr_val}</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        # Top Movers List
        st.markdown("<div class='metric-card'><b>Top Movers</b></div>", unsafe_allow_html=True)
        st.dataframe(df[['Symbol', 'CMP', 'Trend']].sort_values(by='CMP', ascending=False).head(5), hide_index=True)

    # 2. BOTTOM SECTION: Motilal Oswal Table
    st.subheader("📊 Trade Guide Signals")
    
    def apply_style(val):
        if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white; font-weight: bold;'
        if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white; font-weight: bold;'
        if val == 'Positive': return 'color: #2ecc71; font-weight: bold;'
        if val == 'Negative': return 'color: #e74c3c; font-weight: bold;'
        return ''

    # ERROR FIXED: Using .map() instead of .applymap()
    styled_df = df.style.map(apply_style, subset=['Action', 'Trend'])
    st.table(styled_df)

# Auto-Refresh Logic (Every 60s)
time.sleep(60)
st.rerun()
