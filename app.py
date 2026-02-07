import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Tradex Live Signals")

# Custom Tradex Style UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .tradex-header { background-color: #f8f9fa; padding: 10px; border-bottom: 2px solid #eee; margin-bottom: 20px; }
    .status-live { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .priority-tag { background-color: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #bbdefb; }
    th { color: #888 !important; font-size: 12px !important; text-transform: uppercase; border-bottom: 1px solid #eee !important; }
    td { padding: 15px !important; border-bottom: 1px solid #f5f5f5 !important; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Reversal & Trend Logic
def get_tradex_logic():
    # Watchlist based on your images
    watchlist = {"NIFTY": "^NSEI", "CRUDE FEB FUT": "CL=F", "BANK NIFTY": "^NSEBANK", "POWERINDIA": "POWERINDIA.NS"}
    signals = []
    
    for name, sym in watchlist.items():
        try:
            data = yf.download(sym, period="2d", interval="5m", progress=False)
            if data.empty: continue
            
            h, l, cmp = round(data['High'].max(), 2), round(data['Low'].min(), 2), round(data['Close'].iloc[-1], 2)
            
            # Reversal Logic (Tradex Style)
            if cmp >= (h * 0.999):
                signals.append({"SCRIPT": name, "LEVELS": f"REVERSAL POSSIBLE FROM {h}", "MSG": "OVERBOUGHT ZONE", "PRIORITY": "MEDIUM"})
            elif cmp <= (l * 1.001):
                signals.append({"SCRIPT": name, "LEVELS": f"BEARISH BELOW {l}", "MSG": "BREAKDOWN IMMINENT", "PRIORITY": "HIGH"})
        except: continue
    return signals

# --- DISPLAY ---
st.markdown("<div class='tradex-header'><b>TRADEX</b> <span class='status-live'>LIVE</span> &nbsp;&nbsp; <small>Search signals...</small></div>", unsafe_allow_html=True)

live_signals = get_tradex_logic()

if live_signals:
    # Building the table exactly like image_c5aa14.jpg
    c1, c2, c3, c4 = st.columns([1.5, 2, 2.5, 1])
    c1.write("**SCRIPT**")
    c2.write("**SIGNAL**")
    c3.write("**LEVELS / MESSAGE**")
    c4.write("**PRIORITY**")
    st.markdown("<hr style='margin:0'>", unsafe_allow_html=True)
    
    for s in live_signals:
        r1, r2, r3, r4 = st.columns([1.5, 2, 2.5, 1])
        r1.write(f"**{s['SCRIPT']}**")
        r2.markdown("<span style='color:#888; background:#f0f0f0; padding:3px 8px; border-radius:4px;'>SIGNAL</span>", unsafe_allow_html=True)
        r3.write(f"{s['LEVELS']}")
        r4.markdown(f"<span class='priority-tag'>{s['PRIORITY']}</span>", unsafe_allow_html=True)
else:
    st.info("No active high-probability signals. Waiting for reversal levels...")

time.sleep(60)
st.rerun()
