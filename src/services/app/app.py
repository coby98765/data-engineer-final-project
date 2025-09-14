import os, requests, streamlit as st

API = os.getenv("API_BASE_URL","http://api:8000")
st.set_page_config(page_title="RavKav Geo", layout="wide")

st.title("RavKav Geo — חיפוש זכאות")
locality = st.text_input("יישוב")
street = st.text_input("רחוב")
house = st.number_input("מספר בית", min_value=0, step=1)

if st.button("חפש"):
    params = {"locality": locality, "street": street}
    if house:
        params["house"] = int(house)
    r = requests.get(f"{API}/search", params=params, timeout=20)
    if r.ok:
        data = r.json()
        st.json(data)
    else:
        st.error(f"API error: {r.status_code}")
