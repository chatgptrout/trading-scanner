import streamlit as st
import pytz
from datetime import datetime
import time

# Force IST for Live Commodity Trading
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%H:%M:%S')

st.set_page_config(page_title="SANTOSH TRADER PRO", layout="wide")

# Pro-Trader Theme (Gold & Dark)
st.markdown(f"""
    <style>
    .live-clock {{ background-color: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 24px; text-align: center; border: 2px solid #333; }}
    .mcx-card {{ background: #111; border: 2px solid #d4af37; padding: 20px; border-radius: 12px; text-align: center; }}
    .price-up {{ color: #00ff00; font-size: 28px; font-weight: bold; }}
    .price-down {{ color: #ff3131; font-size: 28px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
t1, t2 = st.columns([3, 1])
with t1:
    st.title("🔥 MCX LIVE TERMINAL (Santosh Pro)")
with t2:
    st.markdown(f"<div class='live-clock'>⏰ {current_time}</div>", unsafe_allow_html=True)

# --- LIVE COMMODITY WATCH ---
st.subheader("💰 Active Commodity Markets")
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""<div class='mcx-card'>
        <b style='color:#d4af37;'>CRUDE OIL (FEB)</b><br>
        <span class='price-down'>₹5,812.00</span><br>
        <small style='color:#ff3131;'>▼ -0.99%</small>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown("""<div class='mcx-card'>
        <b style='color:#d4af37;'>NATURAL GAS</b><br>
        <span class='price-down'>₹279.30</span><br>
        <small style='color:#ff3131;'>▼ -2.85%</small>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown("""<div class='mcx-card'>
        <b style='color:#d4af37;'>GOLD (APR)</b><br>
        <span class='price-up'>₹72,480.00</span><br>
        <small style='color:#00ff00;'>▲ +0.12%</small>
    </div>""", unsafe_allow_html=True)

# --- LIVE SCALPING RADAR ---
st.markdown("---")
st.subheader("🚀 Scalping Signals (5-Min Chart)")
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.error("📉 **CRUDE OIL:** Lower-Low pattern. 5800 is a crucial support. Agar break hua toh 5740 tak slip ho sakta hai.")
with col_s2:
    st.success("📈 **GOLD:** VIP Signal: 72400-72450 is a strong buying zone for 72600 target. SL 72350.")

time.sleep(1)
st.rerun()
