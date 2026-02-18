import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 
import pandas as pd

st.set_page_config(page_title="TRADEX MEGA TERMINAL", layout="wide")

# --- CUSTOM CSS (Style aur Layout) ---
st.markdown("""
    <style>
    .live-clock { font-size: 35px; font-weight: 900; color: #d32f2f; text-align: right; }
    .compact-card { background: white; border-radius: 8px; padding: 12px 18px; margin-bottom: 6px; border-left: 10px solid #1a237e; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .stock-name { font-size: 28px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 28px !important; font-weight: 900; color: #000; margin: 0; }
    .signal-label { padding: 6px 12px; border-radius: 4px; font-size: 16px; font-weight: 900; color: white; text-align: center; }
    .bg-buy { background-color: #2e7d32; }
    .bg-sell { background-color: #c62828; }
    .btst-card { background: #f3e5f5; border: 2px solid #4a148c; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    .commodity-alert { background: #fff3e0; border: 2px dashed #ef6c00; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    .option-card { 
        background: #e3f2fd; border: 2px solid #1565c0; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }
    .sideways-card { background: #eeeeee; border: 2px solid #9e9e9e; border-radius: 10px; padding: 15px; text-align: center; font-weight: bold; color: #616161; }
    .option-name { font-size: 18px; font-weight: bold; color: #0d47a1; margin: 0; }
    .buy-level { font-size: 22px; font-weight: 900; color: #1565c0; margin: 0; }
    .zone-safe { color: #2e7d32; font-weight: bold; font-size: 14px; }
    .zone-risky { color: #ef6c00; font-weight: bold; font-size: 14px; }
    .rsi-tag { font-size: 12px; font-weight: bold; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# --- RSI & CALCULATION FUNCTIONS ---
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
        
        # Sideways detection (Price very close to EMA)
        is_sideways = abs(cp - ema) / ema < 0.001
        
        status = "SIDEWAYS" if is_sideways else ("BUY" if cp > ema else "SELL")
        color = "#9e9e9e" if is_sideways else ("#2e7d32" if cp > ema else "#c62828")
        
        df['RSI'] = calculate_rsi(df['Close'])
        rsi_val = round(df['RSI'].iloc[-1], 2)
        
        is_safe = "✅ SAFE ENTRY" if abs(cp - ema) / ema < 0.003 else "⚠️ PRICE TOO HIGH"
        zone_class = "zone-safe" if "SAFE" in is_safe else "zone-risky"
        diff = cp * 0.007
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "c": color, "zone": is_safe, "z_cls": zone_class, "rsi": rsi_val, "sw": is_sideways}
    except: return None

def get_atm_strike(price, base=100):
    return base * round(price / base)

QUALITY_LIST = ["ITC.NS", "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "SBIN.NS"]

# --- HEADER (Clock & Title) ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='live-clock'>⏰ {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<h1 style='margin:0;'>🚀 TRADEX MEGA TERMINAL</h1>", unsafe_allow_html=True)

# --- 1. MARKET STATUS (ALL 5 ASSETS) ---
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
                <p class='rsi-tag'>RSI: {res['rsi']}</p>
            </div>""", unsafe_allow_html=True)

# --- 2. EVENING BREAKOUT RADAR ---
st.markdown(f"""
    <div class='commodity-alert'>
        <h4 style='color:#ef6c00; margin:0;'>🌙 EVENING BREAKOUT RADAR (ACTIVE)</h4>
        <p style='margin:0; font-size:14px;'>Sideways assets will show 'Wait' signal below.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. STRIKE PRICE RADAR (AUTO-SIGNALS) ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
o_cols = st.columns(2)

def display_option_signal(name, res, col, base=100):
    if res:
        with col:
            if res['sw']:
                st.markdown(f"<div class='sideways-card'>😴 {name} IS SIDEWAYS<br>Wait for Breakout</div>", unsafe_allow_html=True)
            elif res['s'] == "BUY":
                strike = get_atm_strike(res['p'], base)
                st.markdown(f"""<div class='option-card'>
                    <p class='option-name'>{name} {strike} CE</p>
                    <p class='buy-level'>BUY ABOVE: {res['p']} 👁️🙏</p>
                </div>""", unsafe_allow_html=True)

display_option_signal("SENSEX", results.get("SENSEX"), o_cols[0], 100)
display_option_signal("NIFTY", results.get("NIFTY"), o_cols[1], 50)
display_option_signal("CRUDE", results.get("CRUDE OIL"), st, 50)

# --- 4. BTST / STBT SCANNER ---
st.markdown("### 🌙 BTST / STBT TOP PICKS")
NIFTY_100 = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS", "BHARATFORG.NS", "TATAMOTORS.NS", "TCS.NS", "ICICIBANK.NS", "INFY.NS", "JSWSTEEL.NS", "AXISBANK.NS", "BAJFINANCE.NS", "LT.NS", "ITC.NS", "BHARTIARTL.NS"]
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
            st.markdown(f"""<div class='btst-card'><h2 style='color:#4a148c; margin:0;'>✨ {name} - BTST</h2>
                <p class='price-bold'>Entry: {data['p']} | Tgt: {data['t']}</p>
                <p class='{data['z_cls']}'>{data['zone']}</p></div>""", unsafe_allow_html=True)

st.divider()

# --- 5. NIFTY 100 LIVE SCANNER ---
st.markdown("### 🔥 NIFTY 100 LIVE SCANNER")
for s_sym, res in stock_results:
    star = "⭐ " if s_sym in QUALITY_LIST else ""
    st.markdown(f"""
    <div class='compact-card' style='border-left-color:{res['c']};'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div style='flex:2;'>
                <p class='stock-name'>{star}{s_sym.split('.')[0]}</p>
                <p class='price-bold'>₹{res['p']}</p>
                <p class='{res['z_cls']}'>{res['zone']}</p>
            </div>
            <div style='flex:1;'><div class='signal-label {res['bg'] if not res['sw'] else ""}' style='background-color:{res['c']}'>{res['s']}</div></div>
            <div style='flex:2; text-align:right;'>
                <p style='color:#2e7d32; font-weight:bold; margin:0;'>TGT: {res['t']}</p>
                <p style='color:#c62828; font-weight:bold; margin:0;'>SL: {res['sl']}</p>
                <p class='rsi-tag'>RSI: {res['rsi']}</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
