
import streamlit as st
import json, random, os

APP_TITLE = "Milestone Quiz"

st.set_page_config(page_title=APP_TITLE, page_icon="🧠", layout="wide")

# --------- Compact, polished styling (dark/light friendly) ---------
st.markdown(
    """
    <style>
    /* tighten the default padding and set a nice max width */
    .main .block-container {max-width: 980px; padding-top: 1.25rem; padding-bottom: 2rem;}
    body {background: linear-gradient(180deg, rgba(248,250,252,1) 0%, rgba(255,255,255,1) 100%);}
    /* Title spacing */
    h1, h2, h3, h4 {margin-bottom: .25rem;}
    .subtitle {color: var(--text-color, #475569); font-size: 0.95rem; margin-bottom: .75rem;}
    /* Header controls */
    .controls .stButton>button, .controls .stSelectbox [data-baseweb="select"] {margin-top: .25rem;}
    /* Card */
    .card {background: var(--card-bg, #ffffff); border: 1px solid rgba(226,232,240,.9); border-radius: 16px;
           box-shadow: 0 8px 24px rgba(2,6,23,.06); padding: 18px;}
    /* Choice buttons */
    .stButton>button {text-align: left; width: 100%; border-radius: 12px; border: 1px solid #e2e8f0;
                      padding: 12px 14px; background: #fff;}
    .stButton>button:hover {background: #f8fafc; border-color: #38bdf8;}
    /* Small badge */
    .pill {display:inline-block; font-size: 12px; color: #0f172a; background: #f1f5f9;
           padding: 4px 10px; border-radius: 999px;}
    /* Feedback boxes tighter */
    .feedback .stAlert {padding: .5rem .75rem;}
    /* Make progress bar thin */
    .stProgress .st-bo {height: 8px !important;}
    /* Dark theme tweaks */
    @media (prefers-color-scheme: dark) {
        body {background: linear-gradient(180deg, #0b1220 0%, #111827 100%);}
        .card {background: #0f172a; border-color: #1f2937; box-shadow: 0 8px 24px rgba(0,0,0,.35);}
        .stButton>button {background: #0b1220; border-color: #1f2937; color: #e5e7eb;}
        .stButton>button:hover {background: #0b162a; border-color: #38bdf8;}
        .pill {background: #111827; color: #e5e7eb;}
        .subtitle {color:#9ca3af;}
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------- Load questions ---------
DATA_FILE = "milestone_quiz_questions.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        QUESTIONS = json.load(f)
else:
    st.error(f"Could not find {DATA_FILE}. Place it next to this app and rerun.")
    st.stop()

def shuffle_array(array):
    arr = list(array)
    random.shuffle(arr)
    return arr

def filter_bank(tag):
    if tag == "all":
        return QUESTIONS
    return [q for q in QUESTIONS if tag in q.get("tags", [])]

# --------- State ---------
if "filter" not in st.session_state:
    st.session_state.filter = "all"
if "questions" not in st.session_state:
    st.session_state.questions = shuffle_array(filter_bank(st.session_state.filter))
if "index" not in st.session_state:
    st.session_state.index = 0
if "selected" not in st.session_state:
    st.session_state.selected = None
if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "attempted" not in st.session_state:
    st.session_state.attempted = 0
if "missed_ids" not in st.session_state:
    st.session_state.missed_ids = []

def restart(new_filter=None, use_missed=False):
    if use_missed:
        missed_set = set(st.session_state.missed_ids)
        bank = [q for q in QUESTIONS if q["id"] in missed_set]
        st.session_state.questions = shuffle_array(bank) if bank else shuffle_array(filter_bank(st.session_state.filter))
        st.session_state.missed_ids = []
    else:
        if new_filter is None:
            new_filter = st.session_state.filter
        st.session_state.filter = new_filter
        st.session_state.questions = shuffle_array(filter_bank(new_filter))
    st.session_state.index = 0
    st.session_state.selected = None
    st.session_state.revealed = False
    st.session_state.correct = 0
    st.session_state.attempted = 0

def choose(i):
    if st.session_state.revealed:
        return
    q = st.session_state.questions[st.session_state.index]
    st.session_state.selected = i
    is_correct = (i == q["answer_index"])
    st.session_state.revealed = True
    st.session_state.attempted += 1
    if is_correct:
        st.session_state.correct += 1
    else:
        st.session_state.missed_ids.append(q["id"])

def next_question():
    if st.session_state.index < len(st.session_state.questions) - 1:
        st.session_state.index += 1
        st.session_state.selected = None
        st.session_state.revealed = False

# --------- Header ---------
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown(f"## {APP_TITLE}")
    st.markdown('<div class="subtitle">Single Best Answer • Instant feedback • 100 items</div>', unsafe_allow_html=True)
with c2:
    with st.container():
        st.markdown('<div class="controls">', unsafe_allow_html=True)
        bank = st.selectbox("Bank", ["all", "recall", "computation", "case", "gross", "fine", "language", "social", "growth", "reflex", "redflag"], index=0, help="Filter by tag")
        colA, colB = st.columns(2)
        if colA.button("Restart"):
            restart(new_filter=bank)
        if colB.button("Review missed"):
            restart(use_missed=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --------- Progress ---------
q_total = len(st.session_state.questions)
q_index = st.session_state.index
progress = 0 if q_total == 0 else int((q_index / q_total) * 100)
st.progress(progress, text=f"Question {q_index + 1} of {q_total}" if q_total else "Loading…")

# --------- Question Card ---------
st.markdown('<div class="card">', unsafe_allow_html=True)
if q_total == 0:
    st.info("No questions in this bank yet. Use Restart to reload all questions.")
else:
    q = st.session_state.questions[q_index]
    top = st.columns([7,3])
    with top[0]:
        st.markdown(f"### {q['stem']}")
    with top[1]:
        if q.get("tags"):
            st.markdown(f"<span class='pill'>{' • '.join(q['tags'])}</span>", unsafe_allow_html=True)

    st.write("")

    # Choices
    for i, choice in enumerate(q["choices"]):
        is_correct = (i == q["answer_index"])
        is_selected = (st.session_state.selected == i)
        cols = st.columns([1, 11])
        with cols[1]:
            if st.session_state.revealed:
                if is_selected and is_correct:
                    st.success("✔")
                elif is_selected and not is_correct:
                    st.error("✘")
                elif is_correct:
                    st.success("✔")
            else:
                st.write(" ")
        with cols[1]:
            if st.button(f"{chr(65+i)}. {choice}", key=f"c_{q['id']}_{i}", use_container_width=True, disabled=st.session_state.revealed):
                choose(i)

    # Feedback + nav
    st.markdown('<div class="feedback">', unsafe_allow_html=True)
    if st.session_state.revealed:
        if st.session_state.selected == q["answer_index"]:
            st.success("Correct")
        else:
            st.error("Incorrect")
        st.markdown(f"**Explanation:** {q['rationale']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Correct", st.session_state.correct)
        with col2:
            st.metric("Attempted", st.session_state.attempted)
        with col3:
            ratio = f"{st.session_state.correct}/{st.session_state.attempted}" if st.session_state.attempted else "0/0"
            st.metric("Ratio", ratio)

        if q_index < q_total - 1:
            st.button("Next question ➜", on_click=next_question, use_container_width=True)
        else:
            st.success("End of quiz.")
            colR1, colR2 = st.columns(2)
            with colR1:
                st.button("Review missed", on_click=lambda: restart(use_missed=True), use_container_width=True)
            with colR2:
                st.button("Restart all", on_click=lambda: restart(new_filter=st.session_state.filter), use_container_width=True)
    else:
        st.info("Click an answer to check it.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close card
