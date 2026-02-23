import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY LIVE TERMINAL", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem; background-color: #000;}</style>""", unsafe_allow_html=True)

# --- 1. SAFE DATA FETCHING ---
def get_live_nifty():
    try:
        # Fetching 2-day data to ensure we have a price even if 1-day is lagging
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period="2d", interval="1m")
        return df['Close'].iloc[-1] if not df.empty else None
    except: return None

ltp = get_live_nifty()

# --- 2. DISPLAY PANEL ---
pcr_val = 2.01 #
pcr_color = "#ff1744" if pcr_val > 1.2 else "#00ff66"

if ltp:
    st.markdown(f"""
        <div style='text-align: center; background: #111; padding: 15px; border-radius: 15px; border: 2px solid {pcr_color};'>
            <h3 style='color: {pcr_color}; margin: 0;'>PCR: {pcr_val} | BEARISH ⚠️</h3>
            <h1 style='color: white; font-size: 55px; margin: 5px 0;'>{ltp:,.2f}</h1>
            <p style='color: gray; margin: 0;'>NIFTY 50 LIVE SPOT</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("🔄 Connecting to Exchange... Please wait 10 seconds.")
    time.sleep(10)
    st.rerun()

# --- 3. BREAKOUT SCANNER WITH T1/T2 & SL ---
st.markdown("<h3 style='color: yellow; text-align: center; margin-top: 15px;'>⚡ LIVE LEVELS & TARGETS</h3>", unsafe_allow_html=True)

# Column 1: BREAKOUT (BUY)
c1, c2 = st.columns(2)
with c1:
    st.markdown("<p style='color: #00ff66; font-weight: bold; border-bottom: 2px solid #00ff66;'>🚀 BUY ABOVE</p>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: #002b11; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
            <b style='color: white;'>RELIANCE</b><br>
            <span style='color: #00ff66;'>Above: 2985</span><br>
            <span style='color: #ff9800; font-size: 11px;'>SL: 2960</span><br>
            <span style='color: white; font-size: 11px;'>T1: 3005 | T2: 3025</span>
        </div>
    """, unsafe_allow_html=True)

# Column 2: BREAKDOWN (SELL)
with c2:
    st.markdown("<p style='color: #ff1744; font-weight: bold; border-bottom: 2px solid #ff1744;'>📉 SELL BELOW</p>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: #2b0000; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
            <b style='color: white;'>HDFCBANK</b><br>
            <span style='color: #ff1744;'>Below: 1640</span><br>
            <span style='color: #ff9800; font-size: 11px;'>SL: 1655</span><br>
            <span style='color: white; font-size: 11px;'>T1: 1625 | T2: 1610</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: gray; font-size: 10px;'>Last Refresh: {datetime.now().strftime('%I:%M:%S %p')}</p>", unsafe_allow_html=True)
time.sleep(15)
st.rerun()
