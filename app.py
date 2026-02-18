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
    .compact-card { background: white; border-radius: 8px; padding: 12px 18px; margin-bottom: 6px; border-left: 10px solid #1a237e; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .price-bold { font-size: 28px !important; font-weight: 900; color: #000; margin: 0; }
    .option-card { 
        background: #e3f2fd; border: 2px solid #1565c0; border-radius: 10px; 
        padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }
    .sideways-card { background: #eeeeee; border: 2px solid #9e9e9e; border-radius: 10px; padding: 12px; text-align: center; font-weight: bold; color: #616161; }
    .buy-level { font-size: 20px; font-weight: 900; color: #1565c0; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
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
        is_sideways = abs(cp - ema) / ema < 0.001
        status = "SIDEWAYS" if is_sideways else ("BUY" if cp > ema else "SELL")
        df['RSI'] = calculate_rsi(df['Close'])
        rsi_val = round(df['RSI'].iloc[-1], 2)
        is_safe = "✅ SAFE ENTRY" if abs(cp - ema) / ema < 0.003 else "⚠️ PRICE TOO HIGH"
        return {"p": cp, "s": status, "sl": ema, "c": "#9e9e9e" if is_sideways else ("#2e7d32" if cp > ema else "#c62828"), "zone": is_safe, "rsi": rsi_val, "sw": is_sideways}
    except: return None

def get_atm_strike(price, base=100):
    return int(base * round(price / base))

QUALITY_LIST = ["ITC.NS", "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "SBIN.NS"]

# --- HEADER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='live-clock'>⏰ {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<h1>🚀 TRADEX MEGA TERMINAL</h1>", unsafe_allow_html=True)

# --- 1. MARKET STATUS ---
st.markdown("### 🎯 INDEX & COMMODITY STATUS")
m_cols = st.columns(5)
assets = {"SENSEX": "^BSESN", "NIFTY": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_market_data(sym)
    results[name] = res
    if res:
        with m_cols[i]:
            st.markdown(f"""<div class='compact-card' style='border-left-color:{res['c']};'>
                <h4 style='margin:0;'>{name}</h4>
                <p class='price-bold'>{res['p']}</p>
                <p style='font-weight:bold; color:{res['c']};'>{res['s']}</p>
                <p style='font-size:12px;'>RSI: {res['rsi']}</p>
            </div>""", unsafe_allow_html=True)

# --- 2. EVENING BREAKOUT RADAR ---
st.markdown("<div class='commodity-alert'><h4 style='color:#ef6c00; margin:0;'>🌙 EVENING BREAKOUT RADAR (ACTIVE)</h4></div>", unsafe_allow_html=True)

# --- 3. STRIKE PRICE RADAR (AUTO-SIGNALS) ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
o_cols = st.columns(3) # Fix: Changed to 3 columns for Sensex, Nifty, Crude

def display_option_signal(name, res, col, base=100):
    if res:
        with col:
            if res['sw']:
                st.markdown(f"<div class='sideways-card'>😴 {name} SIDEWAYS</div>", unsafe_allow_html=True)
            elif res['s'] == "BUY":
                strike = get_atm_strike(res['p'], base)
                st.markdown(f"""<div class='option-card'>
                    <p class='option-name'>{name} {strike} CE</p>
                    <p class='buy-level'>BUY ABOVE: {res['p']} 👁️🙏</p>
                </div>""", unsafe_allow_html=True)

display_option_signal("SENSEX", results.get("SENSEX"), o_cols[0], 100)
display_option_signal("NIFTY", results.get("NIFTY"), o_cols[1], 50)
display_option_signal("CRUDE", results.get("CRUDE OIL"), o_cols[2], 50) # Error Fixed Here

# --- 4. BTST & 100 SCANNER ---
st.markdown("### 🌙 BTST / STBT TOP PICKS")
NIFTY_100 = ["RELIANCE.NS", "HDFCBANK.NS", "SBIN.NS", "BHARATFORG.NS", "TATAMOTORS.NS", "TCS.NS", "ICICIBANK.NS", "INFY.NS"]
btst_list = []
stock_results = []
for s_sym in NIFTY_100:
    res = get_market_data(s_sym)
    if res:
        stock_results.append((s_sym, res))
        if res['s'] == "BUY":
            star = "⭐" if s_sym in QUALITY_LIST else ""
            btst_list.append((f"{star}{s_sym.split('.')[0]}", res))

if btst_list:
    b_col1, b_col2 = st.columns(2)
    for i in range(min(2, len(btst_list))):
        name, data = btst_list[i]
        with (b_col1 if i==0 else b_col2):
            st.markdown(f"<div class='btst-card'><h2 style='color:#4a148c; margin:0;'>✨ {name} - BTST</h2><p class='price-bold'>Entry: {data['p']}</p></div>", unsafe_allow_html=True)

st.divider()
st.markdown("### 🔥 NIFTY 100 LIVE SCANNER")
for s_sym, res in stock_results:
    star = "⭐ " if s_sym in QUALITY_LIST else ""
    st.markdown(f"""<div class='compact-card' style='border-left-color:{res['c']};'><p class='stock-name'>{star}{s_sym.split('.')[0]}</p><p class='price-bold'>₹{res['p']}</p><p class='{res['z_cls'] if 'z_cls' in res else ""}'>{res['zone']}</p></div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
