import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- UI CONFIG ---
st.set_page_config(page_title="TRADEX PRO V68", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    .price-card { 
        background: #ffffff; padding: 20px; border-radius: 12px; 
        border: 1px solid #e0e0e0; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .buy-box { background: #00c853; color: white; padding: 8px; border-radius: 5px; font-weight: 900; margin: 10px 0; }
    .sell-box { background: #ff1744; color: white; padding: 8px; border-radius: 5px; font-weight: 900; margin: 10px 0; }
    .level-container { font-size: 14px; font-weight: bold; padding: 8px; border-radius: 8px; margin-top: 5px; }
    .bull-lvl { color: #00c853; border: 2px solid #00c853; background: #e8f5e9; }
    .bear-lvl { color: #ff1744; border: 2px solid #ff1744; background: #ffebee; }
    </style>
    """, unsafe_allow_html=True)

def get_accurate_data():
    # Symbols based on your dashboard
    symbols = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    main_rows = []
    for name, sym in symbols.items():
        # Fetching 2 days data for high/low calculation
        df = yf.Ticker(sym).history(period="2d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            high_lvl = round(df['High'].max(), 2) # Bullish Above logic
            low_lvl = round(df['Low'].min(), 2)   # Bearish Below logic
            ema = df['Close'].ewm(span=9).mean().iloc[-1]
            status = "BUY" if ltp > ema else "SELL"
            main_rows.append({"name": name, "ltp": ltp, "status": status, "bull": high_lvl, "bear": low_lvl})
            
    # BTST/STBT Logic for specific stocks
    stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
    scan_results = []
    for s in stocks:
        sdf = yf.Ticker(s).history(period="1d", interval="15m")
        if not sdf.empty:
            cur = round(sdf['Close'].iloc[-1], 2)
            s_high = round(sdf['High'].max(), 2)
            if cur >= (s_high * 0.998): # Breakout/BTST signal
                scan_results.append({"Script": s.replace(".NS",""), "Signal": "BREAKOUT", "LTP": cur, "Action": "BTST ✅"})
    
    return main_rows, pd.DataFrame(scan_results)

# --- HEADER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#1a237e;'>🦅 TRADEX PRO V68 | WHITE MODE</h2>", unsafe_allow_html=True)

data_list, breakout_df = get_accurate_data()

# Render Cards
cols = st.columns(4)
for i, item in enumerate(data_list):
    with cols[i]:
        bg_class = "buy-box" if item['status'] == "BUY" else "sell-box"
        st.markdown(f"""<div class='price-card'>
            <div style='color:#666; font-size:13px;'>{item['name']}</div>
            <div style='font-size:35px; font-weight:900;'>{item['ltp']}</div>
            <div class='{bg_class}'>{item['status']}</div>
            <div class='level-container bull-lvl'>BULLISH ABOVE: {item['bull']}</div>
            <div class='level-container bear-lvl'>BEARISH BELOW: {item['bear']}</div>
        </div>""", unsafe_allow_html=True)

# Breakout Table
st.markdown("<br><h3 style='color:#1a237e;'>🚀 BREAKOUT & BTST ONLY</h3>", unsafe_allow_html=True)
if not breakout_df.empty:
    st.dataframe(breakout_df, use_container_width=True, hide_index=True)
else:
    st.info("Searching for high-momentum breakouts...")

time.sleep(10)
st.rerun()
