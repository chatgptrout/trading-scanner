import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX FINAL", layout="wide")

# Sidebar Menu
st.sidebar.title("🛠️ CATEGORY MENU")
app_mode = st.sidebar.radio("CHOOSE SCANNER", ["STOCKS", "COMMODITY", "INDEX LEVELS"])

def get_live_signal(ticker):
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

st.markdown(f"<h1 style='text-align: center;'>🚀 {app_mode} LIVE</h1>", unsafe_allow_html=True)

# --- CATEGORY: STOCKS ---
if app_mode == "STOCKS":
    STOCKS = {"RELIANCE": "RELIANCE.NS", "BHARAT FORGE": "BHARATFORG.NS", "TCS": "TCS.NS", "SBIN": "SBIN.NS"}
    for name, sym in STOCKS.items():
        res = get_live_signal(sym)
        if res:
            c = st.columns([2, 1, 2, 2, 2])
            c[0].subheader(name); c[1].markdown(f"<div style='background-color:{res['c']}; color:white; padding:5px; border-radius:5px; text-align:center;'>SIGNAL</div>", unsafe_allow_html=True)
            c[2].write(f"Price: {res['p']}"); c[3].write(f"Target: {res['t']}"); c[4].write(f"SL: {res['sl']}")
            st.divider()

# --- CATEGORY: INDEX LEVELS ---
elif app_mode == "INDEX LEVELS":
    INDICES = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
    for name, sym in INDICES.items():
        res = get_live_signal(sym)
        if res:
            st.subheader(f"{name}: {res['p']}")
            st.markdown(f"### Trend: :{res['c']}[{res['s']} ABOVE {res['sl']}]")
            st.divider()

# --- CATEGORY: COMMODITY ---
else:
    # (Aapka purana commodity code yahan rahega)
    st.info("Commodity Section is Active. Select from Sidebar.")
