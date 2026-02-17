import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX PRO ULTRA", layout="wide")

# --- PREMIUM CSS FOR HIGH-END DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stApp { background-color: #f8f9fa; }
    
    /* Premium Card Design */
    .card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    
    /* Signal Badge Design */
    .signal-badge {
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 14px;
        text-align: center;
        color: white;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .buy-color { background: linear-gradient(135deg, #00c853, #b9f6ca); color: #1b5e20; }
    .sell-color { background: linear-gradient(135deg, #ff1744, #ff8a80); color: #b71c1c; }
    
    /* Header Styling */
    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #1a237e;
        margin-bottom: 20px;
        border-left: 5px solid #1a237e;
        padding-left: 15px;
    }
    
    .price-text { font-size: 32px; font-weight: 900; color: #212121; }
    .btst-card { background: linear-gradient(135deg, #4527a0, #7e57c2); color: white; border-radius: 15px; padding: 25px; }
    </style>
    """, unsafe_allow_html=True)

def get_premium_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        status = "BULLISH" if cp > ema else "BEARISH"
        badge = "buy-color" if cp > ema else "sell-color"
        diff = cp * 0.007
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "badge": badge}
    except: return None

st.markdown("<h1 style='text-align:center; color:#1a237e; font-weight:900;'>🚀 TRADEX PREMIUM</h1>", unsafe_allow_html=True)

# --- INDEX SECTION ---
st.markdown("<div class='section-title'>🎯 MARKET STATUS</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
for i, (name, sym) in enumerate(indices.items()):
    res = get_premium_data(sym)
    if res:
        with (c1 if i==0 else c2):
            st.markdown(f"""<div class='card'>
                <p style='color:#757575; font-weight:bold; margin:0;'>{name}</p>
                <p class='price-text'>₹{res['p']}</p>
                <div class='signal-badge {res['badge']}'>{res['s']}</div>
            </div>""", unsafe_allow_html=True)

# --- STOCKS SECTION ---
st.markdown("<div class='section-title'>🔥 TOP PICKS</div>", unsafe_allow_html=True)
STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS"]
for s_sym in STOCKS:
    res = get_premium_data(s_sym)
    if res:
        st.markdown(f"""
        <div class='card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <h2 style='margin:0;'>{s_sym.split('.')[0]}</h2>
                    <p style='font-size:24px; font-weight:bold; margin:0;'>₹{res['p']}</p>
                </div>
                <div class='signal-badge {res['badge']}'>{res['s']}</div>
                <div style='text-align:right;'>
                    <p style='color:#2e7d32; font-weight:bold; margin:0;'>TGT: {res['t']}</p>
                    <p style='color:#c62828; font-weight:bold; margin:0;'>SL: {res['sl']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- BTST SECTION ---
st.markdown("<div class='section-title'>🌙 OVERNIGHT SPECIAL</div>", unsafe_allow_html=True)
btst_res = get_premium_data("JINDALSTEL.NS")
if btst_res:
    st.markdown(f"""
    <div class='btst-card'>
        <h2 style='margin:0;'>✨ JINDAL STEEL - {btst_res['s']}</h2>
        <h3 style='margin:0;'>Action: {'BUY AT CLOSE' if btst_res['s']=="BULLISH" else 'SELL AT CLOSE'}</h3>
        <p style='font-size:20px; margin-top:10px;'>Targeting Gap {'Up' if btst_res['s']=="BULLISH" else 'Down'} for Tomorrow</p>
    </div>
    """, unsafe_allow_html=True)
