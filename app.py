import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 
import pandas as pd

st.set_page_config(page_title="TRADEX MEGA TERMINAL", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .live-clock { font-size: 35px; font-weight: 900; color: #d32f2f; text-align: right; }
    .compact-card { background: white; border-radius: 8px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .stock-name { font-size: 24px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 26px !important; font-weight: 900; color: #000; margin: 0; }
    .signal-label { padding: 6px 12px; border-radius: 4px; font-size: 14px; font-weight: 900; color: white; text-align: center; width: 85px; }
    .option-card { background: #e3f2fd; border: 2px solid #1565c0; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .buy-level { font-size: 18px; font-weight: 900; color: #1565c0; margin: 0; }
    .tgt-text { color: #2e7d32 !important; font-weight: 900; margin: 0; font-size: 16px; }
    .sl-text { color: #c62828 !important; font-weight: 900; margin: 0; font-size: 16px; }
    .level-msg { font-size: 14px; font-weight: 900; margin-top: 2px; margin-bottom: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FUNCTIONS ---
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_market_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        is_sw = abs(cp - ema) / ema < 0.001
        status = "SIDEWAYS" if is_sw else ("BUY" if cp > ema else "SELL")
        df['RSI'] = calculate_rsi(df['Close'])
        rsi_val = round(df['RSI'].iloc[-1], 2)
        is_safe = "✅ SAFE ENTRY" if abs(cp - ema) / ema < 0.003 else "⚠️ PRICE TOO HIGH"
        diff = cp * 0.007
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, 
                "c": "#9e9e9e" if is_sw else ("#2e7d32" if cp > ema else "#c62828"), 
                "zone": is_safe, "rsi": rsi_val, "sw": is_sw}
    except: return None

def get_atm_strike(price, base=100):
    return int(base * round(price / base))

QUALITY_LIST = ["ITC.NS", "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "SBIN.NS"]

# --- HEADER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='live-clock'>⏰ {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<h1>🚀 TRADEX MEGA TERMINAL</h1>", unsafe_allow_html=True)

# --- 1. MARKET STATUS (BULLISH/BEARISH MSG RESTORED) ---
st.markdown("### 🎯 INDEX & COMMODITY STATUS")
m_cols = st.columns(5)
assets = {"SENSEX": "^BSESN", "NIFTY": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_market_data(sym)
    results[name] = res
    if res:
        msg = "BULLISH ABOVE" if res['s'] == "BUY" else "BEARISH BELOW"
        if res['sw']: msg = "SIDEWAYS"
        with m_cols[i]:
            st.markdown(f"""<div class='compact-card' style='border-left-color:{res['c']};'>
                <h4 style='margin:0;'>{name}</h4>
                <p class='price-bold'>{res['p']}</p>
                <p class='level-msg' style='color:{res['c
