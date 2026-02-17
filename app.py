import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX SUPER 100 PRO", layout="wide")

# --- CSS FOR FIXED TOP & BOLD DESIGN ---
st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 1000;
        background: #f8f9fa;
        padding: 10px;
        border-bottom: 2px solid #1a237e;
    }
    .compact-card {
        background: white;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 6px;
        border-left: 10px solid #1a237e;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stock-name { font-size: 28px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 32px !important; font-weight: 900; color: #000; margin: 0; }
    .signal-label {
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 16px;
        font-weight: 900;
        color: white;
        text-align: center;
    }
    .bg-buy { background-color: #2e7d32; }
    .bg-sell { background-color: #c62828; }
    .btst-card { background: #f3e5f5; border: 2px solid #4a148c; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

def get_market_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        status = "BUY" if cp > ema else "SELL"
        bg = "bg-buy" if cp > ema else "bg-sell"
        color = "#2e7d32" if cp > ema else "#c62828"
        diff = cp * 0.007
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "bg": bg, "c": color}
    except: return None

# --- TOP SECTION: NIFTY & BTST ---
st.title("🚀 TRADEX MEGA DASHBOARD")

# 1. NIFTY & BANKNIFTY (Fixed on top)
st.markdown("### 🎯 INDEX STATUS")
c1, c2 = st.columns(2)
for i, (name, sym) in enumerate({"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK"}.items()):
    res = get_market_data(sym)
    if res:
        with (c1 if i==0 else c2):
            st.markdown(f"""<div class='compact-card' style='border-left-color:{res['c']};'>
                <h2 style='margin:0;'>{name}</h2>
                <p class='price-bold'>{res['p']}</p>
                <p style='font-weight:bold; color:{res['c']};'>{res['s']} ABOVE {res['sl']}</p>
            </div>""", unsafe_allow_html=True)

# 2. BTST SPECIAL (Upar hi dikhega)
st.markdown("### 🌙 BTST / STBT PICK")
btst_res = get_market_data("JINDALSTEL.NS")
if btst_res:
    st.markdown(f"""
    <div class='btst-card'>
        <h2 style='color:#4a148c; margin:0;'>✨ JINDAL STEEL - {btst_res['s']}</h2>
        <p class='price-bold'>Entry: {btst_res['p']} | Target: {btst_res['t']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- BOTTOM SECTION: 100 STOCKS SCANNER ---
st.markdown("### 🔥 NIFTY 100 SCANNER")

NIFTY_100 = [
    "RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS", "BHARATFORG.NS", "TATAMOTORS.NS", "TCS.NS", "ICICIBANK.NS", "INFY.NS", "JSWSTEEL.NS",
    "AXISBANK.NS", "BAJFINANCE.NS", "LT.NS", "ITC.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS"
    # ... baki stocks niche automatic scan hote rahenge
]

for s_sym in NIFTY_100:
    res = get_market_data(s_sym)
    if res:
        st.markdown(f"""
        <div class='compact-card' style='border-left-color:{res['c']};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:2;'>
                    <p class='stock-name'>{s_sym.split('.')[0]}</p>
                    <p class='price-bold'>₹{res['p']}</p>
                </div>
                <div style='flex:1;'><div class='signal-label {res['bg']}'>{res['s']}</div></div>
                <div style='flex:2; text-align:right;'>
                    <p style='color:#2e7d32; font-weight:bold; margin:0;'>TGT: {res['t']}</p>
                    <p style='color:#c62828; font-weight:bold; margin:0;'>SL: {res['sl']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
