import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX BOLD", layout="wide")

# --- ULTRA BOLD & COMPACT CSS ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 45px !important; font-weight: 900 !important; }
    
    .compact-card {
        background: white;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 5px; /* Paas-paas lane ke liye kam margin */
        border-left: 8px solid #1a237e;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .stock-name { font-size: 30px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 35px !important; font-weight: 900; color: #000; margin: 0; }
    
    .signal-label {
        padding: 5px 15px;
        border-radius: 4px;
        font-size: 18px;
        font-weight: 900;
        color: white;
        text-align: center;
    }
    .bg-buy { background-color: #2e7d32; box-shadow: 0 0 10px #2e7d32; }
    .bg-sell { background-color: #c62828; box-shadow: 0 0 10px #c62828; }
    
    .level-text { font-size: 20px; font-weight: bold; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

def get_bold_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        diff = cp * 0.007
        status = "BUY" if cp > ema else "SELL"
        bg = "bg-buy" if cp > ema else "bg-sell"
        color = "#2e7d32" if cp > ema else "#c62828"
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "bg": bg, "c": color}
    except: return None

st.markdown("<h1 style='text-align:center; font-size:40px;'>🚀 TRADEX BOLD</h1>", unsafe_allow_html=True)

# --- INDEX SECTION (Compact) ---
st.markdown("### 🎯 INDEX")
c1, c2 = st.columns(2)
indices = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK"}
for i, (name, sym) in enumerate(indices.items()):
    res = get_bold_data(sym)
    if res:
        with (c1 if i==0 else c2):
            st.markdown(f"""<div class='compact-card' style='border-left-color:{res['c']};'>
                <h2 style='margin:0;'>{name}</h2>
                <p class='price-bold'>{res['p']}</p>
                <p class='level-text'>{res['s']} ABOVE {res['sl']}</p>
            </div>""", unsafe_allow_html=True)

# --- STOCKS SECTION (Bada Text, Kam Jagah) ---
st.markdown("### 🔥 STOCKS")
STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS", "BHARATFORG.NS"]

for s_sym in STOCKS:
    res = get_bold_data(s_sym)
    if res:
        st.markdown(f"""
        <div class='compact-card' style='border-left-color:{res['c']};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:2;'>
                    <p class='stock-name'>{s_sym.split('.')[0]}</p>
                    <p class='price-bold'>₹{res['p']}</p>
                </div>
                <div style='flex:1;'>
                    <div class='signal-label {res['bg']}'>{res['s']}</div>
                </div>
                <div style='flex:2; text-align:right;'>
                    <p class='level-text' style='color:#2e7d32;'>TGT: {res['t']}</p>
                    <p class='level-text' style='color:#c62828;'>SL: {res['sl']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- BTST (Kone mein aur Bada) ---
st.markdown("### 🌙 BTST")
btst_res = get_bold_data("JINDALSTEL.NS")
if btst_res:
    st.markdown(f"""
    <div class='compact-card' style='background:#f3e5f5; border-left:15px solid #4a148c;'>
        <h1 style='color:#4a148c; margin:0;'>✨ JINDAL STEL: {btst_res['s']}</h1>
        <p class='price-bold'>Entry: {btst_res['p']}</p>
    </div>
    """, unsafe_allow_html=True)
