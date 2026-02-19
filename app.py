import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="NIFTY BREAKOUT HUNTER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-clock { font-size: 35px; font-weight: 900; color: #00ff00; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
    .breakout-card { background: #1e1e1e; border-radius: 15px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #00ff00; box-shadow: 0 4px 15px rgba(0,255,0,0.1); }
    .breakout-price { font-size: 28px; font-weight: 900; color: #ffffff; }
    .signal-tag { background: #00ff00; color: black; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BREAKOUT ENGINE ---
def find_breakouts(ticker):
    try:
        # Fetching 15m interval data for intraday breakout
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        
        ltp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        prev_close = round(df['Close'].iloc[-2], 2)
        
        # Breakout Condition: Current Price is above EMA AND just crossed it
        is_breakout = ltp > ema and prev_close <= ema
        
        return {"p": ltp, "ema": ema, "is_breakout": is_breakout}
    except: return None

# --- 3. UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🎯 BREAKOUT LIVE: {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# Top Indices Status (Short & Sweet)
st.columns(2)[0].metric("NIFTY 50", yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1].round(2))
st.columns(2)[1].metric("BANK NIFTY", yf.Ticker("^NSEBANK").history(period="1d")['Close'].iloc[-1].round(2))

st.markdown("---")
st.markdown("### 🔥 NIFTY 50 BREAKOUT ALERTS")

# Main Nifty 50 Heavyweights to Scan
NIFTY_50_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
    "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LTIM.NS", "AXISBANK.NS",
    "ADANIENT.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", "KOTAKBANK.NS"
]

found_any = False
for stock in NIFTY_50_STOCKS:
    res = find_breakouts(stock)
    if res and res['is_breakout']:
        found_any = True
        st.markdown(f"""
        <div class='breakout-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span class='signal-tag'>BREAKOUT DETECTED</span>
                    <h2 style='margin:0;'>{stock.split('.')[0]}</h2>
                </div>
                <div style='text-align:right;'>
                    <div class='breakout-price'>₹{res['p']}</div>
                    <div style='color:#00ff00; font-weight:bold;'>EMA Support: {res['ema']}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

if not found_any:
    st.warning("Market Scanning... No fresh Nifty 50 breakouts in the last 15 mins. Check EMA levels.")

time.sleep(30)
st.rerun()
