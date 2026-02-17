import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX PRO ALL-IN-ONE", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🚀 TRADEX PRO LIVE DASHBOARD</h1>", unsafe_allow_html=True)

def get_live_pro_signal(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 5: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        diff = cp * 0.005 
        status = "BULLISH" if cp > ema else "BEARISH"
        color = "green" if cp > ema else "red"
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "c": color}
    except: return None

# --- SECTION 1: INDEX LEVELS (Nifty/Bank Nifty) ---
st.header("🎯 INDEX LEVELS")
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
idx_cols = st.columns(len(indices))
for i, (name, sym) in enumerate(indices.items()):
    res = get_live_pro_signal(sym)
    if res:
        with idx_cols[i]:
            st.subheader(name)
            st.metric("LTP", res['p'])
            st.markdown(f"**Trend:** :{res['c']}[{res['s']} ABOVE {res['sl']}]")
st.divider()

# --- SECTION 2: STOCKS ---
st.header("📈 STOCK LEVELS")
STOCKS = {"RELIANCE": "RELIANCE.NS", "BHARAT FORGE": "BHARATFORG.NS", "TCS": "TCS.NS", "SBIN": "SBIN.NS", "HDFC BANK": "HDFCBANK.NS"}
h = st.columns([2, 1, 2, 2, 2])
h[0].write("**NAME**"); h[1].write("**SIGNAL**"); h[2].write("**ENTRY**"); h[3].write("**TARGET**"); h[4].write("**STOPLOSS**")

for name, sym in STOCKS.items():
    res = get_live_pro_signal(sym)
    if res:
        c = st.columns([2, 1, 2, 2, 2])
        c[0].write(f"**{name}**")
        c[1].markdown(f"<div style='background-color:{res['c']}; color:white; padding:2px; border-radius:5px; text-align:center; font-size:12px;'>SIGNAL</div>", unsafe_allow_html=True)
        c[2].write(res['p']); c[3].write(res['t']); c[4].write(res['sl'])
st.divider()

# --- SECTION 3: COMMODITY ---
st.header("🛢️ COMMODITY LEVELS")
COMM = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
for name, sym in COMM.items():
    res = get_live_pro_signal(sym)
    if res:
        c = st.columns([2, 1, 2, 2, 2])
        c[0].write(f"**{name}**")
        c[1].markdown(f"<div style='background-color:{res['c']}; color:white; padding:2px; border-radius:5px; text-align:center; font-size:12px;'>SIGNAL</div>", unsafe_allow_html=True)
        c[2].write(res['p']); c[3].write(res['t']); c[4].write(res['sl'])
