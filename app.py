import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX MEGA SCANNER", layout="wide")

# Sidebar - Yahan se Category wapas aayegi
st.sidebar.title("🛠️ CATEGORY MENU")
app_mode = st.sidebar.radio("CHOOSE SCANNER", ["STOCKS (Breakout)", "COMMODITY", "INDEX LEVELS"])

def get_smart_signal(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 10: return None
        
        cp = data['Close'].iloc[-1]
        avg_vol = data['Volume'].mean()
        curr_vol = data['Volume'].iloc[-1]
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        
        # High Volume Breakout Logic
        if cp > ema and curr_vol > (avg_vol * 1.5):
            return {"name": ticker.split('.')[0], "sig": "SIGNAL", "lvl": f"BULLISH BREAKOUT ABOVE {round(ema, 2)}", "clr": "green"}
        elif cp < ema and curr_vol > (avg_vol * 1.5):
            return {"name": ticker.split('.')[0], "sig": "SIGNAL", "lvl": f"BEARISH BREAKDOWN BELOW {round(ema, 2)}", "clr": "red"}
        return None
    except:
        return None

# --- UI DISPLAY ---
st.markdown(f"<h1 style='text-align: center;'>🚀 {app_mode} LIVE</h1>", unsafe_allow_html=True)
st.markdown("---")

# List Selection based on Category
if app_mode == "STOCKS (Breakout)":
    # Yahan Nifty 100+ stocks ki list hai, aap aur bhi add kar sakte hain
    LIST = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARATFORG.NS", "TATAMOTORS.NS", "SBIN.NS", "INFY.NS", "JINDALSTEL.NS", "ADANIPORTS.NS", "TITAN.NS", "M&M.NS"]
elif app_mode == "COMMODITY":
    LIST = ["CL=F", "NG=F", "GC=F"]
else:
    LIST = ["^NSEI", "^NSEBANK"]

found = False
for stock in LIST:
    res = get_smart_signal(stock)
    if res:
        found = True
        c1, c2, c3 = st.columns([2, 1, 3])
        c1.subheader(res['name'])
        c2.markdown(f"<div style='background-color:{res['clr']}; color:white; padding:5px; border-radius:5px; text-align:center;'>{res['sig']}</div>", unsafe_allow_html=True)
        c3.markdown(f"<h3 style='color:{res['clr']};'>{res['lvl']}</h3>", unsafe_allow_html=True)
        st.divider()

if not found:
    st.info(f"Searching for real breakouts in {app_mode}... Agar koi stock level cross karega tabhi yahan dikhega.")
