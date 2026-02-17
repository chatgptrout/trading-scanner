import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX ULTRA", layout="wide")

# --- ULTRA ATTRACTIVE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main { background-color: #0e1117; }
    
    .stHeader { font-family: 'Orbitron', sans-serif; color: #00d4ff; text-align: center; text-shadow: 0 0 10px #00d4ff; }
    
    /* Box Styling */
    .trade-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        transition: transform 0.3s;
    }
    .trade-card:hover { transform: scale(1.02); border: 1px solid #00d4ff; }

    /* Neon Signal Badges */
    .badge {
        padding: 8px 15px;
        border-radius: 8px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 14px;
        box-shadow: 0 0 15px;
    }
    .buy-badge { background-color: #00ff88; color: #000; box-shadow: 0 0 20px #00ff88; }
    .sell-badge { background-color: #ff3131; color: #fff; box-shadow: 0 0 20px #ff3131; }
    
    /* BTST Special Card */
    .btst-special {
        background: linear-gradient(135deg, #6a1b9a 0%, #4a148c 100%);
        color: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(106, 27, 154, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

def get_ultra_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        diff = cp * 0.008
        status = "BULLISH" if cp > ema else "BEARISH"
        color = "#00ff88" if cp > ema else "#ff3131"
        b_class = "buy-badge" if cp > ema else "sell-badge"
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "c": color, "bg": b_class}
    except: return None

st.markdown("<h1 class='stHeader'>⚡ TRADEX ULTRA PRO</h1>", unsafe_allow_html=True)

# --- INDEX SECTION ---
st.write("### 💎 MARKET OVERVIEW")
col1, col2 = st.columns(2)
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
for i, (name, sym) in enumerate(indices.items()):
    res = get_ultra_data(sym)
    if res:
        with (col1 if i==0 else col2):
            st.markdown(f"""<div class='trade-card'>
                <p style='color:grey; margin:0;'>{name}</p>
                <h1 style='color:{res['c']}; margin:0;'>{res['p']}</h1>
                <p style='margin:0;'>Trend: <b>{res['s']}</b> | Support: {res['sl']}</p>
            </div>""", unsafe_allow_html=True)

# --- STOCKS TABLE SECTION ---
st.write("### 🔥 LIVE BREAKOUT RADAR")
MOVERS = {"ADANI ENT": "ADANIENT.NS", "RELIANCE": "RELIANCE.NS", "HDFC BANK": "HDFCBANK.NS", "SBIN": "SBIN.NS"}

# Header line
st.markdown("<div style='display:flex; justify-content:space-between; padding:10px; color:grey; font-weight:bold;'><span>STOCK</span><span>SIGNAL</span><span>TARGET</span></div>", unsafe_allow_html=True)

for name, sym in MOVERS.items():
    res = get_ultra_data(sym)
    if res:
        st.markdown(f"""
        <div class='trade-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <h3 style='margin:0;'>{name}</h3>
                    <p style='margin:0; font-size:18px;'>₹{res['p']}</p>
                </div>
                <div class='badge {res['bg']}'>SIGNAL</div>
                <div style='text-align:right;'>
                    <p style='color:#00ff88; margin:0;'>TGT: {res['t']}</p>
                    <p style='color:#ff3131; margin:0;'>SL: {res['sl']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- BTST SECTION ---
st.write("### 🌙 OVERNIGHT LEGENDS (BTST)")
res_btst = get_ultra_data("JINDALSTEL.NS")
if res_btst:
    st.markdown(f"""
    <div class='btst-special'>
        <h2 style='margin:0;'>✨ JINDAL STEEL - {res_btst['s']}</h2>
        <p style='font-size:20px;'>Entry Zone: {res_btst['p']} | <b>View: {'🚀 GAP UP' if res_btst['s']=="BULLISH" else '🔻 GAP DOWN'}</b></p>
    </div>
    """, unsafe_allow_html=True)
