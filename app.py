import streamlit as st
import yfinance as yf
import pandas as pd
import time

# PC के लिए चौड़ा लेआउट
st.set_page_config(page_title="SANTOSH TRADE GUIDE", layout="wide")

# Motilal Oswal डार्क प्रीमियम थीम
st.markdown("""<style>
    .stApp { background-color: #121212; color: #ffffff; }
    .main-header { background: #262626; padding: 10px; border-bottom: 2px solid #ffcc00; text-align: center; }
    .cat-header { background: #333333; padding: 5px 15px; color: #ffcc00; font-weight: bold; margin-top: 20px; border-radius: 5px; }
    .data-row { border-bottom: 1px solid #444; padding: 10px; font-family: monospace; }
    .green { color: #00ff88; }
    .red { color: #ff4b2b; }
</style>""", unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🚀 SANTOSH TRADE GUIDE SIGNALS</h1></div>", unsafe_allow_html=True)

# कैटेगरी और स्टॉक्स (1000104792.jpg के आधार पर)
categories = {
    "⏱️ TRADING FOR FEW MINUTES (SCALPING)": ["TATASTEEL.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"],
    "⏳ TRADING FOR FEW HOURS": ["MARUTI.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    "📅 TRADING FOR FEW DAYS": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"]
}

def fetch_trade_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        cmp = info['last_price']
        
        # लॉजिक: Entry CMP से थोड़ा नीचे, SL Entry से नीचे
        entry_price = cmp * 0.995  # FIXED: अब कोई अधूरा गुणा नहीं है
        stop_loss = entry_price * 0.99 
        sl_percent = 0.50
        
        return {"name": symbol.replace(".NS",""), "entry": entry_price, "sl": stop_loss, "slp": sl_percent, "cmp": cmp}
    except: return None

# टेबल हेडर
st.markdown("""
    <div style="display: flex; justify-content: space-between; padding: 10px; background: #262626; font-weight: bold; margin-top: 10px;">
        <span style="width: 25%;">STOCK</span>
        <span style="width: 15%;">ENTRY</span>
        <span style="width: 15%;">STOP LOSS</span>
        <span style="width: 15%;">SL %</span>
        <span style="width: 15%;">CMP</span>
    </div>
    """, unsafe_allow_html=True)

# डेटा दिखाना
for cat, stocks in categories.items():
    st.markdown(f"<div class='cat-header'>{cat}</div>", unsafe_allow_html=True)
    for s in stocks:
        d = fetch_trade_data(s)
        if d:
            color = "green" if d['cmp'] > d['entry'] else "red"
            st.markdown(f"""
                <div class="data-row">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="width: 25%; font-weight: bold;">{d['name']}</span>
                        <span style="width: 15%; color: #00ff88;">{d['entry']:.2f}</span>
                        <span style="width: 15%; color: #ff4b2b;">{d['sl']:.2f}</span>
                        <span style="width: 15%;">{d['slp']}%</span>
                        <span style="width: 15%;" class="{color}">{d['cmp']:.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

time.sleep(60)
st.rerun()
