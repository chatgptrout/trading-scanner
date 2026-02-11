import streamlit as st
import time
import random

# --- APP CONFIG ---
st.set_page_config(page_title="SANTOSH AUTO-SNIPER", layout="wide")

# Sniper Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .sniper-card { 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        padding: 20px; 
        margin-bottom: 15px;
    }
    .buy-label { color: #2ecc71; font-weight: bold; font-size: 18px; }
    .sell-label { color: #ff3131; font-weight: bold; font-size: 18px; }
    .price-box { background: #0d1117; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 SANTOSH AUTOMATIC BREAKOUT TERMINAL")
st.write("Live Market Engine: **Connected** ✅")

# --- AUTOMATIC SIGNAL ENGINE ---
def get_auto_signals():
    # Ye stocks hamare radar mein rahenge
    stock_list = ["BSE LTD", "JINDAL STEL", "M&M", "ADANI ENT", "TATA MOTORS", "RELIANCE", "CRUDE OIL"]
    signals = []
    
    for s in stock_list:
        # Pseudo-Live Logic (Isse actual live data se connect karenge)
        ltp = round(random.uniform(1000, 6000), 2)
        signals.append({
            "stock": s,
            "type": "BUY" if ltp % 2 == 0 else "SELL",
            "ltp": ltp,
            "entry": round(ltp * 0.99, 2),
            "sl": round(ltp * 0.98, 2),
            "tgt": round(ltp * 1.05, 2)
        })
    return signals

# --- DISPLAY ---
auto_data = get_auto_signals()
c1, c2 = st.columns(2)

for i, data in enumerate(auto_data):
    target_col = c1 if i % 2 == 0 else c2
    label_class = "buy-label" if data['type'] == "BUY" else "sell-label"
    
    with target_col:
        st.markdown(f"""
            <div class="sniper-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 22px; font-weight: bold;">{data['stock']}</span>
                    <span class="{label_class}">{data['type']}</span>
                </div>
                <hr style="border: 0.1px solid #333;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                    <div class="price-box"><small style="color:#888;">ENTRY</small><br><b>{data['entry']}</b></div>
                    <div class="price-box"><small style="color:#888;">STOPLOSS</small><br><b style="color:#ff3131;">{data['sl']}</b></div>
                    <div class="price-box"><small style="color:#888;">TARGET</small><br><b style="color:#58a6ff;">{data['tgt']}</b></div>
                </div>
                <div style="margin-top:15px; text-align:right;">
                    <small style="color:#2ecc71;">Live LTP: {data['ltp']}</small>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Auto-Refresh to simulate live market
time.sleep(2)
st.rerun()
