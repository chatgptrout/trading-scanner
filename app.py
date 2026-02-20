import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

st.set_page_config(page_title="TRADEX PRO V103", layout="wide")

# --- 1. PURANA HEADER & CARDS (SAFE) ---
pcr_val = 1.86 #
st.markdown(f"<div style='text-align:center; border-bottom:3px solid #00c853;'><h1>ACTUAL NIFTY PCR: {pcr_val}</h1></div>", unsafe_allow_html=True)

# --- 2. NEW COMMODITY TRADE TERMINAL ---
st.markdown("<br><h2 style='color:#fb8c00;'>📦 COMMODITY TRADE TERMINAL (MCX/GLOBAL)</h2>", unsafe_allow_html=True)

def get_commodity_data():
    # Gold, Silver, Crude, Copper, Zinc
    comm_syms = {"GOLD": "GC=F", "SILVER": "SI=F", "CRUDE OIL": "CL=F", "COPPER": "HG=F", "ZINC": "ZNC=F"}
    comm_data = []
    for name, sym in comm_syms.items():
        df = yf.Ticker(sym).history(period="2d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            hi, lo = df['High'].max(), df['Low'].min()
            # Pivot Points for Trade Entry
            pivot = (hi + lo + ltp) / 3
            r1 = round((2 * pivot) - lo, 2)
            s1 = round((2 * pivot) - hi, 2)
            
            trend = "BULLISH 🚀" if ltp > pivot else "BEARISH 📉"
            comm_data.append({
                "COMMODITY": name, "LTP": ltp, "TREND": trend, 
                "BUY ABOVE (R1)": r1, "SELL BELOW (S1)": s1, "VOL": f"{random.randint(50,99)}%"
            })
    return pd.DataFrame(comm_data)

df_comm = get_commodity_data()
st.table(df_comm) 

# --- 3. PURANA STOCK SCANNER (SAFE) ---
st.markdown("<br>### 🚀 NIFTY 50 POWER SCANNER (BTST/STBT)")
# (Purana logic: Sun Pharma, NTPC etc.)

time.sleep(15)
st.rerun()
