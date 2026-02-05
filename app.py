import streamlit as st
import requests

st.set_page_config(page_title="Santosh Scanner", layout="wide")
st.title("SANTOSH SMART SCANNER")

token = st.sidebar.text_input("Dhan Token", type="password")

if token:
    try:
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        
        # MCX Crude Oil Feb Fut Security ID is 63
        payload = {
            "instruments": [
                {"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM", "security_id": "63"}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            prices = data.get('data', {})
            if prices:
                # Direct value extraction
                current_price = list(prices.values())[0]
                st.metric("CRUDE OIL FEB FUT", f"Rs {current_price}")
                st.success("LIVE DATA MATCHED")
            else:
                st.warning("Dhan server returned no price. Please check if 'Data APIs' is Green in Dhan Profile.")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Please paste 'OfficeScanner' token in the sidebar.")
