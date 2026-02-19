import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. SETTINGS & NEW TABLE THEME ---
st.set_page_config(page_title="TRADEX PRO V17", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; margin-bottom: 20px; }
    
    /* SIGNAL TABLE STYLING */
    .signal-header { background: #f8f9fa; padding: 10px; border-bottom: 2px solid #eee; display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; color: #757575; }
    .signal-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 10px; border-bottom: 1px solid #f0f0f0; }
    .script-name { font-weight: 800; font-size: 14px; color: #121212; width: 40%; }
    .signal-badge { background: #e8f0fe; color: #1a73e8; padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .signal-level { font-weight: 700; font-size: 13px; color: #424242; width: 40%; text-align: right; }

    /* Scanner & BTST Styling */
    .scanner-box { background: white; border-radius: 12px; padding: 15px; margin-top: 10px; border-left: 10px solid #2e7d32; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

def fetch_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        return {"p": cp, "ema": ema, "is_bull": cp > ema}
    except: return None

# --- 2. HEADER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# --- 3. LIVE SIGNAL TABLE (AS PER YOUR SCREENSHOT) ---
st.markdown("### TRADEX <span style='background:#ff5252; color:white; padding:2px 8px; border-radius:4px; font-size:12px;'>LIVE</span>", unsafe_allow_html=True)
st.markdown("<div class='signal-header'><span>SCRIPT</span><span>SIGNAL</span><span style='text-align:right;'>LEVELS</span></div>", unsafe_allow_html=True)

indices = {"CRUDEOIL FEB FUTURE": "CL=F", "NIFTY": "^NSEI", "SENSEX": "^BSESN", "NATURAL GAS": "NG=F"}

for name, sym in indices.items():
    res = fetch_data(sym)
    if res:
        color = "#2e7d32" if res['is_bull'] else "#c62828"
        status = "BULLISH ABOVE" if res['is_bull'] else "BEARISH BELOW"
        st.markdown(f"""
        <div class='signal-row'>
            <div class='script-name'>{name}</div>
            <div><span class='signal-badge'>SIGNAL</span></div>
            <div class='signal-level' style='color:{color};'>{status} {res['ema']}</div>
        </div>""", unsafe_allow_html=True)

# --- 4. LIVE INSTITUTIONAL SCANNER ---
st.markdown("<br>### 📊 LIVE SCANNER", unsafe_allow_html=True)
for s in ["RELIANCE.NS", "HDFCBANK.NS", "SBIN.NS", "ADANIENT.NS"]:
    val = fetch_data(s)
    if val:
        s_color = "#2e7d32" if val['is_bull'] else "#c62828"
        st.markdown(f"""
        <div class='scanner-box' style='border-left-color: {s_color};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div><b>⭐ {s.split('.')[0]}</b><br><span style='font-size:22px; font-weight:900;'>₹{val['p']}</span></div>
                <div style='text-align:right; color:#2e7d32; font-weight:900;'>TGT: {round(val['p']*1.008, 2)}<br><span style='color:#c62828;'>SL: {val['ema']}</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
