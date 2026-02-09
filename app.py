import streamlit as st
import yfinance as yf
import time

# 1. Option-Focused UI Styling
st.markdown("""
    <style>
    .option-call-box {
        background-color: #f0f8ff; border-radius: 20px; padding: 25px;
        border: 2px solid #1c92d2; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-stock { color: #2ecc71; font-size: 28px; font-weight: bold; }
    .premium-price { color: #333; font-size: 22px; font-weight: bold; background: #fff; padding: 10px; border-radius: 10px; display: inline-block; margin: 10px 0; border: 1px dashed #1c92d2; }
    .sl-text { color: #e74c3c; font-weight: bold; font-size: 18px; }
    .tgt-text { color: #2ecc71; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic to separate Stock Price from Option Price
def get_real_option_call():
    stock_name = "POWERINDIA"
    # Option Premium logic (₹5 to ₹500 range)
    option_premium_cmp = 760.0 #
    
    # Entry/Exit based on chhota premium price
    entry_above = round(option_premium_cmp * 1.02, 1) # Entry above premium level
    sl = 600.0 #
    tgt_1 = 850.0
    tgt_2 = 1000.0
    
    return {
        "stock": stock_name,
        "option": "22500 CE",
        "entry": entry_above,
        "sl": sl,
        "tg": f"{tgt_1} - {tgt_2}"
    }

# --- DISPLAY ---
call = get_real_option_call()

st.markdown(f"""
    <div class='option-call-box'>
        <div class='main-stock'>🚀 BUY {call['stock']} {call['option']}</div>
        <div class='premium-price'>OPTION ENTRY: ABOVE ₹{call['entry']}</div>
        <div style='margin-top:15px;'>
            <span class='sl-text'>🛑 STOP LOSS: ₹{call['sl']}</span><br>
            <span class='tgt-text'>🎯 TARGET: ₹{call['tg']}</span>
        </div>
        <hr>
        <small style='color:#888;'>Mausam Nagpal Strategy | Option Premium Focused ✔️</small>
    </div>
    """, unsafe_allow_html=True)

time.sleep(60)
st.rerun()
