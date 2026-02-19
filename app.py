import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V67", layout="wide")

# --- WHITE THEME CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .price-card { 
        background: #fdfdfd; padding: 20px; border-radius: 12px; 
        border: 1px solid #e0e0e0; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .buy-label { background: #00c853; color: white; padding: 5px 15px; border-radius: 5px; font-weight: 900; }
    .sell-label { background: #ff1744; color: white; padding: 5px 15px; border-radius: 5px; font-weight: 900; }
    .level-box { font-size: 14px; margin-top: 10px; font-weight: bold; padding: 5px; border-radius: 5px; }
    .bull-lvl { color: #00c853; border: 1px solid #00c853; background: #e8f5e9; }
    .bear-lvl { color: #ff1744; border: 1px solid #ff1744; background: #ffebee; }
    </style>
    """, unsafe_allow_html=True)

def get_market_data():
    # Index & Commodities
    symbols = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    main_rows = []
    for name, sym in symbols.items():
        df = yf.Ticker(sym).history(period="5d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            high = round(df['High'].max(), 2)
            low = round(df['Low'].min(), 2)
            sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
            main_rows.append({"name": name, "ltp": ltp, "sig": sig, "bull": high, "bear": low})
    
    # BTST / Breakout Logic
    watch = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS", "ICICIBANK.NS"]
    scan_results = []
    for s in watch:
        sdf = yf.Ticker(s).history(period="2d", interval="15m")
        if not sdf.empty:
            cur = round(sdf['Close'].iloc[-1], 2)
            day_high = round(sdf['High'].max(), 2)
            day_low = round(sdf['Low'].min(), 2)
            
            # Filter: Only show Breakouts or BTST candidates
            if cur >= (day_high * 0.997): # Near high
                scan_results.append({"Script": s.split('.')[0], "Signal": "BREAKOUT 🚀", "Action": "BTST ✅", "LTP": cur})
            elif cur <= (day_low * 1.003): # Near low
                scan_results.append({"Script": s.split('.')[0], "Signal": "BREAKDOWN 📉", "Action": "STBT ❌", "LTP": cur})
    
    return main_rows, pd.DataFrame(scan_results)

# --- UI HEADER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#1a237e;'>🦅 TRADEX PRO V67 | WHITE MODE</h2>", unsafe_allow_html=True)

m_data, s_data = get_market_data()

# Main Cards Row
cols = st.columns(4)
for i, item in enumerate(m_data):
    with cols[i]:
        lbl = "buy-label" if item['sig'] == "BUY" else "sell-label"
        st.markdown(f"""<div class='price-card'>
            <div style='color:#777; font-size:12px;'>{item['name']}</div>
            <div style='font-size:32px; font-weight:900;'>{item['ltp']}</div>
            <div class='{lbl}'>{item['sig']}</div>
            <div class='level-box bull-lvl'>BULLISH ABOVE: {item['bull']}</div>
            <div class='level-box bear-lvl'>BEARISH BELOW: {item['bear']}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><h3 style='color:#1a237e;'>🚀 BREAKOUT & BTST/STBT SCANNER</h3>", unsafe_allow_html=True)
if not s_data.empty:
    st.table(s_data) # Only showing filtered stocks
else:
    st.info("No active Breakouts or BTST signals at this moment.")

time.sleep(10)
st.rerun()
