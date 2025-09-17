import time
import random
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="רב-קו admin", layout="centered")
st.markdown(
    """
    <style>
      .headline { font-size: 28px; font-weight: 800; letter-spacing: .3px; margin-bottom: 14px; }
      /* NAV: radio נראה כמו טאבים עם קו */
      div[role="radiogroup"] > label {
        border: none !important;
        background: transparent !important;
        padding: 6px 12px !important;
        margin-right: 6px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
      }
      div[role="radiogroup"] > label:hover { background: #f3f4f6 !important; }
      div[role="radiogroup"] input:checked + div {
        color: #111827 !important;
        position: relative;
      }
      div[role="radiogroup"] input:checked + div:after {
        content: "";
        position: absolute;
        left: 8px; right: 8px; bottom: -6px;
        height: 3px; border-radius: 999px;
        background: #2563eb;
      }

      .chip { display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600; }
      .chip-green { background:#ecfdf5; color:#065f46; border:1px solid #10b98133; }
      .chip-red   { background:#fef2f2; color:#991b1b; border:1px solid #ef444433; }
      .chip-blue  { background:#eff6ff; color:#1e40af; border:1px solid #3b82f633; }
      .chip-amber { background:#fffbeb; color:#92400e; border:1px solid #f59e0b33; }

      .card { border:1px solid #e5e7eb; background:#ffffff; border-radius:14px; padding:16px 16px 10px 16px; box-shadow: 0 1px 2px rgba(0,0,0,.04); }
      .muted { color:#6b7280; font-size:12px; }
      .logs label p { font-size: 12px !important; }
      .logs textarea { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace !important; font-size:12px !important; line-height:1.35 !important; }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="headline">רב-קו admin</div>', unsafe_allow_html=True)

# ---------- Demo Config ----------
SERVICES = ["scraper", "parser", "indexer", "geocoder", "expander"]
AUTO_INTERVAL_SEC = 1.2
HEALTH_FLIP_EVERY = (3, 5)
MAX_LOGS = 600

# שלבים מדורגים (שם → משך שניות → "משקל" בפרוגרס)
PIPELINE = [
    ("checking",   0.8, 0.18),
    ("preparing",  0.8, 0.18),
    ("setup",      1.0, 0.26),
    ("warming_up", 0.9, 0.22),
    ("verifying",  0.7, 0.16),
    # running – סיום
]
STAGE_ORDER = [s for s, _, _ in PIPELINE] + ["running"]
DUR = {s: d for s, d, _ in PIPELINE}
WEI = {s: weight for s, _, weight in PIPELINE}  # ← תוקן

# ---------- State init ----------
st.session_state.setdefault("active_idx", 0)
st.session_state.setdefault("auto_chain", False)

for i, _name in enumerate(SERVICES):
    base = f"s{i}"
    st.session_state.setdefault(f"{base}_stage", "idle")
    st.session_state.setdefault(f"{base}_t0", 0.0)
    st.session_state.setdefault(f"{base}_connected", True)
    st.session_state.setdefault(f"{base}_tick", 0)
    st.session_state.setdefault(f"{base}_logs", [])
    st.session_state.setdefault(f"{base}_started", False)
    st.session_state.setdefault(f"{base}_completed", False)
    st.session_state.setdefault(f"{base}_elapsed", 0.0)

# ---------- Helpers ----------
def _add_log(i: int, text: str):
    base = f"s{i}"
    ts = time.strftime("%H:%M:%S")
    st.session_state[f"{base}_logs"].append(f"[{ts}] {text}")
    if len(st.session_state[f"{base}_logs"]) > MAX_LOGS:
        st.session_state[f"{base}_logs"] = st.session_state[f"{base}_logs"][-MAX_LOGS:]

def _pump_auto_logs(i: int, name: str):
    stage = st.session_state[f"s{i}_stage"]
    bag_map = {
        "idle":        ["idle", "wait", "scheduler"],
        "checking":    ["probe", "ping", "latency", "uptime"],
        "preparing":   ["bootstrap", "preflight", "deps", "env"],
        "setup":       ["init", "config", "apply", "migrate"],
        "warming_up":  ["warmup", "cache", "load", "prime"],
        "verifying":   ["verify", "health", "checks", "ready"],
        "running":     ["worker", "event", "batch", "throughput", "req"]
    }
    bag = bag_map.get(stage, ["log"])
    for _ in range(random.randint(5, 9)):
        w1, w2 = random.choice(bag), random.choice(bag)
        ms = random.randint(2, 220)
        _add_log(i, f"{name}: {stage} · {w1}/{w2} · {ms}ms")

def _auto_health(i: int, name: str):
    base = f"s{i}"
    st.session_state[f"{base}_tick"] += 1
    t = st.session_state[f"{base}_tick"]
    if t % random.randint(*HEALTH_FLIP_EVERY) == 0:
        st.session_state[f"{base}_connected"] = random.choice([True, True, True, False])
        txt = "Connected" if st.session_state[f"{base}_connected"] else "Disconnected"
        _add_log(i, f"{name}: health-probe → {txt}")

def _start_service(i: int, reason: str):
    base = f"s{i}"
    if not st.session_state[f"{base}_started"]:
        st.session_state[f"{base}_stage"] = "checking"
        st.session_state[f"{base}_t0"] = time.time()
        st.session_state[f"{base}_elapsed"] = 0.0
        st.session_state[f"{base}_started"] = True
        _add_log(i, f"{SERVICES[i]}: {reason} → checking")

def _next_stage(stage: str) -> str:
    idx = STAGE_ORDER.index(stage)
    return STAGE_ORDER[min(idx + 1, len(STAGE_ORDER) - 1)]

def _advance_stage_if_ready(i: int):
    base = f"s{i}"
    name = SERVICES[i]
    stage = st.session_state[f"{base}_stage"]
    t0 = st.session_state[f"{base}_t0"]
    now = time.time()

    if stage == "idle" or stage == "running":
        return

    st.session_state[f"{base}_elapsed"] = max(0.0, now - t0)

    if stage in DUR and (now - t0) >= DUR[stage]:
        new_stage = _next_stage(stage)
        st.session_state[f"{base}_stage"] = new_stage
        st.session_state[f"{base}_t0"] = now
        st.session_state[f"{base}_elapsed"] = 0.0

        if new_stage == "running" and not st.session_state[f"{base}_completed"]:
            st.session_state[f"{base}_completed"] = True
            if st.session_state["auto_chain"]:
                next_i = i + 1
                if next_i < len(SERVICES):
                    _start_service(next_i, "auto-start (chain)")
                    st.session_state["active_idx"] = next_i
                else:
                    _add_log(i, "Chain: last service reached.")

def _progress_value(i: int) -> float:
    stage = st.session_state[f"s{i}_stage"]
    if stage == "idle":
        return 0.0
    if stage == "running":
        return 1.0

    completed_weight = 0.0
    for s, _, w in PIPELINE:
        if s == stage:
            break
        completed_weight += w

    elapsed = st.session_state[f"s{i}_elapsed"]
    dur = DUR.get(stage, 1.0)
    frac = max(0.0, min(1.0, elapsed / dur))
    return min(1.0, completed_weight + WEI.get(stage, 0.0) * frac)

def _status_chip(stage: str) -> str:
    mapping = {
        "checking":   '<span class="chip chip-blue">Checking…</span>',
        "preparing":  '<span class="chip chip-blue">Preparing…</span>',
        "setup":      '<span class="chip chip-blue">Setting up…</span>',
        "warming_up": '<span class="chip chip-blue">Warming up…</span>',
        "verifying":  '<span class="chip chip-blue">Verifying…</span>',
        "running":    '<span class="chip chip-green">Running ✅</span>',
        "idle":       '<span class="chip chip-amber">Ready (idle)</span>',
    }
    return mapping.get(stage, '<span class="chip chip-amber">Ready</span>')

def _conn_chip(connected: bool) -> str:
    return f'<span class="chip {"chip-green" if connected else "chip-red"}">{"Connected ✅" if connected else "Disconnected 🔴"}</span>'

# ---------- Tabs Controller ----------
active = st.radio(
    "בחר סרבר",
    options=list(range(len(SERVICES))),
    format_func=lambda i: SERVICES[i],
    index=st.session_state["active_idx"],
    horizontal=True,
    key="active_idx_radio",
)
st.session_state["active_idx"] = active
i = st.session_state["active_idx"]
name = SERVICES[i]

# ---------- Card ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1.2, 1.6, 2.0, 5])
with c1:
    if st.button("Start", key=f"start_{i}"):
        st.session_state["auto_chain"] = True
        _start_service(i, "manual start")
with c2:
    st.markdown(_conn_chip(st.session_state[f"s{i}_connected"]), unsafe_allow_html=True)
with c3:
    st.markdown(_status_chip(st.session_state[f"s{i}_stage"]), unsafe_allow_html=True)
with c4:
    elapsed = st.session_state[f"s{i}_elapsed"]
    st.markdown(f'<span class="muted">elapsed: {elapsed:.1f}s</span>', unsafe_allow_html=True)

_advance_stage_if_ready(i)
progress = _progress_value(i)
if progress > 0.001 or st.session_state[f"s{i}_stage"] != "idle":
    st.progress(progress)

st.markdown("**Logs**")
with st.container():
    _pump_auto_logs(i, name)
    st.markdown('<div class="logs">', unsafe_allow_html=True)
    st.text_area(
        "Service logs",
        value="\n".join(st.session_state[f"s{i}_logs"]),
        height=260,
        key=f"logs_view_{i}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # /card

_auto_health(i, name)

need_auto = any(st.session_state[f"s{j}_started"] for j in range(len(SERVICES)))
if need_auto or st.session_state.get("auto_chain", False):
    time.sleep(AUTO_INTERVAL_SEC)
    st.rerun()
