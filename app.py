import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MEGA V4", layout="wide")

# --- CUSTOM CSS (Premium High-Contrast Design) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .live-clock { font-size: 42px; font-weight: 900; color: #ff5252; text-align: right; text-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    
    /* Premium Index Cards */
    .status-card { background: #ffffff; border-radius: 15px; padding: 20px; border-bottom: 5px solid #1a237e; box-shadow: 0 10px 20px rgba(0,0,0,0.05); transition: 0.3s; }
    .status-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
    .card-bullish { border-bottom-color: #2e7d32 !important; }
    .card-bearish { border-bottom-color: #c62828 !important; }
    .card-danger { border-bottom-color: #ff5252 !important; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 82, 82, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(255, 82, 82, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 82, 82, 0); } }

    /* Strike Price Radar Modern */
    .radar-box { background: #ffffff; border: 2px solid #e0e0e0; border-left: 10px solid #1565c0; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 2px 4px 10px rgba(0,0,0,0.03); }
    .radar-danger { border-left-color: #ff5252; background: #fff5f5; color: #c62828; font-weight: 900; }

    /* Compact Scanner Rows */
    .scanner-card { background: white; border-radius: 12px; padding: 18px; margin-bottom: 12px; border: 1px solid #efefef; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
    .stock-info { display: flex; flex-direction: column; gap: 2px; }
    .stock-title { font-size: 24px; font-weight: 900; color: #1a237e; margin: 0; }
    .price-main { font-size: 28px; font-weight: 900; color: #212121; margin: 0; }
    
    /* BTST Gold Section */
    .btst-vip { background: linear-gradient(135deg, #fffde7 0%, #fff9c4 100%); border: 2px solid #fbc02d; border-radius: 20px; padding: 25px; margin-top: 35px; }
    .btst-item { background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; border-right: 8px solid #fbc02d; box-shadow: 2px 4px 8px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_pro_data(ticker):
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
        return {"p": cp, "ema": ema, "rsi": rsi, "status": "BULLISH" if cp > ema else "BEARISH"}
    except: return None

# --- UI HEADER ---
c1, c2 = st.columns([3, 1])
with c1: st.markdown("# 💎 TRADEX ULTIMATE V4")
with c2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- 1. INDEX STATUS (The Premium Look) ---
m_cols = st.columns(4)
assets = {"SENSEX": "^BSESN", "NIFTY": "^NSEI", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_pro_data(sym)
    results[name] = res
    if res:
        style = "status-card"
        msg = f"📈 BULLISH > {res['ema']}" if res['status'] == "BULLISH" else f"📉 BEARISH < {res['ema']}"
        if res['rsi'] > 80: style += " card-danger"; msg = "🚨 CRITICAL OVERBOUGHT"
        elif res['status'] == "BULLISH": style += " card-bullish"
        else: style += " card-bearish"
        with m_cols[i]:
            st.markdown(f"<div class='{style}'><p style='color:#757575; font-weight:bold; margin:0;'>{name}</p><p style='font-size:32px; font-weight:900; margin:0;'>{res['p']}</p><p style='color:#424242; font-size:13px; font-weight:bold;'>{msg}</p><p style='font-size:11px; color:#9e9e9e;'>RSI: {res['rsi']}</p></div>", unsafe_allow_html=True)

# --- 2. STRIKE PRICE RADAR ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
r_cols = st.columns(3)
def render_radar(name, data, col, strike):
    if data:
        with col:
            if data['rsi'] > 80:
                st.markdown(f"<div class='radar-box radar-danger'><div>{name}</div><div>DANGER 🚨</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='radar-box'><div><b>{strike}</b></div><div style='color:#1565c0; font-weight:900;'>BUY ABOVE: {data['p']} 👁️🙏</div></div>", unsafe_allow_html=True)

render_radar("NIFTY", results.get("NIFTY"), r_cols[0], "NIFTY 25800 CE")
render_radar("SENSEX", results.get("SENSEX"), r_cols[1], "SENSEX 83700 CE")
render_radar("CRUDE", results.get("CRUDE OIL"), r_cols[2], "CRUDE 50 CE")

# --- 3. COMPACT NIFTY 100 SCANNER ---
st.markdown("### 🔥 NIFTY 100 LIVE SCANNER")
for sym in ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]:
    res = get_pro_data(sym)
    if res:
        star = "⭐" if sym in ["RELIANCE.NS", "HDFCBANK.NS"] else ""
        st.markdown(f"""
        <div class='scanner-card' style='border-left: 10px solid {"#2e7d32" if res['status']=="BULLISH" else "#c62828"};'>
            <div class='stock-info'>
                <p class='stock-title'>{star} {sym.split('.')[0]}</p>
                <p class='price-main'>₹{res['p']}</p>
                <p style='color:{"#2e7d32" if res['status']=="BULLISH" else "#c62828"}; font-weight:bold; font-size:13px;'>{res['status']} MODE</p>
            </div>
            <div style='text-align:right;'>
                <p style='color:#2e7d32; font-weight:900; font-size:18px; margin:0;'>TGT: {round(res['p']*1.007, 2)}</p>
                <p style='color:#c62828; font-weight:900; font-size:18px; margin:0;'>SL: {res['ema']}</p>
                <p style='font-size:12px; color:#9e9e9e;'>RSI: {res['rsi']} | EMA: {res['ema']}</p>
            </div>
        </div>""", unsafe_allow_html=True)

# --- 4. BTST VIP ZONE ---
st.markdown("<div class='btst-vip'><h2>💰 BTST / SWING VIP ALERTS</h2>", unsafe_allow_html=True)
BTST_STOCKS = ["TCS.NS", "INFY.NS", "ICICIBANK.NS"]
for sym in BTST_STOCKS:
    res = get_pro_data(sym)
    if res and res['status'] == "BULLISH":
        st.markdown(f"""
        <div class='btst-item'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div><b style='font-size:20px; color:#1a237e;'>🚀 {sym.split('.')[0]}</b><br><span style='color:#757575;'>High Momentum BTST Pick</span></div>
                <div style='text-align:right;'><span style='font-size:24px; font-weight:900;'>₹{res['p']}</span><br><span style='color:#2e7d32; font-weight:bold;'>MODE: STRONG</span></div>
            </div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
