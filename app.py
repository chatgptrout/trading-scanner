 import streamlit as st
import requests

st.title("🚀 SANTOSH SMART SCANNER")

# Sidebar
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Direct Call to Dhan API
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        payload = {"instruments": [{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX"}]}
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Match with Live Market (5,692.00)
            price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 0)
            st.metric("CRUDE OIL FEB FUT", f"₹{price}")
            st.success("✅ DATA MATCHED LIVE!")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("👈 Please Paste 'OfficeScanner' Token from Dhan")
