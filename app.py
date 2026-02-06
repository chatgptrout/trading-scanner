import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(layout="wide", page_title="Santosh Power Scanner")

# Custom UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { padding: 10px; border-radius: 8px; border: 1px solid #333; text-align: center; background-color: #111; }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border-bottom: 1px solid #222 !important; padding: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Top Bar Indices
def get_indices():
    tickers = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT GAS": "NG=F"}
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="1d", interval="5m")
            if not data.empty:
                h, l, cmp = data['High'].max(), data['Low'].min(), data['Close'].iloc[-1]
                status, color = ("BULLISH", "#2ecc71") if cmp > (h+l)/2 else ("BEARISH", "#e74c3c")
                results.append({"name": name, "status": status, "cmp": round(cmp, 2), "color": color})
        except: continue
    return results

# 2. Filtering Logic (Power Signals Only)
high_volume_stocks = ["RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "DLF", "GNFC", "HAL", "BEL", "TRENT", "PNB", "BANKBARODA", "ADANIENT", "POWERGRID", "NTPC"] # Add more as needed

def get_filtered_signals():
    rows = []
    tickers = [t + ".NS" for t in high_volume_stocks]
    data = yf.download(tickers, period="2d", interval="5m", group_by='ticker', progress=False)
    
    for t in high_volume_stocks:
        try:
            df = data[t + ".NS"].dropna()
            if df.empty: continue
            h, l, cmp = round(df['High'].max(), 2), round(df['Low'].min(), 2), round(df['Close'].iloc[-1], 2)
            
            # FILTER: Sirf wo dikhao jo High ke 0.2% paas ho (Bullish) ya Low ke 0.2% paas ho (Bearish)
            is_bullish = cmp >= (h * 0.998)
            is_bearish = cmp <= (l * 1.002)
            
            if is_bullish or is_bearish:
                if is_bullish:
                    sig, lvl, col = "BULLISH", f"ABOVE {h}", "#2ecc71"
                    t1, t2, sl = round(h * 1.008, 2), round(h * 1.015, 2), round(h * 0.994, 2)
                else:
                    sig, lvl, col = "BEARISH", f"BELOW {l}", "#e74c3c"
                    t1, t2, sl = round(l * 0.992, 2), round(l * 0.985, 2), round(l * 1.006, 2)
                
                rows.append({"Symbol": t, "Signal": sig, "Level": lvl, "T1": t1, "T2": t2, "SL": sl, "Color": col})
        except: continue
    return rows

# --- DISPLAY ---
st.title("📟 Santosh Power Scanner (Action Stocks Only)")

# Top Indices
sigs = get_indices()
if sigs:
    cols = st.columns(len(sigs))
    for i, s in enumerate(sigs):
        with cols[i]:
            st.markdown(f"<div class='signal-card'><small>{s['name']}</small><h3 style='color:{s['color']}; margin:5px 0;'>{s['status']}</h3><b>{s['cmp']}</b></div>", unsafe_allow_html=True)

st.markdown("---")

# Filtered Table
filtered_stocks = get_filtered_signals()
if filtered_stocks:
    st.subheader(f"🔥 TRADEX: {len(filtered_stocks)} Active Signals")
    # Using a clean table or columns like your image
    for s in filtered_stocks:
        c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1.5, 1, 1, 1])
        c1.markdown(f"**{s['Symbol']}**")
        c2.markdown(f"<span style='color:{s['Color']}; font-weight:bold;'>{s['Signal']}</span>", unsafe_allow_html=True)
        c3.markdown(f"**{s['Level']}**")
        c4.write(f"🎯 {s['T1']}")
        c5.write(f"🚀 {s['T2']}")
        c6.write(f"🛑 {s['SL']}")
else:
    st.info("Searching for Power Breakouts... No active signals right now.")

time.sleep(60)
st.rerun()
