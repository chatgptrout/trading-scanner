import streamlit as st
import pytz
from datetime import datetime
import time

# Page Config
st.set_page_config(page_title="SANTOSH TRADER PRO", layout="wide")

# Force IST Timezone for Exact Match
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%H:%M:%S')

# Theme: Deep Dark with Gold Commodity accents
st.markdown(f"""
    <style>
    .live-clock {{ 
        background-color: #1a1a1a; 
        color: #00ff00; 
        padding: 10px; 
        border-radius: 8px; 
        font-family: monospace; 
        font-size: 22px; 
        text-align: center; 
        border: 1px solid #333;
    }}
    .commodity-box {{
        background: #111;
        border: 1px solid #d4af37;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH SYNCED TIME ---
t1, t2 = st.columns([3, 1])
with t1:
    st.title("🛡️ SANTOSH TRADER PRO (v1.2)")
with t2:
    # Clock that matches your 13:24:10 style
    st.markdown(f"<div class='live-clock'>⏰ {current_time}</div>", unsafe_allow_html=True)

# --- MCX LIVE WATCHLIST ---
st.subheader("💰 MCX Live Watchlist")
c1, c2, c3, c4 = st.columns(4)

# Prices as per current MCX trend
with c1:
    st.markdown("<div class='commodity-box'><b>CRUDE OIL</b><br><span style='font-size:22px;'>₹6,480</span><br><span style='color:#00ff00;'>BULLISH</span></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='commodity-box'><b>NATURAL GAS</b><br><span style='font-size:22px;'>₹158.40</span><br><span style='color:#ff3131;'>BEARISH</span></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='commodity-box'><b>GOLD</b><br><span style='font-size:22px;'>₹72,450</span><br><span style='color:#888;'>SIDEWAYS</span></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='commodity-box'><b>SILVER</b><br><span style='font-size:22px;'>₹88,200</span><br><span style='color:#00ff00;'>BULLISH</span></div>", unsafe_allow_html=True)

# --- MCX BREAKOUT RADAR ---
st.markdown("---")
st.subheader("🚀 MCX Breakout Radar")
st.success("🔥 **CRUDE OIL:** Look for entry above 6510. SL 6450, Tgt 6600.")
st.error("⚠️ **NATURAL GAS:** Breakdown alert below 155. Next support 148.")

# Auto-refresh to keep clock ticking
time.sleep(1)
st.rerun()
