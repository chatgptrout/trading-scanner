import streamlit as st
import yfinance as yf
import pandas as pd

# Page setup - Pura screen use karne ke liye
st.set_page_config(layout="wide", page_title="Santosh Stock Scanner")

# Styling: Table ko black aur professional look dene ke liye
st.markdown("""
    <style>
    .main { background-color: #1e1e1e; }
    div.stButton > button:first-child { background-color: #ffca28; color: black; font-weight: bold; }
    .css-12w0qpk { border: 1px solid #444; }
    thead tr th { background-color: #333 !important; color: #ffca28 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 Pro-Trader Intraday Scanner")

# Stocks List (Aap yahan tickers badal sakte hain)
tickers = [
    "GNFC.NS", "INTELLECT.NS", "DRREDDY.NS", "ALKEM.NS", "AXISBANK.NS", 
    "M&M.NS", "BALRAMCHIN.NS", "COALINDIA.NS", "ICICIBANK.NS", "HAL.NS"
]

def fetch_scanner_data(stocks):
    rows = []
    for t in stocks:
        try:
            s = yf.Ticker(t)
            hist = s.history(period="2d")
            if len(hist) < 2: continue
            
            prev_close = hist['Close'].iloc[-2]
            cmp = round(hist['Close'].iloc[-1], 2)
            open_p = hist['Open'].iloc[-1]
            high = hist['High'].iloc[-1]
            low = hist['Low'].iloc[-1]

            # Image ke hisaab se Logic
            action = "BUY" if cmp > open_p else "SELL"
            trend = "Positive" if cmp > prev_close else "Negative"
            
            # Entry, SL, Target Calculations
            entry = open_p
            if action == "BUY":
                sl = round(low * 0.998, 2)
                target = round(cmp * 1.015, 2)
                valuation = "Attractive" if cmp < (high * 0.99) else "Fair"
            else:
                sl = round(high * 1.002, 2)
                target = round(cmp * 0.985, 2)
                valuation = "Expensive"

            rows.append({
                "Action": action,
                "Symbol": t.replace(".NS", ""),
                "Entry Price": entry,
                "Stop Loss": sl,
                "CMP": cmp,
                "Target": target,
                "Financial Trend": trend,
                "Valuation": valuation,
                "Segment": "Cash & Fut"
            })
        except:
            continue
    return pd.DataFrame(rows)

# Action Buttons
col1, col2 = st.columns([1, 8])
with col1:
    refresh = st.button("🔄 REFRESH")

# Display Table
data = fetch_scanner_data(tickers)

if not data.empty:
    # Color coding logic for the table
    def color_action(val):
        color = '#2ecc71' if val == 'BUY' else '#e74c3c'
        return f'background-color: {color}; color: white; font-weight: bold'

    def color_trend(val):
        color = '#2ecc71' if val == 'Positive' else '#e74c3c'
        return f'color: {color}; font-weight: bold'

    styled_df = data.style.applymap(color_action, subset=['Action']) \
                          .applymap(color_trend, subset=['Financial Trend'])

    st.table(styled_df)
else:
    st.error("Data fetch nahi ho raha. Check Internet.")

st.info("Note: Yahoo Finance data is slightly delayed. For zero-delay, Dhan API is recommended.")
