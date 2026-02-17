import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX PRO", layout="wide")

# Sidebar
st.sidebar.title("🛠️ CATEGORY MENU")
app_mode = st.sidebar.radio("CHOOSE SCANNER", ["STOCKS (Breakout)", "COMMODITY", "INDEX LEVELS"])

def get_pro_signal(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 10: return None
        
        cp = data['Close'].iloc[-1]
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        high_15m = data['High'].iloc[-1]
        low_15m = data['Low'].iloc[-1]

        # Calculation for Target & SL
        diff = cp * 0.005 # 0.5% buffer
        
        if cp > ema:
            return {
                "name": ticker, "status": "BULLISH", "entry": round(cp, 2),
                "sl": round(ema, 2), "t1": round(cp + diff, 2), "clr": "green"
            }
        else:
            return {
                "name": ticker, "status": "BEARISH", "entry": round(cp, 2),
                "sl": round(ema, 2), "t1": round(cp - diff, 2), "clr": "red"
            }
    except: return None

# --- UI DISPLAY ---
st.markdown(f"<h1 style='text-align: center;'>🚀 {app_mode} LIVE</h1>", unsafe_allow_html=True)

if app_mode == "COMMODITY":
    # MCX Symbols using Yahoo Finance format
    COMM_LIST = {
        "CRUDE OIL": "CL=F", 
        "NATURAL GAS": "NG=F", 
        "GOLD": "GC=F", 
        "SILVER": "SI=F"
    }
    
    # Table Header
    h1, h2, h3, h4, h5 = st.columns([2, 1, 2, 2, 2])
    h1.write("**COMMODITY**")
    h2.write("**SIGNAL**")
    h3.write("**ENTRY**")
    h4.write("**TARGET**")
    h5.write("**STOPLOSS**")
    st.divider()

    for name, sym in COMM_LIST.items():
        res = get_pro_signal(sym)
        if res:
            c1, c2, c3, c4, c5 = st.columns([2, 1, 2, 2, 2])
            c1.subheader(name)
            c2.markdown(f"<div style='background-color:{res['clr']}; color:white; padding:5px; border-radius:5px; text-align:center;'>SIGNAL</div>", unsafe_allow_html=True)
            c3.write(f"📈 {res['entry']}")
            c4.write(f"🎯 {res['t1']}")
            c5.write(f"🛑 {res['sl']}")
            st.divider()

elif app_mode == "STOCKS (Breakout)":
    st.info("Searching for Stock Breakouts...")
    # (Purana stock breakout logic yahan kaam karega)

else:
    st.info("Nifty & Bank Nifty Levels Loading...")
