import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 
import pandas as pd

st.set_page_config(page_title="TRADEX MEGA TERMINAL", layout="wide")

# --- CUSTOM CSS (Purana Layout + Naya Color Logic) ---
st.markdown("""
    <style>
    .live-clock { font-size: 35px; font-weight: 900; color: #d32f2f; text-align: right; }
    /* Green Card for Safe Buy */
    .buy-card { background: #e8f5e9; border: 3px solid #2e7d32; border-radius: 8px; padding: 15px; margin-bottom: 8px; }
    /* Red Card for RSI Danger */
    .danger-card { background: #ffebee; border: 3px solid #c62828; border-radius: 8px; padding: 15px; margin-bottom: 8px; animation: blinker 1.5s linear infinite; }
    /* Normal Card */
    .compact-card { background: white; border-radius: 8px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    
    @keyframes blinker { 50% { opacity: 0.7; } }
    .stock-name { font-size: 24px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 26px !important; font-weight: 900; color: #000; margin: 0; }
    .signal-label { padding: 6px 12px; border-radius: 4px; font-size: 14px; font-weight: 900; color: white; text-align: center; width: 85px; }
    .tgt-text { color: #2e7d32 !important; font-weight: 900; margin: 0; font-size: 16px; }
    .sl-text { color: #c62828 !important; font-weight: 900; margin: 0; font-size: 16px; }
    .level-msg { font-size: 14px; font-weight: 900; margin-top: 2px; }
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
        df['RSI'] = calculate_rsi(df['Close'])
        rsi_val = round(df['RSI'].iloc[-1], 2)
        
        is_sw = abs(cp - ema) / ema < 0.001
        is_danger = rsi_val > 80
        status = "SIDEWAYS" if is_sw else ("BUY" if cp > ema else "SELL")
        
        # Style Selection
        if is_danger: card_style = "danger-card"; text_col = "#c62828"
        elif status == "BUY": card_style = "buy-card"; text_col = "#2e7d32"
        else: card_style = "compact-card"; text_col = "#1a237e"
        
        diff = cp * 0.007
        is_safe = "✅ SAFE ENTRY" if abs(cp - ema) / ema < 0.003 else "⚠️ PRICE TOO HIGH"
        
        return {"p": cp, "s": status, "sl": ema, "t": round(cp + (diff if cp > ema else -diff), 2),
                "rsi": rsi_val, "style": card_style, "c": text_col, "danger": is_danger, "zone": is_safe}
    except: return None

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
        msg = "⚠️ CRITICAL OVERBOUGHT" if res['danger'] else (f"{res['s']} ABOVE {res['sl']}")
        with m_cols[i]:
            st.markdown(f"""<div class='{res['style']}'>
                <h4 style='margin:0;'>{name}</h4>
                <p class='price-bold'>{res['p']}</p>
                <p class='level-msg' style='color:{res['c']};'>{msg}</p>
                <p style='font-size:12px; font-weight:bold;'>RSI: {res['rsi']}</p>
            </div>""", unsafe_allow_html=True)

# --- 2. STRIKE PRICE RADAR ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
o_cols = st.columns(3)
def display_option(name, res, col):
    if res:
        with col:
            if res['danger']: 
                st.markdown(f"<div style='background:#ffebee; border:2px solid #c62828; padding:12px; border-radius:10px; color:#c62828;'><b>{name}: DANGER (RSI {res['rsi']})</b></div>", unsafe_allow_html=True)
            elif res['s'] == "BUY":
                st.markdown(f"<div style='background:#e8f5e9; border:2px solid #2e7d32; padding:12px; border-radius:10px; color:#2e7d32;'><b>{name} Signal</b><br>BUY ABOVE: {res['p']} 👁️🙏</div>", unsafe_allow_html=True)

display_option("SENSEX", results.get("SENSEX"), o_cols[0])
display_option("NIFTY", results.get("NIFTY"), o_cols[1])
display_option("CRUDE", results.get("CRUDE OIL"), o_cols[2])

# --- 3. NIFTY
