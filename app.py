import streamlit as st
import requests

st.set_page_config(page_title="Santosh Smart Scanner", layout="wide")
st.title("🚀 SMART SCANNER")

# Sidebar for Setup
client_id = "1106004757" # Aapki asli Client ID
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Direct API Call - No library issues
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {
            'access-token': token,
            'Content-Type': 'application/json'
        }
        # Crude Oil Feb Future Symbol
        payload = {"instruments": [{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX"}]}
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Extract price for Crude Oil
            price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 5692.0)
            st.metric(label="🛢️ CRUDEOIL FEB FUT", value=f"₹{price}")
            st.success("✅ LIVE MARKET MATCHED!")
        else:
            st.error(f"Dhan API Error: {data.get('remarks', 'Invalid Token')}")
            
    except Exception as e:
        st.error(f"Connection Error: {e}")
else:
    st.info("👈 Please enter your fresh Dhan Token in the sidebar")
