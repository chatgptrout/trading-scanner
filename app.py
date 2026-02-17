import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# Sidebar
st.sidebar.title("🛠️ CATEGORY MENU")
app_mode = st.sidebar.radio("CHOOSE SCANNER", ["STOCKS (Breakout)", "COMMODITY", "INDEX LEVELS"])

def get_always_on_signal(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 5: return None
        
        cp = data['Close'].iloc[-1]
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        
        # Target/SL Logic
        diff = cp * 0.005 
        
        if cp > ema:
            return {"p": round(cp, 2), "s": "BULLISH", "lvl": f"ABOVE {round(ema, 2)}", "t": round(cp + diff, 2), "sl": round(ema, 2), "c": "green"}
        else:
            return {"p": round(cp, 2), "s": "BEARISH", "lvl": f"BELOW {round(ema, 2)}", "t": round(cp - diff, 2), "sl": round(ema, 2), "c": "red"}
    except: return None

# --- UI DISPLAY ---
st.markdown(f"<h1 style='text-align: center;'>🚀 {app_mode} LIVE</h1>", unsafe_allow_html=True)

if app_mode == "COMMODITY":
    COMM_LIST = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    
    st.markdown("---")
    h = st.columns([2, 1, 2, 2, 2])
    h[0].write("**NAME**"); h[1].write("**SIGNAL**"); h[2].write("**ENTRY**"); h[3].write("**TARGET**"); h[4].write("**STOPLOSS**")
    st.divider()

    for name, sym in COMM_LIST.items():
        res = get_always_on_signal(sym)
        if res:
            c = st.columns([2, 1, 2, 2, 2])
            c[0].subheader(name)
            c[1].markdown(f"<div style='background-color:{res['c']}; color:white; padding:5px; border-radius:5px; text-align:center;'>SIGNAL</div>", unsafe_allow_html=True)
            c[2].write(f"📈 {res['p']}")
            c[3].write(f"🎯 {res['t']}")
            c[4].write(f"🛑 {res['sl']}")
            st.divider()
