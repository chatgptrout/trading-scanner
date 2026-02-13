import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# Page Setup
st.set_page_config(layout="wide", page_title="Santosh Turbo Scanner")

# Professional Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { padding: 10px; border-radius: 8px; border: 1px solid #333; text-align: center; background-color: #111; }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.1px solid #222 !important; padding: 10px !important; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 1. Top Bar Indices & Commodities
def get_master_signals():
    tickers = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="1d", interval="5m")
            if not data.empty:
                h, l, cmp = data['High'].max(), data['Low'].min(), data['Close'].iloc[-1]
                status, level, col = ("BULLISH", f"ABOVE {round(h,2)}", "#2ecc71") if cmp > (h+l)/2 else ("BEARISH", f"BELOW {round(l,2)}", "#e74c3c")
                results.append({"name": name, "status": status, "level": level, "color": col})
        except: continue
    return results

# 2. 100+ High Volume Stock List (F&O & Nifty 200)
high_volume_stocks = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "AXISBANK", "KOTAKBANK", "LT",
    "BAJFINANCE", "BHARTIARTL", "ITC", "M&M", "ADANIENT", "SUNPHARMA", "TITAN", "ASIANPAINT", "ULTRACEMCO", "HCLTECH",
    "TATASTEEL", "NTPC", "POWERGRID", "MARUTI", "JSWSTEEL", "ONGC", "ADANIPORTS", "COALINDIA", "HINDALCO", "GRASIM",
    "LTIM", "SBILIFE", "BPCL", "DRREDDY", "BAJAJ-AUTO", "CIPLA", "EICHERMOT", "INDUSINDBK", "BRITANNIA", "NESTLEIND",
    "TATACONSUM", "HDFCLIFE", "APOLLOHOSP", "WIPRO", "HEROMOTOCO", "BAJAJFINSV", "TECHM", "DIVISLAB", "UPL", "DLF",
    "HAL", "BEL", "ABB", "TRENT", "CANBK", "PNB", "BANKBARODA", "RECLTD", "PFC", "CHOLAFIN",
    "SHRIRAMFIN", "BHEL", "TATACOMM", "AMBUJACEM", "ACC", "JUBLFOOD", "AUROPHARMA", "LUPIN", "GLENMARK", "GMRINFRA",
    "IDEA", "SAIL", "NMDC", "IOC", "GAIL", "PETRONET", "IGL", "MGL", "ABCAPITAL", "PEL",
    "HINDCOPPER", "NATIONALUM", "ZEEL", "ASHOKLEY", "MOTHERSON", "BALKRISIND", "MRF", "ESCORTS", "CUMMINSIND", "VOLTAS",
    "HAVELLS", "POLYCAB", "DIXON", "ASTRAL", "PIDILITIND", "UBL", "UNITDSPR", "MCDOWELL-N", "COLPAL", "GODREJCP"
]

def get_bulk_stock_signals():
    rows = []
    # Fetching data in one go for speed
    tickers = [t + ".NS" for t in high_volume_stocks]
    data = yf.download(tickers, period="2d", interval="15m", group_by='ticker', progress=False)
    
    for t in high_volume_stocks:
        try:
            df = data[t + ".NS"].dropna()
            if df.empty: continue
            h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
            
            if cmp > (h + l)/2:
                sig, lvl, col = "BULLISH", h, "#2ecc71"
                t1, t2, sl = round(lvl * 1.007, 2), round(lvl * 1.015, 2), round(lvl * 0.994, 2)
            else:
                sig, lvl, col = "BEARISH", l, "#e74c3c"
                t1, t2, sl = round(lvl * 0.993, 2), round(lvl * 0.985, 2), round(lvl * 1.006, 2)
            
            rows.append({"Symbol": t, "Signal": sig, "Entry": lvl, "T1": t1, "T2": t2, "SL": sl, "Color": col})
        except: continue
    return rows

# --- DISPLAY ---
st.title("📟 Santosh Turbo Multi-Scanner (100+ Stocks)")
st.write(f"Live Market Feed | {datetime.now().strftime('%H:%M:%S')}")

# Top Cards
sigs = get_master_signals()
if sigs:
    cols = st.columns(len(sigs))
    for i, s in enumerate(sigs):
        with cols[i]:
            st.markdown(f"<div class='signal-card'><small>{s['name']}</small><h3 style='color:{s['color']}; margin:5px 0;'>{s['status']}</h3><b>{s['level']}</b></div>", unsafe_allow_html=True)

st.markdown("---")

# Bulk Signal Table
stocks = get_bulk_stock_signals()
if stocks:
    st.subheader(f"📊 Scanning {len(stocks)} High-Volume Stocks")
    
    # Custom Table UI
    c1, c2, c3, c4, c5, c6 = st.columns([1.2, 1, 1.5, 1.2, 1.2, 1.2])
    c1.write("**SYMBOL**"); c2.write("**SIGNAL**"); c3.write("**ENTRY LEVEL**")
    c4.write("**TARGET 1**"); c5.write("**TARGET 2**"); c6.write("**STOP LOSS**")
    st.markdown("---")

    for s in stocks:
        r1, r2, r3, r4, r5, r6 = st.columns([1.2, 1, 1.5, 1.2, 1.2, 1.2])
        r1.write(f"**{s['Symbol']}**")
        r2.markdown(f"<span style='color:{s['Color']}; font-weight:bold;'>{s['Signal']}</span>", unsafe_allow_html=True)
        r3.write(f"{'ABOVE' if s['Signal']=='BULLISH' else 'BELOW'} {s['Entry']}")
        r4.write(f"🎯 {s['T1']}")
        r5.write(f"🚀 {s['T2']}")
        r6.write(f"🛑 {s['SL']}")

# Auto-Refresh (Every 2 minutes for 100+ stocks)
time.sleep(120)
st.rerun()
