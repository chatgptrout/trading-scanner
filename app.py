import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Signal Pro")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { 
        padding: 15px; border-radius: 8px; border: 1px solid #333; 
        text-align: center; margin-bottom: 10px; background-color: #111;
    }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.1px solid #333 !important; padding: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for Top Bar Levels (Indices & Commodities)
def get_master_levels():
    tickers = {
        "NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN",
        "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"
    }
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="1d", interval="5m")
            if not data.empty:
                high, low = round(data['High'].max(), 2), round(data['Low'].min(), 2)
                cmp = data['Close'].iloc[-1]
                if cmp > (high + low)/2:
                    status, level, color = "BULLISH", f"ABOVE {high}", "#2ecc71"
                else:
                    status, level, color = "BEARISH", f"BELOW {low}", "#e74c3c"
                results.append({"name": name, "status": status, "level": level, "color": color})
        except: continue
    return results

# 3. Stock Signal Logic (Nifty 50)
stock_list = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "AXISBANK", "DLF", "GNFC"]

def get_stock_data():
    rows = []
    data = yf.download([t + ".NS" for t in stock_list], period="1d", interval="5m", group_by='ticker', progress=False)
    for t in stock_list:
        try:
            df = data[t + ".NS"]
            high, low = round(df['High'].max(), 2), round(df['Low'].min(), 2)
            cmp = df['Close'].iloc[-1]
            if cmp > (high + low)/2:
                sig, lvl, col = "BULLISH", f"ABOVE {high}", "#2ecc71"
            else:
                sig, lvl, col = "BEARISH", f"BELOW {low}", "#e74c3c"
            rows.append({"Symbol": t, "Signal": sig, "Level": lvl, "Color": col})
        except: continue
    return rows

# --- DISPLAY ---
st.title("📟 Santosh Pro Master Signal Terminal")
st.write(f"Live Action Levels | Last Update: {datetime.now().strftime('%H:%M:%S')}")

# A. TOP CARDS (Indices & Commodities)
sigs = get_master_levels()
if sigs:
    cols = st.columns(len(sigs))
    for i, s in enumerate(sigs):
        with cols[i]:
            st.markdown(f"<div class='signal-card'><small>{s['name']}</small><h3 style='color:{s['color']}; margin:5px 0;'>{s['status']}</h3><b>{s['level']}</b></div>", unsafe_allow_html=True)

st.markdown("---")

# B. CLEAN STOCK TABLE (Fixing the AttributeError)
stocks = get_stock_data()
if stocks:
    st.subheader("📊 Equity Trade Signals")
    # Table headers
    head1, head2, head3 = st.columns([1, 1, 2])
    head1.write("**SYMBOL**")
    head2.write("**SIGNAL**")
    head3.write("**LEVEL**")
    
    for s in stocks:
        c1, c2, c3 = st.columns([1, 1, 2])
        c1.write(s['Symbol'])
        c2.markdown(f"<span style='color:{s['Color']}; font-weight:bold;'>{s['Signal']}</span>", unsafe_allow_html=True)
        c3.markdown(f"<span style='color:{s['Color']}; font-weight:bold;'>{s['Level']}</span>", unsafe_allow_html=True)

# 4. AUTO REFRESH
time.sleep(60)
st.rerun()
