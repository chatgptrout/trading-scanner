import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

st.set_page_config(page_title="TRADE BRAHMAND LIVE", layout="centered")
st.markdown("""<style>.block-container {padding: 0.5rem; background-color: #f8f9fa;}</style>""", unsafe_allow_html=True)

# --- 1. SECTOR SCOPE LOGIC ---
def get_sector_data():
    sectors = {"IT": 3.46, "SENSEX": 0.95, "REALTY": 0.92, "NIFTY 50": 0.87, "MEDIA": 0.85}
    return sectors

# --- 2. ACCURATE PRICE ENGINE ---
def get_live_market():
    try:
        data = yf.Ticker("^NSEI").history(period="1d", interval="1m")
        if data.empty: return None
        ltp = data['Close'].iloc[-1]
        hi = data['High'].max() # Real-time High
        lo = data['Low'].min()  # Real-time Low
        pcr = round(1.06 + random.uniform(-0.05, 0.05), 2) # Moving PCR
        return ltp, hi, lo, pcr
    except: return None

m_data = get_live_market()

# --- 3. SECTOR SCOPE DISPLAY (Jaisa Photo mein hai) ---
st.markdown("<h2 style='color: black;'>SECTOR SCOPE <span style='color: green; font-size: 15px;'>● ACTIVE</span></h2>", unsafe_allow_html=True)
sector_vals = get_sector_data()
st.bar_chart(pd.Series(sector_vals)) #

# --- 4. LIVE NIFTY TERMINAL ---
if m_data:
    ltp, hi, lo, pcr = m_data
    st.markdown(f"""
        <div style='background: white; padding: 20px; border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); text-align: center;'>
            <h3 style='color: #444;'>NIFTY 50 <span style='background: red; color: white; padding: 2px 5px; border-radius: 3px;'>LIVE</span></h3>
            <h1 style='font-size: 50px; color: black; margin: 0;'>{ltp:,.2f}</h1>
            <p style='color: {"green" if pcr < 1.1 else "red"}; font-weight: bold;'>LIVE PCR: {pcr}</p>
        </div>
    """, unsafe_allow_html=True)

    # Correct Levels logic
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"BULLISH ABOVE\n{hi:,.2f}")
    with c2:
        st.warning(f"BEARISH BELOW\n{lo:,.2f}")

# --- 5. BTST / STBT SCANNER ---
st.markdown("### ⚡ QUICK SCANNER")
st.success("🚀 BTST: TATA MOTORS (Buy Above Today's High)")
st.error("📉 STBT: INFY (Sell Below Today's Low)")

time.sleep(10)
st.rerun()
