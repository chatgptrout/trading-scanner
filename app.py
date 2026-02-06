import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(layout="wide", page_title="Santosh Tradex Pro")

# UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .priority-high { color: #ffffff; background-color: #d32f2f; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    .priority-medium { color: #000000; background-color: #ffca28; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border-bottom: 1px solid #222 !important; padding: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. 100+ High Volume Stocks for Backend Scanning
stock_list = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "AXISBANK", "PNB", "BANKBARODA",
    "ADANIENT", "POWERGRID", "NTPC", "HAL", "BEL", "TRENT", "DLF", "GNFC", "MCX", "GOLDMINI", "SILVERMINI"
]

def get_tradex_signals():
    rows = []
    tickers = [t + ".NS" if t not in ["MCX", "GOLDMINI"] else t for t in stock_list] # Simplified for Yahoo
    data = yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)
    
    for t in stock_list:
        try:
            df = data[t + ".NS" if t not in ["MCX", "GOLDMINI"] else t].dropna()
            if df.empty: continue
            h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
            
            # Action Filtering Logic
            is_bullish = cmp >= (h * 0.997)
            is_bearish = cmp <= (l * 1.003)
            
            if is_bullish or is_bearish:
                priority = "HIGH" if (is_bullish and cmp > h) or (is_bearish and cmp < l) else "MEDIUM"
                msg = "BREAKOUT OPPORTUNITY" if priority == "HIGH" else "POTENTIAL REVERSAL"
                
                if is_bullish:
                    sig, lvl, col = "BULLISH", f"ABOVE {h}", "#2ecc71"
                else:
                    sig, lvl, col = "BEARISH", f"BELOW {l}", "#e74c3c"
                
                rows.append({
                    "SCRIPT": t, "SIGNAL": sig, "LEVELS": lvl, 
                    "MESSAGE": msg, "PRIORITY": priority, "COLOR": col
                })
        except: continue
    return rows

# --- DISPLAY ---
st.title("📟 Tradex Live Signals")
st.write(f"Live Market Dashboard | {datetime.now().strftime('%H:%M:%S')}")

signals = get_tradex_signals()

if signals:
    # Header
    c1, c2, c3, c4, c5 = st.columns([1.5, 1, 2, 2, 1])
    c1.write("**SCRIPT**")
    c2.write("**SIGNAL**")
    c3.write("**LEVELS**")
    c4.write("**MESSAGE**")
    c5.write("**PRIORITY**")
    st.markdown("---")

    for s in signals:
        r1, r2, r3, r4, r5 = st.columns([1.5, 1, 2, 2, 1])
        r1.write(f"**{s['SCRIPT']}**")
        r2.markdown(f"<span style='color:{s['COLOR']}; font-weight:bold;'>SIGNAL</span>", unsafe_allow_html=True)
        r3.markdown(f"**{s['LEVELS']}**")
        r4.write(s['MESSAGE'])
        
        p_class = "priority-high" if s['PRIORITY'] == "HIGH" else "priority-medium"
        r5.markdown(f"<span class='{p_class}'>{s['PRIORITY']}</span>", unsafe_allow_html=True)
else:
    st.info("Searching for Active Signals... No major breakouts detected right now.")

# Auto-Refresh
time.sleep(60)
st.rerun()
