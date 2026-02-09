import streamlit as st
import yfinance as yf
import time

# Custom Styling for Live Price Display
st.markdown("""
    <style>
    .live-price-box {
        background: #333; color: #00ff00; padding: 5px 15px;
        border-radius: 20px; font-weight: bold; font-size: 18px;
        display: inline-block; margin-bottom: 10px; border: 1px solid #00ff00;
    }
    .nagpal-card {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 25px;
        border-left: 12px solid #2ecc71;
    }
    </style>
    """, unsafe_allow_html=True)

def get_live_ticker_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="1m")
        return round(data['Close'].iloc[-1], 2)
    except: return "Loading..."

# --- CALL CARD FUNCTION WITH LIVE PRICE ---
def display_call_card(title, symbol, ticker, entry, sl, tgt, color):
    current_p = get_live_ticker_price(ticker)
    st.markdown(f"""
        <div class='nagpal-card' style='border-left-color: {color};'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='color:{color}; font-weight:bold;'>⭐ {title}</span>
                <div class='live-price-box'>LIVE: ₹{current_p}</div>
            </div>
            <div style='font-size:24px; font-weight:bold;'>🚀 BUY {symbol}</div>
            <div style='background:#f9f9f9; padding:10px; margin:10px 0; border:1px dashed #ccc;'>
                <b>ENTRY:</b> ABOVE ₹{entry}
            </div>
            <div style='font-size:18px;'>
                <span style='color:#e74c3c; font-weight:bold;'>🛑 SL: {sl}</span> | 
                <span style='color:#2ecc71; font-weight:bold;'>🎯 TGT: {tgt}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN DISPLAY ---
st.subheader("📢 Live Signals with Real-Time Prices")

# 1. Stock Call (Nagpal Style)
display_call_card("Stock Cash", "POWERINDIA", "POWERINDIA.NS", "22780", "22350", "23200", "#2ecc71")

# 2. Option Call
display_call_card("Option Premium", "NIFTY 22500 CE", "^NSEI", "148", "115", "220", "#1c92d2")

# 3. Commodity Call
display_call_card("Commodity Special", "CRUDEOILM 17FEB 5700 CE", "CL=F", "195-200", "163", "240", "#f39c12")

time.sleep(10)
st.rerun()
