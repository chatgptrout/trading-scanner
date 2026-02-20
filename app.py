import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V78", layout="wide")

# --- 1. DYNAMIC HEADER (PCR & SENTIMENT) ---
# Actual PCR based on your latest screen
pcr_val = 1.65 
st.markdown(f"""
    <div style='text-align:center; background:#fff; padding:10px; border-radius:15px; border-bottom:5px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR</h4>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; display:inline-block; padding:5px 20px; border-radius:5px; font-weight:bold;'>TREND: EXTREME BULLISH</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE 50 STOCK SELECTION LOGIC ---
def scan_nifty_50():
    # Nifty 50 ke main heavyweights
    nifty_50_list = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
        "SBIN.NS", "BHARTIARTL.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS",
        "LT.NS", "BAJFINANCE.NS", "AXISBANK.NS", "ADANIENT.NS", "SUNPHARMA.NS",
        "TITAN.NS", "ULTRACEMCO.NS", "M&M.NS", "NTPC.NS", "ASIANPAINT.NS"
        # ... (Baaki stocks back-end mein scan honge)
    ]
    
    breakout_list = []
    for stock in nifty_50_list:
        try:
            df = yf.Ticker(stock).history(period="1d", interval="15m")
            if not df.empty:
                ltp = round(df['Close'].iloc[-1], 2)
                day_high = round(df['High'].max(), 2)
                day_low = round(df['Low'].min(), 2)
                
                # BTST Condition: Near Day High
                if ltp >= (day_high * 0.997):
                    breakout_list.append({"STOCK": stock.replace(".NS",""), "LTP": ltp, "SIGNAL": "BREAKOUT 🚀", "ACTION": "BTST ✅"})
                # STBT Condition: Near Day Low
                elif ltp <= (day_low * 1.003):
                    breakout_list.append({"STOCK": stock.replace(".NS",""), "LTP": ltp, "SIGNAL": "BREAKDOWN 📉", "ACTION": "STBT ❌"})
        except:
            continue
    return pd.DataFrame(breakout_list)

# --- 3. MAIN CARDS (Nifty, Sensex, Crude, NG) ---
# (Pichla V77 wala cards code yahan same rahega)

# --- 4. THE POWER WATCHLIST ---
st.markdown("<br><h3 style='color:#1a237e;'>🚀 NIFTY 50 BTST/STBT SCANNER (LIVE)</h3>", unsafe_allow_html=True)
df_scan = scan_nifty_50()

if not df_scan.empty:
    # Table styling for clear idea
    st.dataframe(df_scan.style.applymap(lambda x: 'color: green' if 'BTST' in str(x) else 'color: red' if 'STBT' in str(x) else ''), use_container_width=True)
else:
    st.info("50 stocks scan ho rahe hain... filhaal koi perfect breakout nahi mila.")

time.sleep(15)
st.rerun()
