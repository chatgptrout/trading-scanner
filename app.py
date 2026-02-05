import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time

st.set_page_config(page_title="Santosh AI Scanner", layout="wide")
st.title("SANTOSH AI BUY/SELL SCANNER (EMA + RSI)")

watchlist = {
    'NIFTY 50': '^NSEI',
    'BANK NIFTY': '^NSEBANK',
    'RELIANCE': 'RELIANCE.NS',
    'CRUDE OIL': 'CL=F',
    'TATA MOTORS': 'TATAMOTORS.NS'
}

cols = st.columns(len(watchlist))

for i, (name, ticker) in enumerate(watchlist.items()):
    with cols[i]:
        try:
            # Data for Indicator calculation
            df = yf.download(ticker, period='5d', interval='15m', progress=False)
            if not df.empty:
                # Indicators: 20 EMA and 14 RSI
                df['EMA_20'] = ta.ema(df['Close'], length=20)
                df['RSI'] = ta.rsi(df['Close'], length=14)
                
                current_price = df['Close'].iloc[-1]
                current_rsi = df['RSI'].iloc[-1]
                current_ema = df['EMA_20'].iloc[-1]
                
                # Logic: Buy if Price > EMA and RSI > 62
                # Logic: Sell if Price < EMA and RSI < 35
                st.subheader(name)
                st.write(f"Price: ₹{current_price:.2f}")
                st.write(f"RSI: {current_rsi:.1f}")

                if current_price > current_ema and current_rsi > 62:
                    st.success("🚀 STRONG BUY")
                    st.toast(f"{name} Buy Signal!")
                elif current_price < current_ema and current_rsi < 35:
                    st.error("📉 STRONG SELL")
                    st.toast(f"{name} Sell Signal!")
                else:
                    st.warning("⏳ WAIT / NEUTRAL")
        except:
            st.write(f"Scanning {name}...")

# Auto-refresh every 30 seconds for office monitoring
time.sleep(30)
st.rerun()
