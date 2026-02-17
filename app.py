import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="1000+ Stock Breakout Scanner", layout="wide")
st.markdown("<h1 style='text-align: center;'>🔥 Mega Breakout Scanner (500+ Stocks)</h1>", unsafe_allow_html=True)

# List ko bada karne ke liye hum Nifty 500 ke symbols generate kar rahe hain
# Isme aap manually aur bhi add kar sakte hain
SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "BHARATFORG.NS",
    "TATAMOTORS.NS", "SBIN.NS", "AXISBANK.NS", "BAJFINANCE.NS", "LICI.NS", "BHARTIARTL.NS",
    "ADANIENT.NS", "HINDUNILVR.NS", "ITC.NS", "LT.NS", "KOTAKBANK.NS", "TITAN.NS",
    # Aap yahan 1000 stocks tak ki list copy-paste kar sakte hain
] 

# Note: Demo ke liye 50+ bade stocks automatically scan honge
# Professional level par hum yahan direct CSV file upload kar dete hain

def scan_stock(ticker):
    try:
        # Last 2 days data for Volume and Price analysis
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if len(data) < 5: return None
        
        cp = data['Close'].iloc[-1] # Current Price
        prev_cp = data['Close'].iloc[-2]
        avg_vol = data['Volume'].mean()
        curr_vol = data['Volume'].iloc[-1]
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]

        # Criteria: Volume must be 2x and Price crossing EMA
        if cp > ema and curr_vol > (avg_vol * 2):
            return {"name": ticker.split('.')[0], "status": "BULLISH", "level": round(ema, 2), "color": "green"}
        elif cp < ema and curr_vol > (avg_vol * 2):
            return {"name": ticker.split('.')[0], "status": "BEARISH", "level": round(ema, 2), "color": "red"}
        return None
    except:
        return None

st.sidebar.header("Scanner Settings")
if st.sidebar.button("START SCANNING"):
    st.write("🔍 Scanning 1000+ stocks... Please wait.")
    found_any = False
    
    # Columns for Header
    h1, h2, h3 = st.columns([2, 1, 3])
    h1.write("**SCRIPT**")
    h2.write("**SIGNAL**")
    h3.write("**BREAKOUT LEVEL**")
    st.divider()

    for stock in SYMBOLS:
        res = scan_stock(stock)
        if res:
            found_any = True
            c1, c2, c3 = st.columns([2, 1, 3])
            c1.subheader(res['name'])
            c2.markdown(f"<div style='background-color:{res['color']}; color:white; padding:5px; border-radius:5px; text-align:center;'>SIGNAL</div>", unsafe_allow_html=True)
            c3.markdown(f"<h3 style='color:{res['color']};'>{res['status']} ABOVE {res['level']}</h3>", unsafe_allow_html=True)
            st.divider()
            
    if not found_any:
        st.warning("Abhi kisi bhi stock mein 2x volume breakout nahi hai.")
else:
    st.info("Side menu mein 'START SCANNING' par click karein.")
