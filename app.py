import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- PAGE CONFIG ---
st.set_page_config(page_title="TRADEX LIVE TERMINAL", layout="wide")

# --- CUSTOM CSS (Purana + Naya Styling) ---
st.markdown("""
    <style>
    .live-clock {
        font-size: 35px; font-weight: 900; color: #d32f2f;
        text-align: right; padding-right: 20px;
        font-family: 'Courier New', Courier, monospace;
    }
    .ticker-wrap {
        width: 100%; overflow: hidden; background-color: #1a237e; 
        color: white; padding: 10px 0; font-weight: bold; margin-bottom: 20px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: ticker 30s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .compact-card {
        background: white; border-radius: 8px; padding: 12px 18px;
        margin-bottom: 6px; border-left: 10px solid #1a237e;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stock-name { font-size: 28px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 32px !important; font-weight: 900; color: #000; margin: 0; }
    .signal-label {
        padding: 6px 12px; border-radius: 4px; font-size: 16px;
        font-weight: 900; color: white; text-align: center;
    }
    .bg-buy { background-color: #2e7d32; }
    .bg-sell { background-color: #c62828; }
    .btst-card { background: #f3e5f5; border: 2px solid #4a148c; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- TIMEZONE FIX (IST) ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_market_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        status = "BUY" if cp > ema else "SELL"
        bg = "bg-buy" if cp > ema else "bg-sell"
        color = "#2e7d32" if cp > ema else "#c62828"
        diff = cp * 0.007
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "bg": bg, "c": color}
    except: return None

# --- HEADER SECTION ---
col_t1, col_t2 = st.columns([2, 1])
with col_t1:
    st.markdown("<h1 style='margin:0;'>🚀 TRADEX MEGA TERMINAL</h1>", unsafe_allow_html=True)
with col_t2:
    st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- NEWS TICKER ---
st.markdown("""<div class="ticker-wrap"><div class="ticker">📢 MARKET UPDATE: Nifty sustaining... | 🔥 Crude Oil volatility... | ✨ Check BTST Picks... | 🚀 Happy Trading!</div></div>""", unsafe_allow_html=True)

# --- 1. INDEX STATUS (NIFTY/BANKNIFTY) ---
st.markdown("### 🎯 INDEX STATUS")
c1, c2 = st.columns(2)
for i, (name, sym) in enumerate({"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK"}.items()):
    res = get_market_data(sym)
    if res:
        with (c1 if i==0 else c2):
            st.markdown(f"""<div class='compact-card' style='border-left-color:{res['c']};'>
                <h2 style='margin:0;'>{name}</h2>
                <p class='price-bold'>{res['p']}</p>
                <p style='font-weight:bold; color:{res['c']};'>{res['s']} ABOVE {res['sl']}</p>
            </div>""", unsafe_allow_html=True)

# --- 2. BTST SPECIAL ---
st.markdown("### 🌙 BTST / STBT PICK")
btst_res = get_market_data("JINDALSTEL.NS")
if btst_res:
    st.markdown(f"""<div class='btst-card'><h2 style='color:#4a148c; margin:0;'>✨ JINDAL STEEL - {btst_res['s']}</h2><p class='price-bold'>Entry: {btst_res['p']} | Target: {btst_res['t']}</p></div>""", unsafe_allow_html=True)

# --- 3. NIFTY 100 AUTOMATIC SCANNER ---
st.markdown("### 🔥 NIFTY 100 SCANNER")
NIFTY_100 = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS", "BHARATFORG.NS", "TATAMOTORS.NS", "TCS.NS", "ICICIBANK.NS", "INFY.NS", "JSWSTEEL.NS", "AXISBANK.NS", "BAJFINANCE.NS", "LT.NS", "ITC.NS", "BHARTIARTL.NS"]

for s_sym in NIFTY_100:
    res = get_market_data(s_sym)
    if res:
        st.markdown(f"""
        <div class='compact-card' style='border-left-color:{res['c']};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:2;'><p class='stock-name'>{s_sym.split('.')[0]}</p><p class='price-bold'>₹{res['p']}</p></div>
                <div style='flex:1;'><div class='signal-label {res['bg']}'>{res['s']}</div></div>
                <div style='flex:2; text-align:right;'>
                    <p style='color:#2e7d32; font-weight:bold; margin:0;'>TGT: {res['t']}</p>
                    <p style='color:#c62828; font-weight:bold; margin:0;'>SL: {res['sl']}</p>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# --- REFRESH LOGIC ---
time.sleep(30)
st.rerun()
