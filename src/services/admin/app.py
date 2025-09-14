import os, requests, streamlit as st

SERVICES = {
    "scraper": os.getenv("SCRAPER_URL","http://scraper:8000"),
    "parser":  os.getenv("PARSER_URL","http://parser:8000"),
    "expander":os.getenv("EXPANDER_URL","http://expander:8000"),
    "geocoder":os.getenv("GEOCODER_URL","http://geocoder:8000"),
    "indexer": os.getenv("INDEXER_URL","http://indexer:8000"),
}

st.set_page_config(page_title="Admin", layout="wide")
st.title("Pipeline Admin")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Start Jobs")
    for name, base in SERVICES.items():
        if st.button(f"Run {name}"):
            try:
                r = requests.post(f"{base}/start", json={"params": {}}, timeout=10)
                st.write(name, r.json())
            except Exception as e:
                st.error(f"{name} start failed: {e}")

with col2:
    st.subheader("Status")
    for name, base in SERVICES.items():
        try:
            r = requests.get(f"{base}/status", timeout=5)
            st.write(name, r.json())
        except Exception as e:
            st.error(f"{name} status failed: {e}")
