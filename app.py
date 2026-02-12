import streamlit as st
import pandas as pd
import time

# --- CLEAN WHITE UI ---
st.set_page_config(page_title="SANTOSH SNIPER PRO", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .sniper-card { 
        background: #ffffff; border: 1px solid #e1e4e8; border-radius: 15px; 
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #28a745;
    }
    .sell-top { border-top-color: #dc3545; }
    .wait-top { border-top-color: #adb5bd; opacity: 0.7; }
    </style>
    """, unsafe_allow_html=True)

# Aapka correct CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_live_data():
    try:
        # Direct fresh fetch from TGS Sheet
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip() # Spaces saaf karega
        return df
    except:
        return pd.DataFrame()

st.markdown("<h2 style='text-align: center;'>🎯 TGS DASHBOARD - LIVE TRAIL</h2>", unsafe_allow_html=True)

data = load_live_data()

if not data.empty:
    # Saare stocks dikhayega taaki aapko "Empty" screen na dikhe
    col1, col2 = st.columns(2)
    for i, (idx, row) in enumerate(data.head(12).iterrows()):
        t_col = col1 if i % 2 == 0 else col2
        
        # Signal Matching Logic
        sig = str(row['Signal Type']).strip().upper()
        card_style = ""
        sig_color = "#6c757d"
        
        if "POSITIONAL" in sig:
            card_style = ""
            sig_color = "#28a745"
        elif "SHORTS" in sig:
            card_style = "sell-top"
            sig_color = "#dc3545"
        else:
            card_style = "wait-top"
            sig_color = "#6c757d"
            
        with t_col:
            st.markdown(f"""
                <div class="sniper-card {card_style}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: bold; color: #1a1a1a;">{row['Symbol']}</span>
                        <span style="color: {sig_color}; font-weight: bold; font-size: 16px;">{sig}</span>
                    </div>
                    <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                        <div><small style="color:#888;">LTP</small><br><b style="font-size: 18px;">{row['LTP']}</b></div>
                        <div><small style="color:#888;">STOP LOSS</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b></div>
                        <div><small style="color:#888;">TARGET</small><br><b style="color:#007bff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Agar abhi bhi load nahi hua toh ye message dikhayega
    st.warning("⚠️ Bhai, Sheet abhi connect ho rahi hai. 1 minute rukiye ya browser refresh kijiye.")
    st.info("Tip: Google Sheet mein 'File > Share > Publish to web' check karein ki wo active hai.")

time.sleep(10)
st.rerun()
