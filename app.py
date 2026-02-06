 import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Stock Scanner")

st.title("🚀 Real-Time Intraday Scanner")
st.write("Data Source: Yahoo Finance (Delayed by ~1 min)")

# List of Stocks (Aap yahan apne stocks add kar sakte hain)
tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "SBIN.NS", "INFY.NS"]

def get_live_data(stocks):
    data_list = []
    for ticker in stocks:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1d")
        
        if not df.empty:
            cmp = round(df['Close'].iloc[-1], 2)
            high = df['High'].iloc[-1]
            low = df['Low'].iloc[-1]
            
            # Simple Logic for Entry/SL/Target (Aap ise change kar sakte hain)
            entry = round(cmp, 2)
            stop_loss = round(cmp * 0.99, 2) # 1% SL
            target = round(cmp * 1.02, 2)    # 2% Target
            
            data_list.append({
                "Symbol": ticker.replace(".NS", ""),
                "Action": "BUY" if cmp > df['Open'].iloc[-1] else "SELL",
                "CMP": cmp,
                "Entry Price": entry,
                "Stop Loss": stop_loss,
                "Target": target,
                "Financial Trend": "Positive" if cmp > df['Open'].iloc[-1] else "Negative"
            })
    return pd.DataFrame(data_list)

# Refresh Button
if st.button('Refresh Data'):
    df_final = get_live_data(tickers)
    # Displaying Table without Charts
    st.table(df_final)
else:
    df_final = get_live_data(tickers)
    st.table(df_final)

# Formatting
st.markdown("""
<style>
    .stTable { font-size: 20px !important; }
</style>
""", unsafe_allow_html=True)
