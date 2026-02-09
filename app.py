import streamlit as st
import time

# 1. Professional Call Styling (Nagpal Style)
st.markdown("""
    <style>
    .pro-call-card {
        background-color: #ffffff; border-radius: 15px; padding: 25px;
        border-left: 10px solid #f39c12; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        font-family: 'Arial', sans-serif; margin-bottom: 20px;
    }
    .call-title { color: #f39c12; font-weight: bold; font-size: 20px; margin-bottom: 10px; }
    .strike-name { font-size: 22px; font-weight: bold; color: #333; }
    .price-details { font-size: 18px; margin: 10px 0; color: #444; }
    .sl-val { color: #e74c3c; font-weight: bold; }
    .tgt-val { color: #2ecc71; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for Exact Commodity Options
def get_nagpal_style_call():
    # Example based on your Crude Oil image
    return {
        "symbol": "CRUDEOILM 17FEB 5700 CE",
        "type": "Intraday-Buy",
        "entry": "190 - 192",
        "target": "233 (22.63%)",
        "sl": "163 (-14.21%)"
    }

# --- DISPLAY ---
call = get_nagpal_style_call()

st.markdown(f"""
    <div class='pro-call-card'>
        <div class='call-title'>⭐ Commodity Recommendation ⭐</div>
        <div class='strike-name'>📈 {call['symbol']}</div>
        <div class='price-details'>
            <b>Type:</b> {call['type']}<br>
            💰 <b>Entry Price:</b> ₹ {call['entry']}<br>
            🎯 <b>Target:</b> <span class='tgt-val'>₹ {call['target']}</span><br>
            ⚠️ <b>Stop Loss:</b> <span class='sl-val'>₹ {call['sl']}</span>
        </div>
        <hr>
        <small style='color:#888;'>Disclaimer: Trade and invest after reading rules.</small>
    </div>
    """, unsafe_allow_html=True)

# Purana Index Mover Niche Safe Rahega
st.markdown("---")
st.write("📊 **Market Mood Check:**")
# Yahan aapka purana pie chart code rahega.
