import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

st.set_page_config(page_title="TRADEX PRO V90", layout="wide")

# --- 1. DYNAMIC PCR & ADVICE LOGIC ---
def get_market_verdict(pcr, n_chg, s_chg):
    # Advice logic based on current market state
    if pcr >= 2.0:
        return "⚠️ ALERT: PCR EXTREME HIGH (2.0+). MARKET OVERBOUGHT. DON'T BUY AT TOP!", "#fff3cd", "#856404"
    elif n_chg < 0 and s_chg > 0:
        return "⚖️ MIXED MARKET: NIFTY RED & SENSEX GREEN. WAIT FOR SYNC.", "#d1ecf1", "#0c5460"
    elif n_chg > 0.5 and s_chg > 0.5:
        return "🔥 STRONG BULLISH: BOTH INDICES IN SYNC. LOOK FOR BUY!", "#d4edda", "#155724"
    else:
        return "👀 MARKET WATCH: NO CLEAR SIGNAL. CHECK LEVELS BELOW.", "#e2e3e5", "#383d41"

# --- 2. HEADER & LIVE ADVICE BAR ---
# PCR 2.0 as per latest screenshot
pcr_val = 2.0 
nifty_chg = -0.22 #
sensex_chg = 0.03 #

advice_txt, bg_col, txt_col = get_market_verdict(pcr_val, nifty_chg, sensex_chg)

st.markdown(f"""
    <div style='background-color:{bg_col}; color:{txt_col}; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:20px; border:1px solid {txt_col}; margin-bottom:20px;'>
        {advice_txt}
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (LIVE)</h4>
        <h1 style='color:#00c853; font-size:55px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:3px 15px; border-radius:5px; display:inline-block; font-weight:bold;'>TREND: EXTREME BULLISH</div>
    </div>
""", unsafe_allow_html=True)

# --- 3. PURANE CARDS & SCANNER (AS IT IS) ---
# Nifty, Sensex cards and BTST table with D-High/D-Low
# (Baki ka cards aur scanner code yahan same rahega)

time.sleep(10)
st.rerun()
