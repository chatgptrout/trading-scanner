import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V67", layout="wide")

# --- WHITE THEME & SMART UI ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #333; }
    .price-card { 
        background: white; padding: 20px; border-radius: 15px; 
        border: 1px solid #e0e0e0; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .buy-btn { background: #00c853; color: white; padding: 8px 20px; border-radius: 8px; font-weight: 900; }
    .sell-btn { background: #ff1744; color: white; padding: 8px 20px; border-radius: 8px; font-weight: 900; }
    .level-box { font-size: 13px; margin-top: 8px; font-weight: bold; border-radius: 5px; padding: 4px; }
    .bull-lvl { color: #00c853; border: 1px solid #00c853; }
    .bear-lvl { color: #ff1744; border: 1px solid #ff1744; }
    </style>
    """, unsafe_allow_html=True)

def get_pro_scanner():
    symbols = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    main_data = []
    for name, sym in symbols.items():
        df = yf.Ticker(sym).history(period="5d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            high = round(df['High'].max(), 2)
            low = round(df['Low'].min(), 2)
            sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
            main_data.append({"name": name, "ltp": ltp, "sig": sig, "bull": high, "bear": low})
    
    # BTST / Breakout Logic for Stocks
    stocks = {"RELIANCE.NS": "RELIANCE", "TCS.NS": "TCS", "HDFCBANK.NS": "HDFCBANK", "SBIN.NS": "SBIN"}
    scanner_rows = []
    for sym, name in stocks.items():
        s_df = yf.Ticker(sym).history(period="2d", interval="15m")
        if not s_df.empty:
            s_ltp = round(s_df['Close'].iloc[-1], 2)
            s_high = round(s_df['High'].max(), 2)
            # Breakout condition: LTP within 0.5% of high
            if s_ltp >= (s_high * 0.995):
                scanner_rows.append({"Script": name, "Signal": "BREAKOUT 🚀", "Action": "BTST ✅", "LTP": s_ltp})
            # STBT condition: LTP near low
            elif s_ltp <= (s_df['Low'].min() * 1.005):
                scanner_rows.append({"Script": name, "Signal": "BREAKDOWN 📉", "Action": "STBT ❌", "LTP": s_ltp})
    
    return main_data, pd.DataFrame(scanner_rows)

# Header
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#1a237e;'>🦅 TRADEX PRO V67 | PRO SCANNER</h2>", unsafe_allow_html=True)

m_data, s_data = get_pro_scanner()

# Top 4 Cards
cols = st.columns(4)
for i, item in enumerate(m_data):
    with cols[i]:
        btn = "buy-btn" if item['sig'] == "BUY" else "sell-btn"
        st.markdown(f"""<div class='price-card'>
            <div style='color:#666; font-size:12px;'>{item['name']}</div>
            <div style='font-size:32px; font-weight:900;'>{item['ltp']}</div>
            <div class='{btn}'>{item['sig']}</div>
            <div class='level-box bull-lvl'>BULLISH ABOVE: {item['bull']}</div>
            <div class='level-box bear-lvl'>BEARISH BELOW: {item['bear']}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><h3 style='color:#1a237e;'>🚀 BTST / STBT & BREAKOUT WATCHLIST</h3>", unsafe_allow_html=True)
if not s_data.empty:
    st.dataframe(s_data, use_container_width=True, hide_index=True)
else:
    st.write("No Breakouts detected currently. Waiting for high momentum...")

time.sleep(10)
st.rerun()
