import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX PRO BOX", layout="wide")

# Custom CSS for Box Styling
st.markdown("""
    <style>
    .trading-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        border-left: 10px solid #1E88E5;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .bullish-border { border-left-color: #2e7d32; background-color: #f1f8e9; }
    .bearish-border { border-left-color: #c62828; background-color: #ffebee; }
    .btst-card { border-left: 10px solid #6A1B9A; background-color: #F3E5F5; }
    </style>
    """, unsafe_allow_html=True)

def get_pro_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 5: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        diff = cp * 0.005 
        status = "BULLISH" if cp > ema else "BEARISH"
        color = "#2e7d32" if cp > ema else "#c62828"
        bg_class = "bullish-border" if cp > ema else "bearish-border"
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "c": color, "class": bg_class}
    except: return None

st.markdown("<h1 style='text-align: center;'>🚀 TRADEX PRO BOX DASHBOARD</h1>", unsafe_allow_html=True)

# --- SECTION 1: INDEX WATCH ---
st.header("🎯 INDEX WATCH")
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
idx_cols = st.columns(2)
for i, (name, sym) in enumerate(indices.items()):
    res = get_pro_data(sym)
    if res:
        with idx_cols[i]:
            st.markdown(f"""<div class="trading-card {res['class']}"><h2 style='margin:0;'>{name}</h2><h1 style='color:{res['c']}; margin:5px 0;'>{res['p']}</h1><p style='font-weight:bold;'>TREND: {res['s']} ABOVE {res['sl']}</p></div>""", unsafe_allow_html=True)

# --- SECTION 2: STOCK BOXES ---
st.header("🔥 MARKET MOVERS")
STOCKS = {"ADANI ENT": "ADANIENT.NS", "RELIANCE": "RELIANCE.NS", "HDFC BANK": "HDFCBANK.NS", "ICICI BANK": "ICICIBANK.NS", "SBIN": "SBIN.NS"}
stock_cols = st.columns(2)
for i, (name, sym) in enumerate(STOCKS.items()):
    res = get_pro_data(sym)
    if res:
        with stock_cols[i % 2]:
            st.markdown(f"""<div class="trading-card {res['class']}"><div style='display:flex; justify-content:space-between;'><h3>{name}</h3><span style='background:{res['c']}; color:white; padding:5px 10px; border-radius:5px;'>{res['s']}</span></div><hr><p><b>LTP:</b> {res['p']}</p><p style='color:#2e7d32;'><b>TARGET: 🎯 {res['t']}</b></p><p style='color:#c62828;'><b>STOPLOSS: 🛑 {res['sl']}</b></p></div>""", unsafe_allow_html=True)

# --- NEW SECTION 3: BTST / STBT SPECIAL ---
st.header("🌙 BTST / STBT SPECIAL (Overnight Picks)")
BTST_STOCKS = {"TATA MOTORS": "TATAMOTORS.NS", "JINDAL STEEL": "JINDALSTEL.NS"}
btst_cols = st.columns(2)
for i, (name, sym) in enumerate(BTST_STOCKS.items()):
    res = get_pro_data(sym)
    if res:
        type_label = "BTST (Buy)" if res['s'] == "BULLISH" else "STBT (Sell)"
        with btst_cols[i]:
            st.markdown(f"""
                <div class="trading-card btst-card">
                    <h3 style='color:#4A148C;'>✨ {name} - {type_label}</h3>
                    <p><b>Recommended Entry:</b> {res['p']}</p>
                    <p style='color:#4A148C;'><b>Next Day View: {'GAP UP expected' if res['s'] == "BULLISH" else 'GAP DOWN expected'}</b></p>
                </div>
            """, unsafe_allow_html=True)
