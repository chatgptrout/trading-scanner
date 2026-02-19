import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- CONFIG ---
st.set_page_config(page_title="NIFTY 50 BREAKOUT PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-clock { font-size: 32px; font-weight: 900; color: #00ff00; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
    .index-box { background: #1e1e1e; border-radius: 12px; padding: 15px; margin-bottom: 8px; border-left: 8px solid #1a237e; }
    .breakout-card { background: #1e1e1e; border-radius: 15px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #00ff00; border-right: 10px solid #00ff00; }
    .price-large { font-size: 26px; font-weight: 900; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
def get_breakout_data(ticker, is_mcx=False):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        ltp = data['Close'].iloc[-1]
        
        # MCX Match Logic (Purana Wala)
        if ticker == "CL=F": ltp = ltp * 84.50 
        elif ticker == "NG=F": ltp = ltp * 84.50 * 1.26
            
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if is_mcx: ema = ema * 84.50 * (1.26 if ticker=="NG=F" else 1)
        
        # Breakout Condition
        is_breakout = ltp > ema and data['Close'].iloc[-2] <= ema
        return {"p": round(ltp, 2), "ema": round(ema, 2), "breakout": is_breakout, "bull": ltp > ema}
    except: return None

# --- UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🎯 BREAKOUT LIVE: {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. PURANA SECTION (Nifty, Bank Nifty, Crude, NG)
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
for name, sym in indices.items():
    res = get_breakout_data(sym, is_mcx=("F" in sym))
    if res:
        color = "#00ff00" if res['bull'] else "#ff4444"
        st.markdown(f"<div class='index-box' style='border-left-color:{color};'><b>{name}</b><div style='display:flex; justify-content:space-between;'><span class='price-large'>₹{res['p']}</span><span style='color:{color}; font-weight:bold;'>EMA: {res['ema']}</span></div></div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🔥 NIFTY 50 BREAKOUT STOCKS")

# Full Nifty 50 Breakout Scan List
NIFTY_SCAN = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LTIM.NS", "AXISBANK.NS", "ADANIENT.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", "KOTAKBANK.NS", "M&M.NS", "NTPC.NS", "TITAN.NS"]

found = False
for s in NIFTY_SCAN:
    val = get_breakout_data(s)
    if val and val['breakout']:
        found = True
        st.markdown(f"""
        <div class='breakout-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div><span style='background:#00ff00; color:black; padding:2px 5px; border-radius:3px; font-size:10px; font-weight:bold;'>BREAKOUT</span><br><b style='font-size:20px;'>{s.split('.')[0]}</b></div>
                <div style='text-align:right;'><span class='price-large'>₹{val['p']}</span><br><small style='color:#00ff00;'>Above EMA {val['ema']}</small></div>
            </div>
        </div>""", unsafe_allow_html=True)

if not found:
    st.info("Market Scanning... No fresh Nifty 50 breakouts in this 15m candle.")

time.sleep(30)
st.rerun()
