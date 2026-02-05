import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH PRO AI", layout="wide")

# Custom CSS for that "Maza Aa Gaya" Look
st.markdown("""
    <style>
    .big-font { font-size:50px !important; font-weight: bold; }
    .signal-card { padding: 20px; border-radius: 15px; text-align: center; color: white; margin: 10px; }
    .buy-bg { background-color: #2ecc71; }
    .sell-bg { background-color: #e74c3c; }
    .wait-bg { background-color: #34495e; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 SANTOSH PRO AI: ACTION DASHBOARD")

watchlist = {'NIFTY 50': '^NSEI', 'BANK NIFTY': '^NSEBANK', 'RELIANCE': 'RELIANCE.NS', 'CRUDE OIL': 'CL=F'}

cols = st.columns(4)

for i, (name, ticker) in enumerate(watchlist.items()):
    with cols[i]:
        try:
            df = yf.download(ticker, period='2d', interval='5m', progress=False)
            if not df.empty:
                df['EMA'] = ta.ema(df['Close'], length=20)
                df['RSI'] = ta.rsi(df['Close'], length=14)
                
                price = df['Close'].iloc[-1]
                rsi = df['RSI'].iloc[-1]
                ema = df['EMA'].iloc[-1]

                # SIGNAL LOGIC
                if price > ema and rsi > 62:
                    st.markdown(f'<div class="signal-card buy-bg"><h3>{name}</h3><p class="big-font">BUY 🚀</p><h1>₹{price:.1f}</h1><p>RSI: {rsi:.1f}</p></div>', unsafe_allow_html=True)
                elif price < ema and rsi < 35:
                    st.markdown(f'<div class="signal-card sell-bg"><h3>{name}</h3><p class="big-font">SELL 📉</p><h1>₹{price:.1f}</h1><p>RSI: {rsi:.1f}</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="signal-card wait-bg"><h3>{name}</h3><p class="big-font">WAIT ⏳</p><h1>₹{price:.1f}</h1><p>RSI: {rsi:.1f}</p></div>', unsafe_allow_html=True)
        except:
            st.write("Loading...")

time.sleep(15) # Fast Refresh for Scalping
st.rerun()
