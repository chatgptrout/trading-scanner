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
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }
    .sideways-card { background: #eeeeee; border: 2px solid #9e9e9e; border-radius: 10px; padding: 15px; text-align: center; font-weight: bold; color: #616161; }
    .buy-level { font-size: 22px; font-weight: 900; color: #1565c0; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- RSI & SIDEWAYS LOGIC ---
def get_market_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        # Sideways logic: If price is within 0.1% of EMA
        is_sideways = abs(cp - ema) / ema < 0.001
        
        status = "SIDEWAYS" if is_sideways else ("BUY" if cp > ema else "SELL")
        color = "#9e9e9e" if is_sideways else ("#2e7d32" if cp > ema else "#c62828")
        
        is_safe = "✅ SAFE ENTRY" if abs(cp - ema) / ema < 0.003 else "⚠️ PRICE TOO HIGH"
        return {"p": cp, "s": status, "sl": ema, "zone": is_safe, "c": color, "sw": is_sideways}
    except: return None

def get_atm_strike(price, base=100):
    return base * round(price / base)

# --- HEADER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='live-clock'>⏰ {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<h1>🚀 TRADEX MEGA TERMINAL</h1>", unsafe_allow_html=True)

# --- 1. MARKET STATUS (SENSEX, NIFTY, CRUDE, NG, GOLD) ---
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
            </div>""", unsafe_allow_html=True)

# --- 2. STRIKE PRICE RADAR (DASHBOARD) ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
o_cols = st.columns(3)

def show_signal(name, res, col, base=100):
    if res:
        with col:
            if res['sw']:
                st.markdown(f"<div class='sideways-card'>😴 {name} IS SIDEWAYS<br>Wait for Breakout</div>", unsafe_allow_html=True)
            elif res['s'] == "BUY":
                strike = get_atm_strike(res['p'], base)
                st.markdown(f"""<div class='option-card'>
                    <p style='font-weight:bold;margin:0;'>{name} {strike} CE</p>
                    <p class='buy-level'>BUY ABOVE: {res['p']} 👁️🙏</p>
                </div>""", unsafe_allow_html=True)

show_signal("SENSEX", results.get("SENSEX"), o_cols[0], 100)
show_signal("NIFTY", results.get("NIFTY"), o_cols[1], 50)
show_signal("CRUDE", results.get("CRUDE OIL"), o_cols[2], 50)

st.divider()
# ... (Baaki BTST aur Nifty 100 Scanner code niche waise hi chalta rahega) ...
time.sleep(30)
st.rerun()
