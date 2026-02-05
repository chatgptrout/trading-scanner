import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH BULL-BEAR AI", layout="wide")

# Stylish CSS for signals
st.markdown("""
    <style>
    .signal-box { padding: 30px; border-radius: 20px; text-align: center; color: white; font-family: sans-serif; }
    .bullish { background: linear-gradient(135deg, #00b09b, #96c93d); border: 5px solid #ffffff; }
    .bearish { background: linear-gradient(135deg, #cb2d3e, #ef473a); border: 5px solid #ffffff; }
    .neutral { background: #2c3e50; opacity: 0.8; }
    .symbol-font { font-size: 80px; margin: 0; }
    .price-font { font-size: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SANTOSH MOMENTUM TRACKER")

watchlist = {'NIFTY 50': '^NSEI', 'BANK NIFTY': '^NSEBANK', 'RELIANCE': 'RELIANCE.NS', 'CRUDE OIL': 'CL=F', 'TATA MOTORS': 'TATAMOTORS.NS'}

cols = st.columns(len(watchlist))

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

                # BULLISH/BEARISH LOGIC
                if price > ema and rsi > 62:
                    st.markdown(f'''<div class="signal-box bullish">
                        <p class="symbol-font">🐂</p>
                        <h3>{name}</h3>
                        <p class="price-font">₹{price:.1f}</p>
                        <p>BULLISH MOVEMENT</p>
                    </div>''', unsafe_allow_html=True)
                elif price < ema and rsi < 35:
                    st.markdown(f'''<div class="signal-box bearish">
                        <p class="symbol-font">🐻</p>
                        <h3>{name}</h3>
                        <p class="price-font">₹{price:.1f}</p>
                        <p>BEARISH MOVEMENT</p>
                    </div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''<div class="signal-box neutral">
                        <p class="symbol-font">⚖️</p>
                        <h3>{name}</h3>
                        <p class="price-font">₹{price:.1f}</p>
                        <p>WAITING...</p>
                    </div>''', unsafe_allow_html=True)
        except:
            st.write("🔄")

time.sleep(15)
st.rerun()
