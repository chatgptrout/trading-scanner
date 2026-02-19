import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V70", layout="wide")

# --- DYNAMIC THEME LOGIC ---
pcr_val = 0.76 #
sent_color = "#ff1744" if pcr_val < 0.85 else "#00c853"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff; color: #1a1a1a; }}
    .pcr-card {{ 
        background: #fdfdfd; padding: 15px; border-radius: 12px; 
        border: 2px solid {sent_color}; text-align: center; 
    }}
    .price-card {{ 
        background: #ffffff; padding: 20px; border-radius: 12px; 
        border: 1px solid #e0e0e0; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    .buy-box {{ background: #00c853; color: white; padding: 8px; border-radius: 5px; font-weight: 900; }}
    .sell-box {{ background: #ff1744; color: white; padding: 8px; border-radius: 5px; font-weight: 900; }}
    .bull-lvl {{ color: #00c853; font-weight: bold; border: 1px solid #00c853; padding: 3px; border-radius: 5px; background: #e8f5e9; }}
    .bear-lvl {{ color: #ff1744; font-weight: bold; border: 1px solid #ff1744; padding: 3px; border-radius: 5px; background: #ffebee; }}
    </style>
    """, unsafe_allow_html=True)

def get_complete_data():
    # 1. Index & Commodities
    symbols = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    main_rows = []
    for name, sym in symbols.items():
        df = yf.Ticker(sym).history(period="2d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            high = round(df['High'].max(), 2)
            low = round(df['Low'].min(), 2)
            sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
            main_rows.append({"name": name, "ltp": ltp, "sig": sig, "bull": high, "bear": low})
    
    # 2. BTST / STBT Breakout Logic
    stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS", "INFY.NS"]
    btst_rows = []
    for s in stocks:
        sdf = yf.Ticker(s).history(period="1d", interval="15m")
        if not sdf.empty:
            cur = round(sdf['Close'].iloc[-1], 2)
            day_high = round(sdf['High'].max(), 2)
            day_low = round(sdf['Low'].min(), 2)
            
            # Show only if near breakout or breakdown
            if cur >= (day_high * 0.998): 
                btst_rows.append({"SCRIPT": s.split('.')[0], "SIGNAL": "BREAKOUT 🚀", "ACTION": "BTST ✅", "LTP": cur})
            elif cur <= (day_low * 1.002):
                btst_rows.append({"SCRIPT": s.split('.')[0], "SIGNAL": "BREAKDOWN 📉", "ACTION": "STBT ❌", "LTP": cur})
    
    return main_rows, pd.DataFrame(btst_rows)

# --- UI DISPLAY ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#1a237e;'>🦅 TRADEX PRO V70 | BTST SPECIAL</h2>", unsafe_allow_html=True)

# Sidebar PCR
with st.sidebar:
    st.markdown(f"<div class='pcr-card'><div style='color:#666;'>PCR VALUE</div><div style='color:{sent_color}; font-size:28px; font-weight:900;'>{pcr_val}</div><div style='background:{sent_color}; color:white; border-radius:5px;'>{'BEARISH' if pcr_val < 0.85 else 'BULLISH'}</div></div>", unsafe_allow_html=True)

m_data, b_data = get_complete_data()

# Render Top Cards
cols = st.columns(4)
for i, item in enumerate(m_data):
    with cols[i]:
        box = "buy-box" if item['sig'] == "BUY" else "sell-box"
        st.markdown(f"""<div class='price-card'>
            <div style='color:#888; font-size:12px;'>{item['name']}</div>
            <div style='font-size:32px; font-weight:900;'>{item['ltp']}</div>
            <div class='{box}'>{item['sig']}</div>
            <div style='margin-top:10px;' class='bull-lvl'>BULLISH ABOVE: {item['bull']}</div>
            <div class='bear-lvl'>BEARISH BELOW: {item['bear']}</div>
        </div>""", unsafe_allow_html=True)

# BTST Table
st.markdown("<br><h3 style='color:#1a237e;'>🚀 BTST / STBT BREAKOUT SCANNER</h3>", unsafe_allow_html=True)
if not b_data.empty:
    st.table(b_data)
else:
    st.info("No stocks currently in Breakout zone. Scanner is active...")

time.sleep(10)
st.rerun()
