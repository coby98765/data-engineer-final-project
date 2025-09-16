import streamlit as st
import requests
import streamlit.components.v1 as components
# from streamlit_autocomplete import st_autocomplete

# שים כאן את ה-API KEY שלך מגוגל
API_KEY = "AIzaSyAIwC0O2xEpCFMv5eTc34LBfsjkP3BWFV8"
API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"

def get_address_suggestions(query: str):
    if not query:
        return []
    params = {
        "input": query,
        "types": "address",
        "components": "country:il",  # רק ישראל
        "language": "he",
        "key": API_KEY
    }
    r = requests.get(API_URL, params=params)
    data = r.json()
    if "predictions" in data:
        return [p["description"] for p in data["predictions"]]
    return []

st.title("🔎 חיפוש כתובות")

# שדה חיפוש
search_text = st.text_input("הקלד כתובת:")

# ברגע שמקלידים – נטען הצעות
options = get_address_suggestions(search_text)

# דרופדאון שמחובר ישירות לאותו טקסט
if options:
    selected = st.selectbox(
        "בחר כתובת:",
        options,
        key="selected_address"
    )
    st.success(f"✔ בחרת: {selected}")