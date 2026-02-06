import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH MCX RUPEE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .mcx-card {
        background: #0d1b2a; padding: 20px; border-radius: 15px;
        border-top: 5px solid #ffcc00; margin-bottom: 20px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .price-big { font-size: 42px; font-weight: bold; color: #ffffff; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='color:#ffcc00;'>🇮🇳 MCX INDIA LIVE (RUPEES)</h2>", unsafe_allow_html=True)

# Indian MCX Symbols (Yahoo Finance format for Indian Commodities)
# Note: Inme thoda delay ho sakta hai, par rate RUPEES mein aayega
mcx_rupee_assets = {
    "CRUDE OIL": "MCRUDEOIL25FEB.NS", 
    "NATURAL GAS": "NATGAS25FEB.NS", 
    "GOLD MINI": "GOLDM25MAR.NS"
}

c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]

for (name, sym), col in zip(mcx_rupee_assets.items(), cols):
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        prev = t.fast_info['previous_close']
        change = ((p - prev) / prev) * 100
        color = "#00ff88" if change > 0 else "#ff4b2b"
        
        with col:
            st.markdown(f"""
                <div class="mcx-card">
                    <p style="color:#ffcc00; font-size:18px; margin:0;">{name}</p>
                    <p class="price-big">₹{p:.2f}</p>
                    <p style="color:{color}; font-size:22px; font-weight:bold;">{change:.2f}%</p>
                    <p style="font-size:14px; color:#a0a0a0;">Current Market Price in INR</p>
                </div>
            """, unsafe_allow_html=True)
    except:
        # Fallback agar Indian symbol load na ho
        with col: st.write(f"Connecting to MCX for {name}...")

time.sleep(15)
st.rerun()
