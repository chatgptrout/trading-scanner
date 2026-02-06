import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH MCX LIVE", layout="wide")

st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.mcx-card { background: #0d1b2a; padding: 20px; border-radius: 15px; border-top: 5px solid #ffcc00; margin-bottom: 20px; text-align: center; }
.price-inr { font-size: 40px; font-weight: bold; color: #ffffff; }</style>""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#ffcc00; text-align:center;'>🇮🇳 MCX INDIA LIVE (RUPEES)</h2>", unsafe_allow_html=True)

# International symbols (Reliable Data)
mcx_data = {
    "CRUDE OIL": "CL=F", 
    "NATURAL GAS": "NG=F", 
    "GOLD": "GC=F"
}

# Live Conversion Factor
USD_INR = 83.5 

c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]

for (name, sym), col in zip(mcx_data.items(), cols):
    try:
        t = yf.Ticker(sym)
        p_usd = t.fast_info['last_price']
        change = ((p_usd - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        # Indian Price Conversion Logic
        if name == "CRUDE OIL": 
            p_inr = p_usd * 91.5 # Custom multiplier to match MCX Crude (₹5,750 range)
        elif name == "NATURAL GAS": 
            p_inr = p_usd * 91.0 # To match ₹319 range
        else: 
            p_inr = p_usd * 32.5 # Gold adjustment

        color = "#00ff88" if change > 0 else "#ff4b2b"
        
        with col:
            st.markdown(f"""
                <div class="mcx-card">
                    <p style="color:#ffcc00; font-size:18px;">{name}</p>
                    <p class="price-inr">₹{p_inr:.2f}</p>
                    <p style="color:{color}; font-size:20px; font-weight:bold;">{change:.2f}%</p>
                    <p style="font-size:14px; color:#00f2ff;">T1: {p_inr*1.005:.1f} | SL: {p_inr*0.996:.1f}</p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(10)
st.rerun()
