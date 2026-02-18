import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MEGA PRO V3", layout="wide")

# --- CUSTOM CSS (Compact & Grouped Design) ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .live-clock { font-size: 38px; font-weight: 900; color: #ff5252; text-align: right; }
    
    /* Compact Radar */
    .radar-box { background: #f8f9fa; border: 2px solid #1a237e; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .radar-danger { background: #ffebee; border-color: #ff5252; color: #c62828; font-weight: bold; }
    .radar-buy { background: #e3f2fd; border-color: #1565c0; border-left: 10px solid #1565c0; }

    /* Compact Mega Cards */
    .compact-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border: 1px solid #eee; border-left: 10px solid #1a237e; box-shadow: 2px 2px 10px rgba(0,0,0,0.03); display: flex; justify-content: space-between; align-items: center; }
    .neon-red { border-left-color: #ff5252 !important; box-shadow: 0 0 15px rgba(255,82,82,0.1) !important; }
    .neon-green { border-left-color: #4caf50 !important; box-shadow: 0 0 15px rgba(76,175,80,0.1) !important; }

    /* Zone Badges */
    .zone-badge { padding: 4px 12px; border-radius: 50px; font-size: 12px; font-weight: 900; text-transform: uppercase; margin-top: 5px; display: inline-block; }
    .tag-demand { background: #fff9c4; color: #f57f17; border: 1px solid #f57f17; }
    .tag-supply { background: #ffebee; color: #c62828; border: 1px solid #c62828; }

    .price-group { line-height: 1.1; }
    .stock-title { font-size: 22px; font-weight: 900; color: #1a237e; margin: 0; }
    .price-main { font-size: 26px; font-weight: 900; color: #212121; margin: 0; }
    .tgt-sl-group { text-align: right; line-height: 1.2; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_compact_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        style = "compact-card neon-red" if rsi > 80 else ("compact-card neon-green" if cp > ema else "compact-card")
        tag = "tag-demand" if cp <= ema * 1.005 else "tag-supply"
        msg = "📍 Daily Demand Zone" if cp <= ema * 1.005 else "🚫 Near Supply Zone"
        
        return {"p": cp, "ema": ema, "rsi": rsi, "style": style, "msg": msg, "tag": tag}
    except: return None

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1: st.markdown("<h1>🚀 TRADEX MEGA PRO V3</h1>", unsafe_allow_html=True)
with col_h2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- 1. INDEX STATUS ---
m_cols = st.columns(4)
assets = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_compact_data(sym)
    results[name] = res
    if res:
        with m_cols[i]:
            st.markdown(f"""
            <div class='{res['style']}'>
                <div class='price-group'>
                    <p style='color:#757575; font-weight:bold; margin:0; font-size:14px;'>{name}</p>
                    <p class='price-main'>{res['p']}</p>
                    <div class='zone-badge {res['tag']}'>{res['msg']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 2. STRIKE PRICE RADAR ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
r_cols = st.columns(3)
def display_radar(name, res, col, strike):
    if res:
        with col:
            if res['rsi'] > 80:
                st.markdown(f"<div class='radar-box radar-danger'>{name}: DANGER (RSI {res['rsi']})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='radar-box radar-buy'><div><b>{strike}</b></div><div style='font-weight:900;'>BUY ABOVE: {res['p']} 👁️🙏</div></div>", unsafe_allow_html=True)

display_radar("NIFTY", results.get("NIFTY 50"), r_cols[0], "NIFTY 25800 CE")
display_radar("SENSEX", results.get("SENSEX"), r_cols[1], "SENSEX 83700 CE")
display_radar("CRUDE", results.get("CRUDE OIL"), r_cols[2], "CRUDE 50 CE")

# --- 3. COMPACT SCANNER ---
st.markdown("### 🔥 NIFTY 100 INSTITUTIONAL SCANNER")
STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]

for sym in STOCKS:
    res = get_compact_data(sym)
    if res:
        star = "⭐" if sym in ["RELIANCE.NS", "HDFCBANK.NS"] else ""
        st.markdown(f"""
        <div class='{res['style']}'>
            <div class='price-group'>
                <p class='stock-title'>{star} {sym.split('.')[0]}</p>
                <p class='price-main'>₹{res['p']}</p>
                <div class='zone-badge {res['tag']}'>{res['msg']}</div>
            </div>
            <div class='tgt-sl-group'>
                <p style='color:#2e7d32; font-weight:900; margin:0;'>TGT: {round(res['p']*1.01, 2)}</p>
                <p style='color:#c62828; font-weight:900; margin:0;'>SL: {res['ema']}</p>
                <p style='font-size:12px; color:#757575; margin-top:5px;'>RSI: {res['rsi']} | EMA: {res['ema']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

time.sleep(30)
st.rerun()
