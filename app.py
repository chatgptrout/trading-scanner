import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MEGA PRO V3", layout="wide")

# --- CUSTOM CSS (Radar Restoration + Mega Glow) ---
st.markdown("""
    <style>
    .live-clock { font-size: 38px; font-weight: 900; color: #ff5252; text-align: right; }
    
    /* Strike Price Radar Design */
    .radar-container { display: flex; gap: 10px; margin-bottom: 20px; }
    .radar-box { flex: 1; background: #f8f9fa; border: 2px solid #1a237e; border-radius: 10px; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
    .radar-danger { background: #ffebee; border-color: #ff5252; color: #c62828; font-weight: 900; text-align: center; }
    .radar-buy { background: #e3f2fd; border-color: #1565c0; }
    
    /* Mega Cards */
    .mega-card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 15px; border-left: 12px solid #1a237e; box-shadow: 5px 5px 20px rgba(0,0,0,0.05); }
    .neon-red { border-left-color: #ff5252 !important; box-shadow: 0 0 20px rgba(255,82,82,0.2) !important; }
    .neon-green { border-left-color: #4caf50 !important; box-shadow: 0 0 20px rgba(76,175,80,0.2) !important; }

    /* Zone Badges */
    .zone-tag { padding: 6px 15px; border-radius: 50px; font-size: 14px; font-weight: 900; display: inline-block; margin-top: 10px; }
    .tag-demand { background: #fff9c4; color: #f57f17; border: 1px solid #f57f17; }
    .tag-supply { background: #ffebee; color: #c62828; border: 1px solid #c62828; }
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
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        # Zone
        is_demand = cp <= ema * 1.005
        msg = "📍 Daily Demand Zone" if is_demand else "🚫 Near Supply Zone"
        tag = "tag-demand" if is_demand else "tag-supply"
        style = "mega-card neon-red" if rsi > 80 else ("mega-card neon-green" if cp > ema else "mega-card")
        
        return {"p": cp, "ema": ema, "rsi": rsi, "style": style, "msg": msg, "tag": tag, "dz": round(ema * 0.99, 2)}
    except: return None

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1: st.markdown("<h1>🚀 TRADEX MEGA PRO V3</h1>", unsafe_allow_html=True)
with col_h2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- 1. INDEX & COMMODITY STATUS ---
m_cols = st.columns(4)
assets = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_mega_data(sym)
    results[name] = res
    if res:
        with m_cols[i]:
            st.markdown(f"<div class='{res['style']}'><b>{name}</b><p style='font-size:32px; font-weight:900; margin:0;'>{res['p']}</p><div class='zone-tag {res['tag']}'>{res['msg']}</div></div>", unsafe_allow_html=True)

# --- 2. RESTORED STRIKE PRICE RADAR ---
st.markdown("### 🔥 STRIKE PRICE RADAR (AUTO-SIGNALS)")
r_cols = st.columns(3)
def display_radar(name, res, col, strike_name):
    if res:
        with col:
            if res['rsi'] > 80:
                st.markdown(f"<div class='radar-box radar-danger'>{name}: DANGER (RSI {res['rsi']})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class='radar-box radar-buy'><div><b>{strike_name}</b></div><div style='color:#1565c0; font-weight:900;'>BUY ABOVE: {res['p']} 👁️🙏</div></div>""", unsafe_allow_html=True)

display_radar("NIFTY", results.get("NIFTY 50"), r_cols[0], "NIFTY 25800 CE")
display_radar("SENSEX", results.get("SENSEX"), r_cols[1], "SENSEX 83700 CE")
display_radar("CRUDE", results.get("CRUDE OIL"), r_cols[2], "CRUDE 50 CE")

# --- 3. NIFTY 100 INSTITUTIONAL SCANNER ---
st.markdown("### 🔥 NIFTY 100 INSTITUTIONAL SCANNER")
STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]
for sym in STOCKS:
    res = get_mega_data(sym)
    if res:
        st.markdown(f"""
        <div class='{res['style']}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div><b>⭐ {sym.split('.')[0]}</b><p style='font-size:28px; font-weight:900; margin:0;'>₹{res['p']}</p></div>
                <div style='text-align:right;'><p style='color:#2e7d32; font-weight:900; margin:0;'>TGT: {round(res['p']*1.01, 2)}</p><p style='color:#c62828; font-weight:900; margin:0;'>SL: {res['ema']}</p></div>
            </div>
        </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
