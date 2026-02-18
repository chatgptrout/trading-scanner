import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX PRO V2", layout="wide")

# --- CUSTOM CSS (Purana Data + Naya Professional Look) ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0e14; color: #e0e0e0; }
    .live-clock { font-size: 35px; font-weight: 900; color: #ff5252; text-align: right; font-family: 'Courier New', monospace; }
    
    /* GTF Zone Badges */
    .zone-badge { padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 900; color: #000; margin-top: 5px; display: inline-block; }
    .demand-badge { background-color: #ffd700; } 
    .supply-badge { background-color: #ff5252; color: #fff; } 
    .safe-badge { background-color: #4caf50; color: #fff; } 

    /* Card Styling (Scanner and Status) */
    .pro-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 10px; border-left: 8px solid #1f6feb; }
    .stock-name { font-size: 24px; font-weight: 900; color: #ffffff; margin: 0; }
    .price-bold { font-size: 28px; font-weight: 900; color: #ffffff; margin: 0; }
    .tgt-text { color: #4caf50 !important; font-weight: 900; font-size: 16px; margin: 0; }
    .sl-text { color: #ff5252 !important; font-weight: 900; font-size: 16px; margin: 0; }
    
    /* Filter Buttons */
    .filter-btn { background: #21262d; border: 1px solid #30363d; padding: 10px 20px; border-radius: 8px; color: #c9d1d9; font-weight: bold; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        df['RSI'] = calculate_rsi(df['Close'])
        rsi_val = round(df['RSI'].iloc[-1], 2)
        
        # Zone Logic
        demand_zone = round(ema * 0.99, 2)
        supply_zone = round(ema * 1.01, 2)
        
        status = "BULLISH" if cp > ema else "BEARISH"
        zone_msg = "📍 DEMAND ZONE" if cp <= demand_zone * 1.005 else ("🚫 SUPPLY ZONE" if cp >= supply_zone * 0.995 else "APPROACHING ZONE")
        badge_class = "demand-badge" if "APPROACHING" in zone_msg else ("safe-badge" if "DEMAND" in zone_msg else "supply-badge")
        
        diff = cp * 0.007
        is_safe = "✅ SAFE ENTRY" if abs(cp - ema) / ema < 0.003 else "⚠️ PRICE TOO HIGH"
        
        return {"p": cp, "ema": ema, "rsi": rsi_val, "status": status, "msg": zone_msg, "b_class": badge_class, 
                "d_z": demand_zone, "t": round(cp + (diff if cp > ema else -diff), 2), "zone_info": is_safe}
    except: return None

QUALITY_LIST = ["ITC.NS", "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "SBIN.NS"]

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1: st.title("🚀 TRADEX PRO V2")
with c2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- 1. FILTERS & STATUS ---
st.markdown("### 🔍 INSTITUTIONAL FILTERS")
f_cols = st.columns(6)
with f_cols[0]: st.markdown("<div class='filter-btn' style='background:#ffd700; color:black;'>DAILY</div>", unsafe_allow_html=True)
with f_cols[1]: st.markdown("<div class='filter-btn'>WEEKLY</div>", unsafe_allow_html=True)

st.markdown("---")
assets = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}
m_cols = st.columns(4)

for i, (name, sym) in enumerate(assets.items()):
    res = get_pro_data(sym)
    if res:
        card_col = "#238636" if res['status'] == "BULLISH" else "#da3633"
        if res['rsi'] > 80: card_col = "#ff5252" # Critical RSI Glow
        with m_cols[i]:
            st.markdown(f"""<div class='pro-card' style='border-left-color:{card_col};'>
                <div style='color:#8b949e; font-weight:bold;'>{name}</div>
                <div class='price-bold'>{res['p']}</div>
                <div class='zone-badge {res['b_class']}'>{res['msg']}</div>
                <div style='margin-top:10px; font-size:12px; color:#8b949e;'>RSI: {res['rsi']} | EMA: {res['ema']}</div>
            </div>""", unsafe_allow_html=True)

# --- 2. RESTORED NIFTY 100 SCANNER (TGT/SL/STARS) ---
st.markdown("### 🔥 NIFTY 100 ZONE SCANNER")
NIFTY_100 = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS", "TCS.NS", "BHARATFORG.NS"]

for sym in NIFTY_100:
    res = get_pro_data(sym)
    if res:
        star = "⭐" if sym in QUALITY_LIST else ""
        bg = "#238636" if res['status'] == "BULLISH" else "#da3633"
        st.markdown(f"""
        <div class='pro-card' style='border-left-color:{bg};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:2;'>
                    <div class='stock-name'>{star} {sym.split('.')[0]}</div>
                    <div class='price-bold'>₹{res['p']}</div>
                    <div style='color:{bg}; font-weight:bold; font-size:13px;'>{res['zone_info']}</div>
                </div>
                <div style='flex:1.5; text-align:center;'>
                    <div class='zone-badge {res['b_class']}' style='font-size:14px;'>{res['msg']}</div>
                    <div style='color:#8b949e; font-size:12px; margin-top:5px;'>Demand: {res['d_z']}</div>
                </div>
                <div style='flex:2; text-align:right;'>
                    <p class='tgt-text'>TGT: {res['t']}</p>
                    <p class='sl-text'>SL: {res['ema']}</p>
                    <p style='font-size:12px; color:#8b949e;'>RSI: {res['rsi']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

time.sleep(30)
st.rerun()
