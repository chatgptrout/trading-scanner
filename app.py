import streamlit as st
import time
from datetime import datetime

# Page Config
st.set_page_config(page_title="SANTOSH TRADER PRO", layout="wide")

# Theme: Deep Dark & High Contrast 
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .commodity-card { background: linear-gradient(135deg, #1e1e2f 0%, #111119 100%); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; text-align: center; }
    .buy-signal { color: #00ff00; font-weight: bold; font-size: 18px; }
    .sell-signal { color: #ff3131; font-weight: bold; font-size: 18px; }
    .price-text { font-size: 24px; font-weight: bold; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
t1, t2 = st.columns([3, 1])
with t1:
    st.title("🛡️ SANTOSH TRADER PRO (v1.1)")
with t2:
    st.markdown(f"### ⏰ {datetime.now().strftime('%H:%M:%S')}")

# --- TABS: EQUITY & COMMODITY ---
tab1, tab2 = st.tabs(["📈 Equity & Index", "🔥 MCX Commodity"])

with tab1:
    st.subheader("Market Sentiment (NSE/BSE)")
    # (Puran wala Nifty/BankNifty logic yahan aayega)
    st.info("Nifty 50: 25,962.65 | Bank Nifty: 53,840.10")

with tab2:
    st.subheader("💰 MCX Live Watchlist")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""<div class='commodity-card'>
            <b style='color:#d4af37;'>CRUDE OIL</b><br>
            <span class='price-text'>₹6,480</span><br>
            <span class='buy-signal'>BULLISH</span>
        </div>""", unsafe_allow_html=True)
    
    with c2:
        st.markdown("""<div class='commodity-card'>
            <b style='color:#d4af37;'>NATURAL GAS</b><br>
            <span class='price-text'>₹158.40</span><br>
            <span class='sell-signal'>BEARISH</span>
        </div>""", unsafe_allow_html=True)
        
    with c3:
        st.markdown("""<div class='commodity-card'>
            <b style='color:#d4af37;'>GOLD (10g)</b><br>
            <span class='price-text'>₹72,450</span><br>
            <span class='buy-signal'>SIDEWAYS</span>
        </div>""", unsafe_allow_html=True)
        
    with c4:
        st.markdown("""<div class='commodity-card'>
            <b style='color:#d4af37;'>SILVER (1kg)</b><br>
            <span class='price-text'>₹88,200</span><br>
            <span class='buy-signal'>BULLISH</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🚀 MCX Breakout Radar")
    st.success("🔥 **CRUDE OIL:** Breakout above 6510 possible for Target 6600. SL 6450.")
    st.error("⚠️ **NATURAL GAS:** Trading near support 155. Breakdown below this can lead to 148.")

# --- FOOTER ---
if st.button("🔄 REFRESH ALL DATA"):
    st.rerun()