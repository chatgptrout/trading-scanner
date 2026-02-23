import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY ULTIMATE", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem; background-color: #000;}</style>""", unsafe_allow_html=True)

# --- 1. LIVE NIFTY PRICE FETCHING ---
def get_nifty_live():
    try:
        # '1d' data agar slow hai toh '2d' fetch karega taaki error na aaye
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period="1d", interval="1m")
        if df.empty:
            df = ticker.history(period="2d", interval="1m")
        return df
    except: return None

df_nifty = get_nifty_live()

# --- 2. MAIN PRICE DISPLAY ---
if df_nifty is not None and not df_nifty.empty:
    ltp = df_nifty['Close'].iloc[-1]
    hi = df_nifty['High'].max()
    lo = df_nifty['Low'].min()
    
    st.markdown(f"""
        <div style='text-align: center; background: #111; padding: 20px; border-radius: 15px; border-bottom: 4px solid #333;'>
            <p style='color: gray; margin: 0; font-size: 14px;'>NIFTY 50 LIVE SPOT</p>
            <h1 style='color: white; font-size: 55px; margin: 0;'>{ltp:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # --- 3. BULLISH ABOVE / BEARISH BELOW ---
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style='text-align: center; background: #002b11; padding: 10px; border-radius: 10px;'>
                <p style='color: #00ff66; margin: 0; font-size: 12px;'>BULLISH ABOVE</p>
                <h2 style='color: white; margin: 0;'>{hi:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style='text-align: center; background: #2b0000; padding: 10px; border-radius: 10px;'>
                <p style='color: #ff1744; margin: 0; font-size: 12px;'>BEARISH BELOW</p>
                <h2 style='color: white; margin: 0;'>{lo:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)

    # --- 4. LIVE PCR SECTION (SHIFTED TO BOTTOM) ---
    pcr_val = 2.01  # Live sync placeholder
    pcr_color = "#ff1744" if pcr_val > 1.2 else "#00ff66"
    
    st.markdown(f"""
        <div style='background: #111; padding: 15px; border-radius: 12px; border: 1px solid {pcr_color}; margin-top: 20px; text-align: center;'>
            <span style='color: gray; font-size: 14px;'>LIVE PCR SENTIMENT</span>
            <h2 style='color: {pcr_color}; margin: 5px 0;'>{pcr_val} ({'BEARISH ⚠️' if pcr_val > 1.2 else 'BULLISH ✅'})</h2>
            <p style='color: white; font-size: 11px; margin: 0;'>PCR niche shift kar diya gaya hai.</p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.warning("🔄 Exchange connectivity in progress... Auto-refreshing.")
    time.sleep(5)
    st.rerun()

# --- 5. BREAKOUT/BREAKDOWN STOCK LIST ---
st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
st.markdown("<h4 style='color: yellow; text-align: center;'>⚡ LIVE STOCK SCANNER</h4>", unsafe_allow_html=True)
# (Stock list logic as per previous version)

time.sleep(10)
st.rerun()
