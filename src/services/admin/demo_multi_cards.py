# demo_multi_cards.py
import time
import streamlit as st

st.set_page_config(page_title="Services – 5 Cards", layout="wide")

SERVICES = ["scraper", "parser", "geocoder", "expander", "api"]

COLOR = {
    "idle": "#1e88e5",
    "checking": "#00acc1",
    "healthy": "#43a047",
    "setting_up": "#fdd835",
    "running": "#2e7d32",
    "error": "#e53935",
}
LABEL = {
    "idle": "start",
    "checking": "checking health...",
    "healthy": "healthy",
    "setting_up": "setting up",
    "running": "running",
    "error": "error",
}

# ---- state per service ----
def init_state(name: str):
    st.session_state.setdefault(f"state_{name}", "idle")
    st.session_state.setdefault(f"busy_{name}", False)

def set_state(name: str, s: str):
    st.session_state[f"state_{name}"] = s

def get_state(name: str) -> str:
    return st.session_state[f"state_{name}"]

def set_busy(name: str, val: bool):
    st.session_state[f"busy_{name}"] = val

def is_busy(name: str) -> bool:
    return st.session_state[f"busy_{name}"]

def show_status(ph, state: str):
    ph.markdown(
        f"""
        <div style="
            background:{COLOR[state]};
            color:#000;
            padding:12px;
            border-radius:10px;
            text-align:center;
            font-weight:600;">
            {LABEL[state]}
        </div>
        """,
        unsafe_allow_html=True
    )

def run_flow(name: str, ph):
    set_busy(name, True)
    for step in ["checking", "healthy", "setting_up", "running"]:
        set_state(name, step)
        show_status(ph, step)   # מעדכן את אותו מלבן סטטוס
        time.sleep(0.8)
    set_busy(name, False)

st.title("Services – 5 cards (native border)")

cols = st.columns(5, gap="large")

for i, name in enumerate(SERVICES):
    init_state(name)
    with cols[i]:
        with st.container(border=True):
            # כותרת הכרטיס
            st.markdown(f"<h4 style='text-align:center;margin:0 0 12px 0;'>{name}</h4>",
                        unsafe_allow_html=True)

            # כפתור Start באמצע
            left, mid, right = st.columns([1,2,1])
            with mid:
                disabled = is_busy(name) or get_state(name) not in ("idle", "healthy")
                # placeholder לסטטוס – אחד לכל כרטיס
                status_ph = st.empty()
                # כפתור
                if st.button("Start", type="primary", use_container_width=True,
                             disabled=disabled, key=f"start_{name}"):
                    run_flow(name, status_ph)

            # מציג את מצב הסטטוס הנוכחי (אם לא לחצו עדיין)
            show_status(status_ph, get_state(name))

            # debug
            with st.expander("debug", expanded=False):
                st.write("state:", get_state(name))
                st.write("busy:", is_busy(name))
