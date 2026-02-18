import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MEGA PRO V3", layout="wide")

# --- CUSTOM CSS (The Mega Glow Design) ---
st.markdown("""
    <style>
    .live-clock { font-size: 38px; font-weight: 900; color: #ff5252; text-align: right; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    
    /* Institutional Glow Buttons */
    .filter-btn { background: #004d40; color: #ffca28; border: 2px solid #ffca28; padding: 12px 25px; border-radius: 50px; font-weight: 900; box-shadow: 0 4px 15px rgba(255,202,40,0.3); }

    /* Mega Cards with Neon Borders */
    .mega-card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 15px; border: 1px solid #e0e0e0; border-left: 12px solid #1a237e; box-shadow: 5px 5px 20px rgba(0,0,0,0.05); }
    .neon-red { border-left-color: #ff5252 !important; box-shadow: 0 0 20px rgba(255,82,82,0.2) !important; }
    .neon-green { border-left-color: #4caf50 !important; box-shadow: 0 0 20px rgba(76,175,80,0.2) !important; }

    /* GTF Zone Badges */
    .zone-tag { padding: 6px 15px; border-radius: 50px; font-size: 14px; font-weight: 900; display: inline-block; margin-top: 10px; text-transform: uppercase; }
    .tag-demand { background: #fff9c4; color: #f57f17; border: 1px solid #f57f17; }
    .tag-supply { background: #ffebee; color: #c62828; border: 1px solid #c62828; }
    .tag-reacting { background: #e8f5e9; color: #2e7d32; border: 1px solid #2e7d32; }

    .price-main { font-size: 32px; font-weight: 900; color: #212121; margin: 0; }
    .stock-title { font-size: 26px; font-weight: 900; color: #1a237e; }
    .tgt-sl { font-size: 18px; font-weight: 900; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_mega_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        # Zone Logic (Institutional GTF style)
        demand_zone = round(ema * 0.99, 2)
        supply_zone = round(ema * 1.01, 2)
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        # Style logic
        style_class = "mega-card"
        if rsi > 80: style_class += " neon-red"
        elif cp > ema: style_class += " neon-green"
        
        zone_type = "demand" if cp <= demand_zone * 1.005 else ("supply" if cp >= supply_zone * 0.995 else "demand")
        zone_msg = "📍 Daily Demand Zone" if zone_type=="demand" else "🚫 Near Supply Zone"
        
        return {"p": cp, "ema": ema, "rsi": rsi, "style": style_class, "msg": zone_msg, "tag": f"tag-{zone_type}", "dz": demand_zone}
    except: return None

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1: st.markdown("<h1>🚀 TRADEX MEGA PRO V3</h1>", unsafe_allow_html=True)
with col_h2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- FILTERS ---
st.markdown("<div class='filter-btn'>🔍 GTF DAILY ZONE SCANNER ACTIVE</div>", unsafe_allow_html=True)
st.markdown("---")

# --- 1. INDEX & COMMODITY (The Mega Look) ---
m_cols = st.columns(4)
assets = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}

for i, (name, sym) in enumerate(assets.items()):
    res = get_mega_data(sym)
    if res:
        with m_cols[i]:
            st.markdown(f"""
            <div class='{res['style']}'>
                <p style='color:#757575; font-weight:bold; margin:0;'>{name}</p>
                <p class='price-main'>{res['p']}</p>
                <div class='zone-tag {res['tag']}'>{res['msg']}</div>
                <p style='margin-top:10px; font-weight:bold; color:#616161;'>RSI: {res['rsi']} | EMA: {res['ema']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- 2. NIFTY 100 ZONE SCANNER ---
st.markdown("### 🔥 NIFTY 100 INSTITUTIONAL SCANNER")
STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS"]

for sym in STOCKS:
    res = get_mega_data(sym)
    if res:
        star = "⭐" if sym in ["RELIANCE.NS", "HDFCBANK.NS"] else ""
        st.markdown(f"""
        <div class='{res['style']}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <p class='stock-title'>{star} {sym.split('.')[0]}</p>
                    <p class='price-main'>₹{res['p']}</p>
                    <div class='zone-tag {res['tag']}'>{res['msg']}</div>
                </div>
                <div style='text-align:right;'>
                    <p class='tgt-sl' style='color:#2e7d32;'>TGT: {round(res['p']*1.01, 2)}</p>
                    <p class='tgt-sl' style='color:#c62828;'>SL: {res['ema']}</p>
                    <p style='margin-top:5px; font-weight:bold;'>Demand: {res['dz']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

time.sleep(30)
st.rerun()
