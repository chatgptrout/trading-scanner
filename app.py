import streamlit as st
import pandas as pd
import time

# --- WHITE THEME (SANTOSH SPECIAL) ---
st.set_page_config(page_title="TGS SNIPER PRO", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .sniper-card { 
        background: #ffffff; border: 1px solid #e1e4e8; border-radius: 12px; 
        padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 8px solid #28a745;
    }
    .sell-card { border-left-color: #dc3545; }
    .wait-card { border-left-color: #ced4da; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

# Correct CSV Link from your screenshot
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip() # Remove spaces from headers
        return df
    except:
        return pd.DataFrame()

st.title("🎯 TGS DASHBOARD - LIVE TRAIL")

df = load_data()

if not df.empty:
    # Match symbols from your sheet: TCS, SBIN, INFY...
    col1, col2 = st.columns(2)
    
    # Hum pehle 15 stocks dikhayenge taaki screen khali na rahe
    for i, (idx, row) in enumerate(df.head(15).iterrows()):
        t_col = col1 if i % 2 == 0 else col2
        
        # Signal Type Logic
        sig = str(row['Signal Type']).strip().upper()
        
        if "POSITIONAL" in sig:
            card_class = ""
            label = "BUY"
            color = "#28a745"
        elif "SHORTS" in sig:
            card_class = "sell-card"
            label = "SELL"
            color = "#dc3545"
        else:
            card_class = "wait-card"
            label = "WAIT"
            color = "#6c757d"
            
        with t_col:
            st.markdown(f"""
                <div class="sniper-card {card_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 20px; font-weight: bold;">{row['Symbol']}</span>
                        <span style="color: {color}; font-weight: bold;">{label}</span>
                    </div>
                    <div style="margin-top: 10px; display: flex; justify-content: space-between; text-align: center;">
                        <div><small style="color:#888;">LTP</small><br><b>{row['LTP']}</b></div>
                        <div><small style="color:#888;">STOP LOSS</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b></div>
                        <div><small style="color:#888;">TARGET</small><br><b style="color:#007bff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Error message as seen in your screenshot
    st.warning("⚠️ Bhai, Data load nahi ho raha. Check karein ki Google Sheet 'Publish to web' hai.")

time.sleep(10)
st.rerun()
