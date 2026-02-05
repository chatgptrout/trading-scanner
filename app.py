import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

# Dashboard Page Config
st.set_page_config(page_title="SANTOSH PRO AI", layout="wide")

# CSS for Futuristic Dark Theme (from your screenshot)
st.markdown("""
    <style>
    .main { background-color: #010b14; color: white; }
    .stApp { background-color: #010b14; }
    .signal-card { 
        background: linear-gradient(145deg, #0d1b2a, #1b263b);
        border-radius: 20px; border: 1px solid #00f2ff;
        padding: 25px; text-align: center; color: white;
    }
    .buy-btn { background-color: #00ff88; color: black; font-weight: bold; border-radius: 10px; padding: 10px 20px; display: inline-block; margin-top: 10px; }
    .sell-btn { background-color: #ff4b2b; color: white; font-weight: bold; border-radius: 10px; padding: 10px 20px; display: inline-block; margin-top: 10px; }
    .stock-title { font-size: 24px; font-weight: bold; color: #00f2ff; }
    .price-text { font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SANTOSH AI COMMAND CENTER")

# Stocks from your interest list
watchlist = {'RELIANCE': 'RELIANCE.NS', 'NIFTY 50': '^NSEI', 'BANK NIFTY': '^NSEBANK', 'CRUDE OIL': 'CL=F'}

cols = st.columns(4)

for i, (name, ticker) in enumerate(watchlist.items()):
    with cols[i]:
        try:
            df = yf.download(ticker, period='5d', interval='15m', progress=False)
            if not df.empty:
                df['EMA'] = ta.ema(df['Close'], length=20)
                df['RSI'] = ta.rsi(df['Close'], length=14)
                
                price = df['Close'].iloc[-1]
                rsi = df['RSI'].iloc[-1]
                ema = df['EMA'].iloc[-1]
                change = price - df['Close'].iloc[-2]

                # SIGNAL LOGIC (EMA + RSI 62/35)
                status = "NEUTRAL"
                signal_class = "wait-bg"
                btn_html = "WAITING"

                if price > ema and rsi > 62:
                    status = "STRONG BULLISH"
                    btn_html = '<div class="buy-btn">BUY SIGNAL</div>'
                elif price < ema and rsi < 35:
                    status = "STRONG BEARISH"
                    btn_html = '<div class="sell-btn">SELL SIGNAL</div>'

                # Display Card
                st.markdown(f'''
                    <div class="signal-card">
                        <div class="stock-title">{name}</div>
                        <div class="price-text">₹{price:.2f}</div>
                        <div style="color: {"#00ff88" if change > 0 else "#ff4b2b"}">{change:+.2f}</div>
                        <hr style="border: 0.5px solid #00f2ff">
                        <p>RSI: {rsi:.1f} | EMA: {ema:.1f}</p>
                        <p>{status}</p>
                        {btn_html}
                    </div>
                ''', unsafe_allow_html=True)
        except:
            st.write("📡 Scanning...")

# Automatic fast refresh for scalping
time.sleep(15)
st.rerun()
