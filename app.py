import streamlit as st
import pandas as pd
import time

# --- WHITE THEME ---
st.set_page_config(page_title="TGS SNIPER", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .sniper-card { 
        background: #fdfdfd; border: 1px solid #eee; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .buy-card { border-left: 10px solid #28a745; background-color: #f0fff4; }
    .sell-card { border-left: 10px solid #dc3545; background-color: #fff5f5; }
    .wait-card { border-left: 10px solid #cccccc; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip() # Column names se space hatayega
        return df
    except:
        return pd.DataFrame()

st.markdown("<h2 style='text-align: center;'>🎯 TGS DASHBOARD LIVE</h2>", unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # Sirf top 10 stocks dikhayega taaki screen bhari rahe
    display_df = df.head(10)
    
    col1, col2 = st.columns(2)
    for i, (idx, row) in enumerate(display_df.iterrows()):
        t_col = col1 if i % 2 == 0 else col2
        
        # Signal Matching Logic
        sig = str(row['Signal Type']).strip().upper()
        
        if sig == "POSITIONAL":
            style = "buy-card"
            color = "#28a745"
        elif sig == "SHORTS":
            style = "sell-card"
            color = "#dc3545"
        else:
            style = "wait-card"
            color = "#888888"
            
        with t_col:
            st.markdown(f"""
                <div class="sniper-card {style}">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 20px; font-weight: bold;">{row['Symbol']}</span>
                        <span style="color: {color}; font-weight: bold;">{sig}</span>
                    </div>
                    <div style="margin-top: 10px; display: flex; justify-content: space-between; text-align: center;">
                        <div><small>LTP</small><br><b>{row['LTP']}</b></div>
                        <div><small>STOP LOSS</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b></div>
                        <div><small>TARGET</small><br><b style="color:#007bff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("Bhai, link toh sahi hai par data load nahi ho raha. Ek baar check karein ki sheet 'Public' hai ya nahi.")

time.sleep(10)
st.rerun()
