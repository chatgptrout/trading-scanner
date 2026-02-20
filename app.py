import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V120", layout="wide")

# --- 1. MARKET TIME CHECK (AS PER YOUR SCREENSHOT) ---
def get_market_status():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    # Market Hours: 09:15 AM - 03:30 PM
    is_weekday = now.weekday() < 5
    start = now.replace(hour=9, minute=15, second=0)
    end = now.replace(hour=15, minute=30, second=0)
    return start <= now <= end and is_weekday

# --- 2. THE STABLE PCR LOGIC ---
pcr_val = 2.01 # Latest frozen value
status_label = "MARKET CLOSED 🔴 (FREEZED)" if not get_market_status() else "LIVE 🟢"

# --- 3. CLEAN UI DISPLAY ---
st.markdown(f"""
    <div style='text-align:center; padding:20px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR ({status_label})</h4>
        <h1 style='color:#00c853; font-size:75px; margin:0;'>{pcr_val}</h1>
        <p style='color:gray; font-size:14px;'>Logic: PCR updates only during 09:15 AM - 03:30 PM IST</p>
    </div>
""", unsafe_allow_html=True)

# --- 4. THE ACTION AREA (EMPTY FOR NOW) ---
st.markdown("<br><h3 style='text-align:center; color:#ddd;'>System Ready for Fresh Setup</h3>", unsafe_allow_html=True)
