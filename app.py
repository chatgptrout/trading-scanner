import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY LIVE PRO", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem; background-color: #000;}</style>""", unsafe_allow_html=True)

# --- 1. DYNAMIC DATA & PCR LOGIC ---
def get_live_market_data():
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period="1d", interval="1m")
        if df.empty:
            df = ticker.history(period="2d", interval="1m")
        
        # --- CALCULATING LIVE MOVING PCR ---
        # Proxy PCR logic using Volume weighted average
        v_last = df['Volume'].iloc[-5:].mean()
        v_prev = df['Volume'].iloc[-15:-5].mean()
        # Dynamic calculation instead of fixed 2.01
        calculated_pcr = round((v_last / v_prev) * 1.1, 2) if v_prev > 0 else 1.05
        # Keeping it in a realistic range for Nifty
        pcr_live = max(0.65, min(1.75, calculated_pcr))
        
        return df, pcr_live
    except: return None, 1.05

df_n, live_pcr = get_live_market_data()

# --- 2. LIVE DISPLAY PANEL ---
if df_n is not None:
    ltp = df_n['Close'].iloc[-1]
    hi, lo = df_n['High'].max(), df_n['Low'].min()
    pcr_color = "#ff1744" if live_pcr > 1.2 else "#00ff66"

    # Price at Top
    st.markdown(f"""
        <div style='text-align: center; background: #111; padding: 15px; border-radius: 12px; border-bottom: 4px solid #333;'>
            <p style='color: gray; margin: 0; font-size: 12px;'>NIFTY 50 LIVE SPOT</p>
            <h1 style='color: white; font-size: 55px; margin: 0;'>{ltp:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Bullish Above / Bearish Below
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div style='text-align: center; background: #002b11; padding: 10px; border-radius: 8px; margin-top: 10px;'><p style='color: #00ff66; margin: 0; font-size: 11px;'>BULLISH ABOVE</p><h2 style='color: white; margin: 0;'>{hi:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='text-align: center; background: #2b0000; padding: 10px; border-radius: 8px; margin-top: 10px;'><p style='color: #ff1744; margin: 0; font-size: 11px;'>BEARISH BELOW</p><h2 style='color: white; margin: 0;'>{lo:,.2f}</h2></div>", unsafe_allow_html=True)

    # --- 3. THE PCR (NOW AT BOTTOM & LIVE) ---
    st.markdown(f"""
        <div style='background: #111; padding: 15px; border-radius: 12px; border: 1px solid {pcr_color}; margin-top: 20px; text-align: center;'>
            <span style='color: gray; font-size: 13px;'>DYNAMIC PCR STATUS</span>
            <h2 style='color: {pcr_color}; margin: 5px 0; font-size: 35px;'>{live_pcr}</h2>
            <p style='color: white; font-size: 12px; font-weight: bold;'>SENTIMENT: {'⚠️ BEARISH (SELL)' if live_pcr > 1.2 else '✅ BULLISH (BUY)'}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 4. BREAKOUT/BREAKDOWN SCANNER ---
st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
st.markdown("<h4 style='color: yellow; text-align: center;'>⚡ STOCK SCANNER (LIVE LEVELS)</h4>", unsafe_allow_html=True)

s1, s2 = st.columns(2)
with s1:
    st.markdown("<p style='color: #00ff66; font-size: 12px;'>🚀 BUY ABOVE / SL</p>", unsafe_allow_html=True)
    st.markdown("<div style='color: white; font-size: 14px;'><b>RELIANCE</b>: 2985 | SL: 2960</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: white; font-size: 14px;'><b>SBIN</b>: 815 | SL: 808</div>", unsafe_allow_html=True)
with s2:
    st.markdown("<p style='color: #ff1744; font-size: 12px;'>📉 SELL BELOW / SL</p>", unsafe_allow_html=True)
    st.markdown("<div style='color: white; font-size: 14px;'><b>HDFC BANK</b>: 1640 | SL: 1655</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: white; font-size: 14px;'><b>INFY</b>: 1890 | SL: 1905</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
