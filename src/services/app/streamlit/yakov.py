import time
import requests
import streamlit as st

# --- Config ---
API_KEY = "AIzaSyAIwC0O2xEpCFMv5eTc34LBfsjkP3BWFV8"
API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"   # GET ?q=...
MIN_CHARS = 2
DEBOUNCE_SEC = 0.3
MAX_SUGGESTIONS = 8

# --- Session state setup ---
st.session_state.setdefault("q", "")
st.session_state.setdefault("last_fetch_q", "")
st.session_state.setdefault("last_fetch_t", 0.0)
st.session_state.setdefault("suggestions", [])
st.session_state.setdefault("selected", None)

def fetch_suggestions(query: str):
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

def set_query(val: str):
    st.session_state.q = val
    st.session_state.selected = val
    # optionally clear suggestions after select
    st.session_state.suggestions = []

st.write("### Search")
st.text_input(" ",
              key="q",
              value=st.session_state.get("q",""),
              label_visibility="collapsed",
              placeholder="Search…")

q = st.session_state.q.strip()
st.session_state.q = q


# Debounced, incremental fetch as the user types
now = time.time()
if len(q) >= MIN_CHARS and q != st.session_state.last_fetch_q and (now - st.session_state.last_fetch_t) >= DEBOUNCE_SEC:
    st.session_state.suggestions = fetch_suggestions(q)
    st.session_state.last_fetch_q = q
    st.session_state.last_fetch_t = now

# "Dropdown" suggestions below the input
if st.session_state.suggestions and not st.session_state.selected:
    with st.container():
        st.markdown(
            """
            <style>
            .suggestion-box {border: 1px solid #ddd; border-radius: 8px; padding: 4px; margin-top: -8px;}
            .suggestion-btn {width: 100%; text-align: left;}
            </style>
            """,
            unsafe_allow_html=True,
        )
        with st.container():
            st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
            for s in st.session_state.suggestions:
                st.button(s, key=f"sugg_{s}", on_click=set_query, args=(s,), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# When user chooses a suggestion (or presses Enter on free text)
if st.session_state.selected or (q and st.session_state.selected is None):
    chosen = st.session_state.selected or q
    # Do whatever you need with the chosen value:
    st.write(f"*You searched for:* {chosen}")
    # Example: call your "search" endpoint only after selection/Enter:
    # results = requests.get("https://your.api/search", params={"q": chosen}).json()
    # st.write(results)