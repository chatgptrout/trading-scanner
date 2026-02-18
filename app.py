import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MEGA TERMINAL", layout="wide")

# --- CUSTOM CSS (Pure Original Design) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .live-clock { font-size: 40px; font-weight: 900; color: #ff5252; text-align: right; font-family: 'Courier New', monospace; }
    
    /* Index Cards */
    .status-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; border-left: 8px solid #1a237e; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .card-bullish { border-left-color: #2e7d32 !important; background-color: #f1f8e9; }
    .card-bearish { border-left-color: #c62828 !important; background-color: #ffebee; }
    .card-danger { border-left-color: #d32f2f !important; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.7; } }

    /* BTST Section */
    .btst-container { background: #fffde7; border: 2px dashed #fbc02d; border-radius: 15px; padding: 20px; margin-top: 30px; }
    .btst-card { background: white; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #fbc02d; display: flex; justify-content: space-between; align-items: center; box-shadow: 3px 3px 10px rgba(0,0,0,0.05); }

    /* Global Text Styles */
    .price-text { font-size: 24px; font-weight: 900; color: #212121; }
    .tgt-text { color: #2e7d32; font-weight: 900; }
    .sl-text { color: #c62828; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_market_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        status = "BULLISH" if cp > ema else "BEARISH"
        return {"p": cp, "ema": ema, "rsi": rsi, "status": status}
    except: return None

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1: st.markdown("# 🚀 TRADEX MEGA TERMINAL")
with c2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- 1. INDEX STATUS ---
st.markdown("### 🎯 INDEX & COMMODITY STATUS")
m_cols = st.columns(4)
assets = {"SENSEX": "^BSESN", "NIFTY": "^NSEI", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_market_data(sym)
    results[name] = res
    if res:
        card_class = "status-card"
        msg = f"{res['status']} ABOVE {res['ema']}" if res['status'] == "BULLISH" else f"{res['status']} BELOW {res['ema']}"
        if res['rsi'] > 80: card_class += " card-danger"; msg = "⚠️ CRITICAL OVERBOUGHT"
        elif res['status'] == "BULLISH": card_class += " card-bullish"
        else: card_class += " card-bearish"
        with m_cols[i]:
            st.markdown(f"<div class='{card_class}'><p style='color:#757575; font-weight:bold; margin:0;'>{name}</p><p style='font-size:28px; font-weight:900; margin:0;'>{res['p']}</p><p style='font-size:12px; font-weight:bold;'>{msg}</p></div>", unsafe_allow_html=True)

# --- 2. RADAR ---
st.markdown("### 🔥 STRIKE PRICE RADAR")
r_cols = st.columns(3)
def render_radar(name, data, col, strike):
    if data:
        with col:
            st.markdown(f"<div style='background:#e3f2fd; border:1px solid #1565c0; border-radius:5px; padding:12px; display:flex; justify-content:space-between; align-items:center;'><div>{strike}</div><div style='color:#1565c0; font-weight:bold;'>BUY ABOVE: {data['p']} 👁️🙏</div></div>", unsafe_allow_html=True)

render_radar("NIFTY", results.get("NIFTY"), r_cols[0], "NIFTY 25800 CE")
render_radar("SENSEX", results.get("SENSEX"), r_cols[1], "SENSEX 83700 CE")

# --- 3. NIFTY 100 SCANNER ---
st.markdown("### 🔥 NIFTY 100 LIVE SCANNER")
for sym in ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]:
    res = get_market_data(sym)
    if res:
        st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #eee; padding:15px;'><div style='flex:2;'><div style='font-size:20px; font-weight:900;'>⭐ {sym.split('.')[0]}</div><div class='price-text'>₹{res['p']}</div></div><div style='flex:1; text-align:right;'><p class='tgt-text'>TGT: {round(res['p']*1.007, 2)}</p><p class='sl-text'>SL: {res['ema']}</p></div></div>", unsafe_allow_html=True)

# --- 4. BTST SCANNER (THE MISSING PIECE) ---
st.markdown("<div class='btst-container'><h3>💰 BTST / SWING TRADING ALERTS</h3>", unsafe_allow_html=True)
BTST_STOCKS = ["TCS.NS", "INFY.NS", "ICICIBANK.NS"]
for sym in BTST_STOCKS:
    res = get_market_data(sym)
    if res and res['status'] == "BULLISH":
        st.markdown(f"""
        <div class='btst-card'>
            <div><b style='font-size:18px;'>🚀 {sym.split('.')[0]}</b><br><span style='color:#757575;'>Potential BTST Pick</span></div>
            <div style='text-align:right;'><span class='price-text'>₹{res['p']}</span><br><span style='color:#2e7d32; font-weight:bold;'>STRENGTH: HIGH</span></div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
