# pip install streamlit-keyup
# pip install streamlit-keyup

import requests
import streamlit as st
from st_keyup import st_keyup

# --- Config ---
API_KEY = "AIzaSyAIwC0O2xEpCFMv5eTc34LBfsjkP3BWFV8"
API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
MIN_CHARS = 2

# --- Session state ---
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "selected" not in st.session_state:
    st.session_state.selected = None


def fetch_suggestions(query: str):
    if not query or len(query.strip()) < MIN_CHARS:
        return []

    params = {
        "input": query.strip(),
        "types": "address",
        "components": "country:il",
        "language": "he",
        "key": API_KEY
    }

    try:
        response = requests.get(API_URL, params=params, timeout=3)
        data = response.json()
        if data.get("status") == "OK" and "predictions" in data:
            return [p["description"] for p in data["predictions"]]
        return []
    except:
        return []


def select_suggestion(suggestion):
    st.session_state.selected = suggestion
    st.session_state.suggestions = []


# --- UI ---
st.title("חיפוש כתובות")

# Input with real-time updates
query = st_keyup("חפש כתובת:", placeholder="הקלד כתובת...")

# Fetch suggestions on every keystroke
if query and len(query.strip()) >= MIN_CHARS:
    st.session_state.suggestions = fetch_suggestions(query)
elif not query:
    st.session_state.suggestions = []
    st.session_state.selected = None

# Show suggestions
if st.session_state.suggestions and not st.session_state.selected:
    st.write("**הצעות:**")
    for i, suggestion in enumerate(st.session_state.suggestions):
        if st.button(suggestion, key=f"btn_{i}"):
            select_suggestion(suggestion)
            st.rerun()

# Show selected result
if st.session_state.selected:
    st.success(f"נבחר: {st.session_state.selected}")
    if st.button("חיפוש חדש"):
        st.session_state.selected = None
        st.session_state.suggestions = []
        st.rerun()