import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX BREAKOUT", layout="wide")
st.markdown("<h1 style='text-align: center;'>🚀 Real-Time Breakout Scanner</h1>", unsafe_allow_html=True)

# Extended Stock List for Scanning
STOCK_LIST = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARATFORG.NS", "TATAMOTORS.NS", 
    "SBIN.NS", "ICICIBANK.NS", "INFY.NS", "ADANIPORTS.NS", "JINDALSTEL.NS",
    "BAJFINANCE.NS", "TITAN.NS", "SUNPHARMA.NS", "M&M.NS", "AXISBANK.NS"
]

def get_breakout_signal(ticker):
    try:
        # Fetching 15-min data
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 20: return None
        
        current_price = data['Close'].iloc[-1]
        avg_vol = data['Volume'].mean()
        current_vol = data['Volume'].iloc[-1]
        ema_20 = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        
        # BREAKOUT LOGIC: Price > EMA AND Volume > Average Volume
        is_breakout = current_price > ema_20 and current_vol > (avg_vol * 1.5)
        is_breakdown = current_price < ema_20 and current_vol > (avg_vol * 1.5)

        if is_breakout:
            return {"name": ticker.split('.')[0], "status": "BULLISH BREAKOUT", "level": round(ema_20, 2), "color": "green"}
        elif is_breakdown:
            return {"name": ticker.split('.')[0], "status": "BEARISH BREAKDOWN", "level": round(ema_20, 2), "color": "red"}
        return None
    except:
        return None

# UI Display
st.markdown("---")
cols = st.columns([2, 2, 3])
cols[0].write("**SCRIPT**")
cols[1].write("**SIGNAL**")
cols[2].write("**STRATEGY LEVELS**")
st.markdown("---")

found = False
for stock in STOCK_LIST:
    res = get_breakout_signal(stock)
    if res:
        found = True
        c1, c2, c3 = st.columns([2, 2, 3])
        c1.subheader(res['name'])
        c2.markdown(f"<div style='background-color:{res['color']}; color:white; padding:5px; border-radius:5px; text-align:center;'>SIGNAL</div>", unsafe_allow_html=True)
        c3.markdown(f"<h3 style='color:{res['color']};'>{res['status']} ABOVE {res['level']}</h3>", unsafe_allow_html=True)
        st.divider()

if not found:
    st.info("Searching for high-volume breakouts... Abhi koi strong breakout nahi mil raha.")

st.caption("Note: Wahi stocks dikh rahe hain jinme Volume aur Price dono ka breakout hai.")
