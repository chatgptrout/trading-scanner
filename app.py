import streamlit as st
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY TERMINAL PRO", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem; background-color: #000;} hr {border-color: #333;}</style>""", unsafe_allow_html=True)

# --- 1. PCR & NIFTY MAIN PANEL ---
pcr_val = 2.01 
pcr_color = "#ff1744" if pcr_val > 1.2 else "#00ff66"

st.markdown(f"""
    <div style='text-align: center; background: #111; padding: 15px; border-radius: 15px; border: 2px solid {pcr_color};'>
        <h3 style='color: {pcr_color}; margin: 0; font-size: 22px;'>LIVE PCR: {pcr_val}</h3>
        <p style='color: white; font-size: 12px;'>{'⚠️ OVERBOUGHT - SELL ON RISE' if pcr_val > 1.2 else '✅ BULLISH - BUY ON DIP'}</p>
        <h1 style='color: white; font-size: 55px; margin: 5px 0;'>25,565.90</h1>
        <div style='display: flex; justify-content: space-around;'>
            <div style='color: #00ff66; font-size: 14px;'><b>BULLISH ABOVE: 25,610</b></div>
            <div style='color: #ff1744; font-size: 14px;'><b>BEARISH BELOW: 25,480</b></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. BREAKOUT & BREAKDOWN LIST WITH LEVELS ---
st.markdown("<h3 style='color: yellow; text-align: center; margin-top: 15px;'>⚡ LIVE BREAKOUT SCANNER</h3>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown("<p style='color: #00ff66; font-weight: bold; border-bottom: 2px solid #00ff66;'>🚀 BREAKOUT (BUY)</p>", unsafe_allow_html=True)
    # Stock: Reliance
    st.markdown("""
        <div style='background: #002b11; padding: 8px; border-radius: 5px; margin-bottom: 10px;'>
            <b style='color: white;'>RELIANCE</b><br>
            <span style='color: #00ff66; font-size: 12px;'>Buy Above: 2985</span><br>
            <span style='color: #ff9800; font-size: 12px;'>SL: 2960</span>
        </div>
    """, unsafe_allow_html=True)
    # Stock: SBIN
    st.markdown("""
        <div style='background: #002b11; padding: 8px; border-radius: 5px; margin-bottom: 10px;'>
            <b style='color: white;'>SBIN</b><br>
            <span style='color: #00ff66; font-size: 12px;'>Buy Above: 815</span><br>
            <span style='color: #ff9800; font-size: 12px;'>SL: 808</span>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("<p style='color: #ff1744; font-weight: bold; border-bottom: 2px solid #ff1744;'>📉 BREAKDOWN (SELL)</p>", unsafe_allow_html=True)
    # Stock: HDFCBANK
    st.markdown("""
        <div style='background: #2b0000; padding: 8px; border-radius: 5px; margin-bottom: 10px;'>
            <b style='color: white;'>HDFCBANK</b><br>
            <span style='color: #ff1744; font-size: 12px;'>Sell Below: 1640</span><br>
            <span style='color: #ff9800; font-size: 12px;'>SL: 1655</span>
        </div>
    """, unsafe_allow_html=True)
    # Stock: INFY
    st.markdown("""
        <div style='background: #2b0000; padding: 8px; border-radius: 5px; margin-bottom: 10px;'>
            <b style='color: white;'>INFY</b><br>
            <span style='color: #ff1744; font-size: 12px;'>Sell Below: 1890</span><br>
            <span style='color: #ff9800; font-size: 12px;'>SL: 1910</span>
        </div>
    """, unsafe_allow_html=True)

# --- 3. BTST / STBT PANEL ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: cyan; text-align: center;'>🌙 POSITIONAL (BTST/STBT)</h3>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    st.markdown("""
        <div style='background: #111; border: 1px solid #00ff66; padding: 10px; border-radius: 10px; text-align: center;'>
            <b style='color: #00ff66;'>BTST (BUY)</b><br>
            <span style='color: white; font-size: 18px;'>TATA MOTORS</span><br>
            <span style='color: gray; font-size: 11px;'>Tgt: +15pts | SL: 8pts</span>
        </div>
    """, unsafe_allow_html=True)

with b2:
    st.markdown("""
        <div style='background: #111; border: 1px solid #ff1744; padding: 10px; border-radius: 10px; text-align: center;'>
            <b style='color: #ff1744;'>STBT (SELL)</b><br>
            <span style='color: white; font-size: 18px;'>COAL INDIA</span><br>
            <span style='color: gray; font-size: 11px;'>Tgt: -10pts | SL: 5pts</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: gray; font-size: 10px; margin-top: 15px;'>Updated: {datetime.now().strftime('%I:%M:%S %p')}</p>", unsafe_allow_html=True)
time.sleep(15)
st.rerun()
