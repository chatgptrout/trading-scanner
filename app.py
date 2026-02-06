import streamlit as st
import yfinance as yf
import pandas as pd

# Page layout
st.set_page_config(layout="wide", page_title="Santosh Stock Scanner")

# Custom CSS for Motilal Oswal Look (Dark Theme & Professional Table)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    table { width: 100% !important; border-collapse: collapse; }
    th { background-color: #333333 !important; color: #ffca28 !important; text-align: left !important; }
    td { border: 0.1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 Pro-Trader Intraday Scanner")

# Stock List
tickers = ["GNFC.NS", "INTELLECT.NS", "DRREDDY.NS", "ALKEM.NS", "AXISBANK.NS", "M&M.NS", "COALINDIA.NS", "ICICIBANK.NS", "HAL.NS", "DLF.NS"]

def get_data(stocks):
    rows = []
    for t in stocks:
        try:
            s = yf.Ticker(t)
            df = s.history(period="2d")
            if df.empty: continue
            
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = df['Open'].iloc[-1]
            high = df['High'].iloc[-1]
            low = df['Low'].iloc[-1]
            
            # Trading Logic
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > open_p else "Negative"
            
            rows.append({
                "Action": action,
                "Name": t.replace(".NS", ""),
                "Entry Price": round(open_p, 2),
                "Stop Loss": round(low * 0.995, 2) if action == "BUY EXIT" else round(high * 1.005, 2),
                "CMP": cmp,
                "Target": round(cmp * 1.01, 2) if action == "BUY EXIT" else round(cmp * 0.99, 2),
                "Financial Trend": trend,
                "Valuation": "Attractive" if trend == "Positive" else "Expensive",
                "Segment": "Cash & Fut"
            })
        except:
            continue
    return pd.DataFrame(rows)

if st.button('🔄 REFRESH DATA'):
    data = get_data(tickers)
else:
    data = get_data(tickers)

if not data.empty:
    # Error Fix: .applymap() ki jagah .map() use kiya hai
    def color_action(val):
        bg = '#2ecc71' if 'BUY' in val else '#e74c3c'
        return f'background-color: {bg}; color: white; font-weight: bold'

    def color_trend(val):
        color = '#2ecc71' if val == 'Positive' else '#e74c3c'
        return f'color: {color}; font-weight: bold'

    # Displaying clean table without charts
    styled_df = data.style.map(color_action, subset=['Action']) \
                          .map(color_trend, subset=['Financial Trend'])
    
    st.table(styled_df)

st.write("---")
st.caption("Data source: Yahoo Finance | Version: 1.0 (Santosh Scanner)")
