import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Auto-Scanner")

# Professional Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    th { background-color: #222 !important; color: #ffca28 !important; font-size: 16px; border: 1px solid #444 !important; }
    td { font-size: 15px; border: 1px solid #333 !important; padding: 10px !important; }
    .status-box { padding: 10px; border-radius: 5px; background-color: #1a1a1a; border-left: 5px solid #ffca28; }
    </style>
    """, unsafe_allow_html=True)

# --- Header with Auto-Refresh Info ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.title("📟 Santosh Live Auto-Scanner")
with col_t2:
    last_update = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<div class='status-box'><b>Last Update:</b> {last_update}<br>Next refresh in 60s</div>", unsafe_allow_html=True)

# --- NSE Stock List (Top Traded) ---
nse_list = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "AXISBANK", "SBIN", "BHARTIARTL", 
    "LICI", "ITC", "HINDUNILVR", "LT", "BAJFINANCE", "TATAMOTORS", "SUNPHARMA", "MARUTI", 
    "ADANIENT", "KOTAKBANK", "TITAN", "ONGC", "TATASTEEL", "NTPC", "ASIANPAINT", "HAL", 
    "COALINDIA", "BAJAJFINSV", "ADANIPORTS", "JSWSTEEL", "HCLTECH", "M&M", "DRREDDY", 
    "ADANIPOWER", "CIPLA", "BEL", "ZOMATO", "DLF", "GAIL", "WIPRO", "GNFC", "INTELLECT"
]

# User selection saved in session state
if 'selected_stocks' not in st.session_state:
    st.session_state.selected_stocks = ["RELIANCE", "SBIN", "TATAMOTORS", "DLF", "GNFC"]

selected_names = st.multiselect("Stocks add/remove karein:", options=sorted(nse_list), default=st.session_state.selected_stocks)
st.session_state.selected_stocks = selected_names

def fetch_data(names):
    rows = []
    tickers = [n + ".NS" for n in names]
    for t in tickers:
        try:
            s = yf.Ticker(t)
            df = s.history(period="2d")
            if df.empty: continue
            
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = round(df['Open'].iloc[-1], 2)
            high = round(df['High'].iloc[-1], 2)
            low = round(df['Low'].iloc[-1], 2)
            
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > df['Close'].iloc[-2] else "Negative"
            
            rows.append({
                "Action": action,
                "Name": t.replace(".NS", ""),
                "Entry Price": open_p,
                "Stop Loss": round(low * 0.998, 2) if action == "BUY EXIT" else round(high * 1.002, 2),
                "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Financial Trend": trend,
                "Valuation": "Attractive" if trend == "Positive" else "Fair",
                "Segment": "Cash & Fut"
            })
        except: continue
    return pd.DataFrame(rows)

# Main Table Display
if st.session_state.selected_stocks:
    data = fetch_data(st.session_state.selected_stocks)
    if not data.empty:
        def style_rows(val):
            if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
            if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
            if val == 'Positive': return 'color: #2ecc71; font-weight: bold'
            if val == 'Negative': return 'color: #e74c3c; font-weight: bold'
            return ''

        st.table(data.style.map(style_rows, subset=['Action', 'Financial Trend']))
    
    # --- AUTO REFRESH LOGIC ---
    time.sleep(60) # 60 seconds wait karega
    st.rerun()    # Fir apne aap refresh kar dega
else:
    st.warning("Please select at least one stock.")
