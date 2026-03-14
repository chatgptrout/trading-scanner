import streamlit as st
import pandas as pd
from stoxkart_superr import SuperrApi
from datetime import datetime
import pytz

# Page Settings
st.set_page_config(page_title="Pro Stock Scanner", layout="wide")

# 🕒 Live Indian Clock
IST = pytz.timezone('Asia/Kolkata')
time_now = datetime.now(IST).strftime('%d-%m-%Y | %H:%M:%S')

st.title("🚀 Pro Breakout Scanner (Stoxkart Live)")
st.write(f"🕒 **Current Time (IST):** {time_now}")

# 🔑 Stoxkart API Credentials
# Note: Inhe hamesha secret rakhein
API_KEY = "6H4YuzLo1MqUgBoC"
API_SECRET = "VA6LpKmAM1Ejii8AFkR00m"
CLIENT_ID = "SQ38296"

def start_scanner():
    # Trading List
    stocks = ["NIFTY 50", "BANK NIFTY", "RELIANCE", "HDFCBANK", "CRUDEOIL", "NATURALGAS"]
    
    data_rows = []
    for s in stocks:
        # Dummy calculation (Real API se link hone par ye auto-update hoga)
        # Yahan humne OI (Open Interest) ka column bhi add kiya hai
        lp = 25181.80 if "NIFTY" in s else 2500.00
        
        data_rows.append({
            "Stock": s,
            "LTP": f"₹{lp}",
            "Buy Above": round(lp * 1.005, 2),
            "Target": round(lp * 1.015, 2),
            "Stop Loss": round(lp * 0.995, 2),
            "OI (Open Interest)": "1.4Cr" if "NIFTY" in s else "52L",
            "Signal": "⚖️ WATCHING"
        })

    # Display Table
    st.table(pd.DataFrame(data_rows))

# Run Scanner
start_scanner()

if st.button('🔄 Refresh & Sync API'):
    st.rerun()
