import streamlit as st
import pytz
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="SANTOSH SNIPER", layout="wide")

# --- Custom Professional Theme ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .signal-card { 
        background-color: #1a1c23; 
        border: 1px solid #333; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 15px;
        border-left: 8px solid #2ecc71; 
    }
    .sell-card { border-left: 8px solid #ff3131; }
    .stock-name { font-size: 22px; font-weight: bold; color: #ffffff; }
    .price-label { color: #888; font-size: 14px; }
    .price-value { font-size: 18px; font-weight: bold; color: #00ff00; }
    .sl-value { font-size: 18px; font-weight: bold; color: #ff3131; }
    .tgt-value { font-size: 18px; font-weight: bold; color: #3498db; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 LIVE STOCK BREAKOUT SNIPER")
st.write("---")

# --- DATA LIST (6-7 BREAKOUT STOCKS) ---
# Format: Stock, Signal, Price, SL, Target
breakouts = [
    {"stock": "BSE LTD", "signal": "BUY", "price": "3150.00", "sl": "3110.00", "tgt": "3220.00"},
    {"stock": "JINDAL STEL", "signal": "BUY", "price": "1182.00", "sl": "1168.00", "tgt": "1210.00"},
    {"stock": "M&M", "signal": "BUY", "price": "2845.00", "sl": "2815.00", "tgt": "2910.00"},
    {"stock": "ADANI ENT", "signal": "BUY", "price": "3140.00", "sl": "3105.00", "tgt": "3190.00"},
    {"stock": "TATA MOTORS", "signal": "SELL", "price": "922.00", "sl": "935.00", "tgt": "905.00"},
    {"stock": "RELIANCE", "signal": "BUY", "price": "2980.00", "sl": "2955.00", "tgt": "3030.00"},
    {"stock": "CRUDE OIL", "signal": "SELL", "price": "5850.00", "sl": "5910.00", "tgt": "5740.00"}
]

# --- GRID LAYOUT FOR SIGNALS ---
col1, col2 = st.columns(2)

for i, b in enumerate(breakouts):
    # Select Column
    target_col = col1 if i % 2 == 0 else col2
    
    # Check if Buy or Sell for Styling
    card_class = "signal-card" if b['signal'] == "BUY" else "signal-card sell-card"
    price_color = "#00ff00" if b['signal'] == "BUY" else "#ff3131"
    
    with target_col:
        st.markdown(f"""
            <div class="{card_class}">
                <div class="stock-name">{b['stock']} <span style="font-size:14px; color:{price_color}; float:right;">{b['signal']}</span></div>
                <hr style="border:0.5px solid #333;">
                <table style="width:100%;">
                    <tr>
                        <td><span class="price-label">ENTRY</span><br><span class="price-value" style="color:{price_color};">{b['price']}</span></td>
                        <td><span class="price-label">STOP LOSS</span><br><span class="sl-value">{b['sl']}</span></td>
                        <td><span class="price-label">TARGET</span><br><span class="tgt-value">{b['tgt']}</span></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
if st.button("🔄 REFRESH BREAKOUTS"):
    st.rerun()
