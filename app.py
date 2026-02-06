import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# Page Setup
st.set_page_config(layout="wide", page_title="Santosh Master Terminal")

# Styling: High-Visibility Cards
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { 
        padding: 15px; border-radius: 8px; border: 1px solid #444; 
        text-align: center; margin-bottom: 10px; background-color: #111;
    }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. DATA FETCHING LOGIC (Indices + Commodities)
def get_market_signals():
    # Yahoo Finance Tickers for Nifty, Sensex, Crude, NG, Gold, Silver
    tickers = {
        "NIFTY 50": "^NSEI", 
        "SENSEX": "^BSESN", 
        "CRUDE OIL": "CL=F", 
        "NAT GAS": "NG=F", 
        "GOLD": "GC=F", 
        "SILVER": "SI=F"
    }
    
    signals = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="1d", interval="5m")
            if not data.empty:
                cmp = round(data['Close'].iloc[-1], 2)
                open_p = data['Open'].iloc[0]
                high = data['High'].max()
                low = data['Low'].min()
                
                # Tradex Style Logic: CMP vs High/Low
                if cmp > (high * 0.998): 
                    status, color = "BULLISH", "#2ecc71"
                elif cmp < (low * 1.002): 
                    status, color = "BEARISH", "#e74c3c"
                else: 
                    status, color = "SIDEWAYS", "#ffca28"
                
                signals.append({"name": name, "cmp": cmp, "status": status, "color": color})
        except: continue
    return signals

# --- UI EXECUTION ---
st.title("📟 Santosh Master Command Center")
st.write(f"Live Market Feed | Last Update: {datetime.now().strftime('%H:%M:%S')}")

# A. TOP SECTION: SIGNAL CARDS (Nifty, Sensex, Commodities)
signals = get_market_signals()
if signals:
    cols = st.columns(len(signals))
    for i, sig in enumerate(signals):
        with cols[i]:
            st.markdown(f"""
                <div class='signal-card'>
                    <small>{sig['name']}</small>
                    <h3 style='color:{sig['color']}; margin:5px 0;'>{sig['status']}</h3>
                    <p style='margin:0; font-size:18px;'>{sig['cmp']}</p>
                </div>
            """, unsafe_allow_html=True)

# B. MIDDLE SECTION: MARKET BREADTH (IntradayPulse Style)
st.markdown("---")
# (Nifty 50 Table Logic remains as before)
nifty_list = ["RELIANCE", "TCS", "HDFCBANK", "SBIN", "ICICIBANK", "TATAMOTORS", "INFY", "DLF", "GNFC"]

def get_table_data():
    rows = []
    data = yf.download([t + ".NS" for t in nifty_list], period="2d", group_by='ticker', progress=False)
    for t in nifty_list:
        try:
            df = data[t + ".NS"]
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = df['Open'].iloc[-1]
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > df['Close'].iloc[-2] else "Negative"
            rows.append({
                "Action": action, "Symbol": t, "Entry Price": round(open_p, 2), "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Financial Trend": trend, "Valuation": "Attractive" if trend == "Positive" else "Fair"
            })
        except: continue
    return pd.DataFrame(rows)

df_table = get_table_data()
if not df_table.empty:
    col_chart, col_spacer = st.columns([1, 2])
    with col_chart:
        pos = len(df_table[df_table['Financial Trend'] == 'Positive'])
        neg = len(df_table[df_table['Financial Trend'] == 'Negative'])
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[pos, neg], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # C. BOTTOM SECTION: MOTILAL TRADE GUIDE TABLE
    st.subheader("📊 Trade Guide (Equity Signals)")
    def style_rows(val):
        if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
        if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
        return ''
    
    # Error Fix: Use .map instead of .applymap
    st.table(df_table.style.map(style_rows, subset=['Action']))

# 4. AUTO REFRESH (Every 60 Seconds)
time.sleep(60)
st.rerun()
