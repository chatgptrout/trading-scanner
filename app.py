import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MEGA PRO V3", layout="wide")

# --- CUSTOM CSS (Compact & Professional) ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .live-clock { font-size: 38px; font-weight: 900; color: #ff5252; text-align: right; }
    
    /* Radar Styling */
    .radar-box { background: #f8f9fa; border: 2px solid #1a237e; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .radar-danger { background: #ffebee; border-color: #ff5252; color: #c62828; font-weight: bold; }
    .radar-buy { background: #e3f2fd; border-color: #1565c0; border-left: 10px solid #1565c0; }

    /* Compact Scanner Cards */
    .compact-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border: 1px solid #eee; border-left: 12px solid #1a237e; display: flex; justify-content: space-between; align-items: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.03); }
    .neon-red { border-left-color: #ff5252 !important; }
    .neon-green { border-left-color: #4caf50 !important; }

    /* Tags & Text */
    .zone-badge { padding: 4px 12px; border-radius: 50px; font-size: 11px; font-weight: 900; text-transform: uppercase; margin-top: 5px; display: inline-block; }
    .tag-demand { background: #fff9c4; color: #f57f17; border: 1px solid #f57f17; }
    .tag-supply { background: #ffebee; color: #c62828; border: 1px solid #c62828; }
    
    .stock-info { line-height: 1.1; }
    .stock-title { font-size: 22px; font-weight: 900; color: #1a237e; margin: 0; }
    .price-main { font-size: 26px; font-weight: 900; color: #212121; margin: 0; }
    .metrics-group { text-align: right; line-height: 1.3; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_market_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        is_bullish = cp > ema
        style = "compact-card neon-red" if rsi > 80 else ("compact-card neon-green" if is_bullish else "compact-card")
        tag = "tag-demand" if is_bullish else "tag-supply"
        msg = "📍 Daily Demand Zone" if is_bullish else "🚫 Near Supply Zone"
        
        return {"p": cp, "ema": ema, "rsi": rsi, "style": style, "msg": msg, "tag": tag, "t": round(cp*1.01, 2)}
    except: return None

# --- UI RENDER ---
c_h1, c_h2 = st.columns([2, 1])
with c_h1: st.markdown("<h1>🚀 TRADEX MEGA PRO V3</h1>", unsafe_allow_html=True)
with c_h2: st.markdown(f"<div class='live-clock'>⏰ {get_ist_time()}</div>", unsafe_allow_html=True)

# --- INDEX STATUS ---
m_cols = st.columns(4)
assets = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "GOLD": "GC=F"}
results = {}

for i, (name, sym) in enumerate(assets.items()):
    res = get_market_data(sym)
    results[name] = res
    if res:
        with m_cols[i]:
            st.markdown(f"""<div class='{res['style']}'><div class='stock-info'><p style='color:#757575; font-size:14px; margin:0;'>{name}</p><p class='price-main'>{res['p']}</p><div class='zone-badge {res['tag']}'>{res['msg']}</div></div></div>""", unsafe_allow_html=True)

# --- RADAR ---
st.markdown("### 🔥 STRIKE PRICE RADAR")
r_cols = st.columns(3)
def render_radar(name, data, col, strike):
    if data:
        with col:
            if data['rsi'] > 80:
                st.markdown(f"<div class='radar-box radar-danger'>{name}: DANGER (RSI {data['rsi']})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='radar-box radar-buy'><div><b>{strike}</b></div><div style='font-weight:900;'>BUY ABOVE: {data['p']} 👁️🙏</div></div>", unsafe_allow_html=True)

render_radar("NIFTY", results.get("NIFTY 50"), r_cols[0], "NIFTY 25800 CE")
render_radar("SENSEX", results.get("SENSEX"), r_cols[1], "SENSEX 83700 CE")
render_radar("CRUDE", results.get("CRUDE OIL"), r_cols[2], "CRUDE 50 CE")

# --- COMPACT SCANNER ---
st.markdown("### 🔥 NIFTY 100 INSTITUTIONAL SCANNER")
STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]

for sym in STOCKS:
    res = get_market_data(sym)
    if res:
        star = "⭐" if sym in ["RELIANCE.NS", "HDFCBANK.NS"] else ""
        st.markdown(f"""
        <div class='{res['style']}'>
            <div class='stock-info'>
                <p class='stock-title'>{star} {sym.split('.')[0]}</p>
                <p class='price-main'>₹{res['p']}</p>
                <div class='zone-badge {res['tag']}'>{res['msg']}</div>
            </div>
            <div class='metrics-group'>
                <p style='color:#2e7d32; font-weight:900; font-size:18px; margin:0;'>TGT: {res['t']}</p>
                <p style='color:#c62828; font-weight:900; font-size:18px; margin:0;'>SL: {res['ema']}</p>
                <p style='font-size:12px; color:#757575; margin-top:4px;'>RSI: {res['rsi']} | EMA: {res['ema']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

time.sleep(30)
st.rerun()
