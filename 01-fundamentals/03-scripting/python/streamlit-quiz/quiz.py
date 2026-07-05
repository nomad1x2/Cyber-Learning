"""
References:
- https://medium.com/@fesomade.alli/building-a-quiz-app-in-python-using-streamlit-d7c1aab4d690
- https://doodleclouds.medium.com/using-github-pages-to-host-your-streamlit-app-f274cbe3b3af
- https://edit.share.stlite.net/

Test question sets used:
- https://github.com/nomad1x2/PDFtoTEST.py

Question sets were altered to match a cleaner question bank
"""

import streamlit as st
import json
import random
import time
import os
from pathlib import Path

st.set_page_config(
    page_title="Quiz",
    layout="centered",
    initial_sidebar_state="collapsed",
)

random.seed()  # so its different each time the script runs

# just the list of question sets and which local json file each one uses
UNIT_OPTIONS = ["All Question Sets",
    "Analogies",
    "Artificial Language",
    "Classifications",
    "Logical Reasoning",
    "Logical Problems",
    "Necessary Part",
    "Number Series",
    "Sequences",
    "Verval Reasoning",
]

UNIT_FILES = {
    "All Question Sets":"quiz_sets/all.json",
    "Analogies":"quiz_sets/analogies.json",
    "Artificial Language":"quiz_sets/artificial_language.json",
    "Classifications":"quiz_sets/classification.json",
    "Logical Reasoning":"quiz_sets/logical_reasoning.json",
    "Logical Problems":"quiz_sets/logic_problems.json",
    "Necessary Part":"quiz_sets/necessary_part.json",
    "Number Series":"quiz_sets/number_series.json",
    "Sequences":"quiz_sets/sequences.json",
    "Verval Reasoning":"quiz_sets/verbal_reasoning.json",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #141414 !important;
    color: #e8e8e8 !important;
}
.stApp { background-color: #141414 !important; }

.question-card {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 1.75rem 1.75rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.question-meta {
    font-size: 0.75rem;
    font-weight: 600;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.6rem;
}
.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f0f0f0;
    line-height: 1.65;
    margin: 0;
}

div[data-testid="stRadio"] {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    display: block !important;
}
div[data-testid="stRadio"] > div,
div[data-testid="stRadio"] > div[role="radiogroup"] {
    gap: 0.4rem !important;
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
}
div[data-testid="stRadio"] > div > label,
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}
div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    padding: 0.6rem 0.9rem !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 7px !important;
    margin: 0 !important;
    cursor: pointer !important;
    background: #252525 !important;
    transition: background 0.12s, border-color 0.12s !important;
    line-height: 1.5 !important;
    width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}
div[data-testid="stRadio"] label:hover {
    background: #2a2f3d !important;
    border-color: #4a6fa5 !important;
}
div[data-testid="stRadio"] label p {
    margin: 0 !important;
    font-size: 0.95rem !important;
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif !important;
    text-align: left !important;
}
div[data-testid="stRadio"] > label {
    display: none !important;
}

div[data-testid="column"] div[data-testid="stRadio"],
div[data-testid="stVerticalBlock"] div[data-testid="stRadio"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
}

div[data-testid="stRadio"] label > div:last-child {
    flex: 1 !important;
    width: 100% !important;
    min-width: 0 !important;
}

div[data-testid="stElementContainer"][width="fit-content"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
}

.progress-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.progress-label {
    font-size: 2rem;
    color: #666;
    font-weight: 500;
}
.timer-text {
    color: #e0e0e0;
}
.timer-warn { color: #e05555 !important; }

.feedback-correct {
    background: #1a2e22;
    border: 1px solid #2e5c3a;
    border-left: 4px solid #3d9e58;
    border-radius: 7px;
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #5ec47a;
    margin-bottom: 1rem;
}
.feedback-wrong {
    background: #2e1a1a;
    border: 1px solid #5c2e2e;
    border-left: 4px solid #a03030;
    border-radius: 7px;
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #e06060;
    margin-bottom: 1rem;
}
.feedback-explanation {
    margin-top: 0.35rem;
    font-size: 0.84rem;
    font-weight: 400;
    color: #aaa;
    line-height: 1.5;
}

.score-big {
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    color: #f0f0f0;
    line-height: 1.1;
}
.score-sub {
    text-align: center;
    font-size: 1rem;
    color: #888;
    margin-bottom: 1.5rem;
    margin-top: 0.3rem;
}
.stat-row {
    display: flex;
    gap: 0.75rem;
    margin: 1rem 0;
}
.stat-box {
    flex: 1;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 0.9rem 0.5rem;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
}
.stat-val {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f0f0f0;
}
.stat-lbl {
    font-size: 0.7rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.2rem;
}

.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
    font-size: 0.9rem !important;
    width: 100% !important;
    padding: 0.6rem 1.1rem !important;
    transition: all 0.15s ease !important;
    background-color: #252525 !important;
    border: 1px solid #3a3a3a !important;
    color: #e0e0e0 !important;
}
.stButton > button:hover {
    background-color: #2e2e2e !important;
    border-color: #555 !important;
}

div[data-testid="column"]:last-child .stButton > button {
    font-size: 0.72rem !important;
    padding: 0.18rem 0.5rem !important;
    line-height: 1.2 !important;
    min-height: unset !important;
    height: auto !important;
    color: #555 !important;
    background: transparent !important;
    border-color: #2a2a2a !important;
    width: 100% !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    color: #999 !important;
    border-color: #444 !important;
    background: #1a1a1a !important;
}

label[data-testid="stWidgetLabel"] p,
div[data-testid="stSlider"] label p,
div[data-testid="stCheckbox"] label p {
    font-size: 0.9rem !important;
    color: #aaa !important;
}
input[type="text"], input[type="number"] {
    background-color: #1e1e1e !important;
    color: #e0e0e0 !important;
    border: 1px solid #333 !important;
}
.stTextInput input {
    background-color: #1e1e1e !important;
    color: #e0e0e0 !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    max-width: 680px !important;
}

details {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}
summary {
    color: #ccc !important;
}

.mastered-banner {
    background: #1a2233; border: 1px solid #2e4a7a; border-left: 4px solid #4a7acd;
    border-radius: 7px; padding: 0.75rem 1rem; font-size: 0.88rem;
    color: #7aaee8; margin-bottom: 1rem;
}
.resume-banner {
    background: #1e2218; border: 1px solid #3a4a2a; border-left: 4px solid #6a9a3a;
    border-radius: 7px; padding: 0.75rem 1rem; font-size: 0.88rem;
    color: #a0c870; margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

SCRIPT_DIR = Path(__file__).parent

def find_json_path(filename):
    # just checks a couple spots for the file, whichever one exists first wins
    for candidate in [SCRIPT_DIR / filename, Path(filename)]:
        if candidate.exists():
            return str(candidate)
    return filename

@st.cache_data
def load_questions(json_path):
    f = open(json_path, "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    return data["questions"]

def get_mastered_key(unit):
    return "mastered_keys_" + unit

def format_time(seconds):
    if seconds < 0:
        seconds = 0
    m = seconds // 60
    s = seconds % 60
    return "%02d:%02d" % (m, s)

def get_rank(pct):
    if pct >= 90:
        return "Excellent"
    elif pct >= 80:
        return "Good"
    elif pct >= 70:
        return "Satisfactory"
    elif pct >= 60:
        return "Marginal"
    else:
        return "Needs improvement"

def reset_quiz():
    random.seed()
    # hang on to stuff we want to keep, wipe the rest
    preserved = {}
    preserved["unit_selector"] = st.session_state.get("active_unit", st.session_state.get("unit_selector", "All Question Sets"))
    preserved["pref_num_questions"] = st.session_state.get("pref_num_questions", 10)
    preserved["cfg_randomize"] = st.session_state.get("cfg_randomize", True)
    preserved["cfg_use_timer"] = st.session_state.get("cfg_use_timer", False)
    preserved["cfg_timer_minutes"] = st.session_state.get("cfg_timer_minutes", 10)
    preserved["cfg_instant_feedback"] = st.session_state.get("cfg_instant_feedback", True)
    preserved["cfg_start_at"] = st.session_state.get("cfg_start_at", 1)

    for unit in UNIT_OPTIONS:
        mk = get_mastered_key(unit)
        preserved[mk] = st.session_state.get(mk, set())

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    for k in preserved:
        st.session_state[k] = preserved[k]

def full_reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "pref_num_questions" not in st.session_state:
    st.session_state.pref_num_questions = 10

if not st.session_state.quiz_active:

    st.markdown("## Quiz Setup")

    if "unit_selector" not in st.session_state:
        st.session_state.unit_selector = st.session_state.get("last_selected_unit", "All Question Sets")

    selected_unit = st.radio(
        "Select unit",
        UNIT_OPTIONS,
        horizontal=True,
        key="unit_selector",
    )
    st.session_state.last_selected_unit = selected_unit

    json_path = find_json_path(UNIT_FILES[selected_unit])

    if not os.path.exists(json_path):
        st.error("File not found: " + json_path)
        st.stop()

    unit_pool = load_questions(json_path)

    mastered_key = get_mastered_key(selected_unit)
    if mastered_key not in st.session_state:
        st.session_state[mastered_key] = set()
    mastered_set = st.session_state[mastered_key]

    total_available = len(unit_pool)
    mastered_count = len(mastered_set)
    available_count = total_available - mastered_count

    if total_available > 0 and available_count == 0:
        st.session_state[mastered_key] = set()
        mastered_set = set()
        mastered_count = 0
        available_count = total_available
        st.info("All questions in " + selected_unit + " have been mastered! The pool has been reset.")

    if mastered_count > 0:
        plural = "s" if mastered_count != 1 else ""
        st.markdown(
            '<div class="mastered-banner"><strong>' + str(mastered_count) + '</strong> question' + plural +
            ' mastered (' + selected_unit + ') &mdash; <strong>' + str(available_count) + '</strong> remaining in pool.</div>',
            unsafe_allow_html=True,
        )

    randomize = st.session_state.get("cfg_randomize", True)
    use_timer = st.session_state.get("cfg_use_timer", False)
    timer_minutes = st.session_state.get("cfg_timer_minutes", 10)
    instant_feedback = st.session_state.get("cfg_instant_feedback", True)
    start_at = st.session_state.get("cfg_start_at", 1)

    if start_at < 1:
        start_at = 1
    if start_at > available_count:
        start_at = available_count

    if not randomize:
        effective_available = available_count - (start_at - 1)
    else:
        effective_available = available_count
    if effective_available < 1:
        effective_available = 1

    num_questions = st.session_state.get("pref_num_questions", 10)
    if num_questions > effective_available:
        num_questions = effective_available
    if num_questions < 1:
        num_questions = 1

    st.markdown("---")

    if st.button("Start Quiz", use_container_width=True):
        random.seed()
        available_keys = [k for k in unit_pool if k not in mastered_set]

        if randomize:
            random.shuffle(available_keys)
            chosen = available_keys[:num_questions]
            pre_master_keys = []
        else:
            pre_master_keys = available_keys[:start_at - 1]
            remaining_keys = available_keys[start_at - 1:]
            chosen = remaining_keys[:num_questions]

        if pre_master_keys:
            st.session_state[mastered_key].update(pre_master_keys)

        new_questions = {}
        for k in chosen:
            new_questions[k] = unit_pool[k]

        st.session_state.questions = new_questions
        st.session_state.q_keys = chosen
        st.session_state.quiz_active = True
        st.session_state.current_q = 0
        st.session_state.selected_answers = {}
        st.session_state.answered = {}
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.q_start_time = time.time()
        st.session_state.elapsed_times = []
        st.session_state.time_up = False
        st.session_state.use_timer = use_timer
        st.session_state.timer_seconds = timer_minutes * 60
        st.session_state.instant_feedback = instant_feedback
        st.session_state.total = num_questions
        st.session_state.active_unit = selected_unit
        st.rerun()

    with st.expander("Settings", expanded=st.session_state.get("settings_open", True)):

        col_rand, col_timer_chk = st.columns(2)
        with col_rand:
            new_randomize = st.checkbox("Randomize order", value=randomize, key="randomize_chk")
            st.session_state["cfg_randomize"] = new_randomize
        with col_timer_chk:
            new_use_timer = st.checkbox("Enable timer", value=use_timer)
            st.session_state["cfg_use_timer"] = new_use_timer

        if not new_randomize and available_count > 1:
            max_start = available_count
            st.markdown(
                '<div class="resume-banner"><strong>Resume from question:</strong> Questions before this number '
                'will be marked as mastered so they are skipped on restart. Set to 1 to start from the beginning.</div>',
                unsafe_allow_html=True,
            )
            new_start_at = st.number_input(
                "Start at question # (1 - " + str(max_start) + ")",
                min_value=1,
                max_value=max_start,
                value=start_at,
                step=1,
                key="start_at_input",
            )
            st.session_state["cfg_start_at"] = int(new_start_at)
            eff_avail = available_count - (int(new_start_at) - 1)
            if eff_avail < 1:
                eff_avail = 1
        else:
            st.session_state["cfg_start_at"] = 1
            eff_avail = available_count

        def _sync_from_slider():
            v = st.session_state["slider_num_q"]
            st.session_state["pref_num_questions"] = v
            st.session_state["number_input_num_q"] = v

        def _sync_from_input():
            v = int(st.session_state["number_input_num_q"])
            st.session_state["pref_num_questions"] = v
            st.session_state["slider_num_q"] = v

        col1, col2 = st.columns(2)
        with col1:
            if eff_avail <= 1:
                st.markdown("**Number of questions:** " + str(eff_avail) + " *(only " + str(eff_avail) + " remaining)*")
                st.session_state["pref_num_questions"] = eff_avail
            else:
                clamped = st.session_state.get("pref_num_questions", 10)
                if clamped > eff_avail:
                    clamped = eff_avail
                if clamped < 1:
                    clamped = 1
                st.session_state["pref_num_questions"] = clamped
                st.session_state["slider_num_q"] = clamped
                st.session_state["number_input_num_q"] = clamped

                st.slider(
                    "Number of questions",
                    min_value=1,
                    max_value=eff_avail,
                    step=5 if eff_avail >= 10 else 1,
                    key="slider_num_q",
                    on_change=_sync_from_slider,
                )
                st.number_input(
                    "Or type an exact number",
                    min_value=1,
                    max_value=eff_avail,
                    step=1,
                    key="number_input_num_q",
                    on_change=_sync_from_input,
                )

        with col2:
            new_timer_minutes = st.slider("Duration (minutes)", 1, 60, timer_minutes, disabled=not new_use_timer)
            st.session_state["cfg_timer_minutes"] = new_timer_minutes

        new_instant = st.checkbox("Show correct answer after each question", value=instant_feedback)
        st.session_state["cfg_instant_feedback"] = new_instant

        st.markdown("*" + str(available_count) + " questions available (excluding mastered) in **" + selected_unit + "***")

        if mastered_count > 0:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            if st.button("Reset Mastered", key="reset_mastered_btn", use_container_width=True):
                st.session_state[mastered_key] = set()
                st.rerun()

elif st.session_state.quiz_active:

    questions = st.session_state.questions
    q_keys = st.session_state.q_keys
    total = st.session_state.total
    idx = st.session_state.current_q
    active_unit = st.session_state.get("active_unit", "All Question Sets")
    mastered_key = get_mastered_key(active_unit)
    if mastered_key not in st.session_state:
        st.session_state[mastered_key] = set()

    # need the full pool again just for the counts on the results page
    json_path = find_json_path(UNIT_FILES[active_unit])
    unit_pool = load_questions(json_path)

    elapsed = int(time.time() - st.session_state.start_time)
    if st.session_state.use_timer:
        remaining = st.session_state.timer_seconds - elapsed
        if remaining <= 0 and not st.session_state.time_up:
            st.session_state.time_up = True
            st.session_state.current_q = total
            st.rerun()

    if idx >= total:

        score = st.session_state.score
        pct = (score / total) * 100 if total else 0
        rank = get_rank(pct)
        elapsed = int(time.time() - st.session_state.start_time)
        if st.session_state.elapsed_times:
            avg_t = sum(st.session_state.elapsed_times) / len(st.session_state.elapsed_times)
        else:
            avg_t = 0

        if not st.session_state.get("results_processed"):
            newly_mastered = []
            for k in q_keys:
                if st.session_state.answered.get(k) is True:
                    newly_mastered.append(k)
            st.session_state[mastered_key].update(newly_mastered)
            if len(st.session_state[mastered_key]) >= len(unit_pool):
                st.session_state[mastered_key] = set()
                st.info("You've mastered every question in " + active_unit + "! The pool has been reset.")
            st.session_state.newly_mastered_count = len(newly_mastered)
            st.session_state.results_processed = True

        newly_mastered_count = st.session_state.get("newly_mastered_count", 0)
        mastered_total = len(st.session_state[mastered_key])

        if st.session_state.get("time_up"):
            st.warning("Time expired.")

        st.markdown('<div class="score-big">' + str(score) + ' / ' + str(total) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="score-sub">' + ("%.0f" % pct) + '% &mdash; ' + rank + '</div>', unsafe_allow_html=True)

        if newly_mastered_count > 0:
            plural = "s" if newly_mastered_count != 1 else ""
            st.markdown(
                '<div class="mastered-banner"><strong>' + str(newly_mastered_count) + '</strong> question' + plural +
                ' added to mastered (' + active_unit + ') &mdash; <strong>' + str(mastered_total) +
                '</strong> mastered total out of ' + str(len(unit_pool)) + '.</div>',
                unsafe_allow_html=True,
            )

        st.markdown('''
        <div class="stat-row">
            <div class="stat-box">
                <div class="stat-val">''' + str(score) + '''</div>
                <div class="stat-lbl">Correct</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">''' + str(total - score) + '''</div>
                <div class="stat-lbl">Incorrect</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">''' + format_time(elapsed) + '''</div>
                <div class="stat-lbl">Total time</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">''' + ("%.1f" % avg_t) + '''s</div>
                <div class="stat-lbl">Avg / question</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        missed = []
        for k in q_keys:
            if k in st.session_state.answered and not st.session_state.answered[k]:
                missed.append(k)

        if missed:
            with st.expander("Review missed questions (" + str(len(missed)) + ")"):
                for k in missed:
                    q = questions[k]
                    correct_key = list(q["answer"].keys())[0]
                    correct_text = list(q["answer"].values())[0]
                    your_raw = st.session_state.selected_answers.get(k, "Not answered")
                    st.markdown("**" + q["question"] + "**")
                    st.markdown("<span style='color:#c0392b'>Your answer: " + your_raw + "</span>", unsafe_allow_html=True)
                    st.markdown("<span style='color:#2e7d4f'>Correct: " + correct_key + " " + correct_text + "</span>", unsafe_allow_html=True)
                    st.markdown("---")

        st.markdown("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Restart Quiz"):
                reset_quiz()
                st.rerun()
        with c2:
            if st.button("New Settings"):
                reset_quiz()
                st.rerun()

    else:
        q_key = q_keys[idx]
        q_data = questions[q_key]
        opts = q_data["options"]
        correct_key = list(q_data["answer"].keys())[0]
        already_answered = q_key in st.session_state.answered

        timer_str = ""
        if st.session_state.use_timer:
            remaining = st.session_state.timer_seconds - elapsed
            warn_cls = "timer-warn" if remaining < 60 else "timer-text"
            timer_str = '<span class="' + warn_cls + '">' + format_time(remaining) + '</span>'

        prog_col, exit_col = st.columns([8, 1])
        with prog_col:
            timer_suffix = "&nbsp;&nbsp;" + timer_str if timer_str else ""
            st.markdown(
                '<div class="progress-label">'
                'Question ' + str(idx + 1) + ' of ' + str(total) + ' &nbsp;&middot;&nbsp; ' + str(st.session_state.score) + ' correct' + timer_suffix +
                '</div>',
                unsafe_allow_html=True,
            )
        with exit_col:
            if st.button("Exit", key="exit_btn", use_container_width=True):
                st.session_state.current_q = total
                st.rerun()

        st.progress(idx / total)
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="question-card">'
            '<div class="question-meta">Question ' + str(idx + 1) + '</div>'
            '<div class="question-text">' + q_data["question"] + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        option_labels = []
        for k, v in opts.items():
            option_labels.append(k + "  " + v)

        default_idx = None
        if q_key in st.session_state.selected_answers:
            saved = st.session_state.selected_answers[q_key]
            for i in range(len(option_labels)):
                if option_labels[i] == saved:
                    default_idx = i
                    break

        selected = st.radio(
            "Select an answer:",
            option_labels,
            index=default_idx,
            key="radio_" + q_key,
            disabled=already_answered,
        )

        btn_label = "Finish" if (already_answered and idx == total - 1) else "Next"
        if st.button(btn_label, use_container_width=True):
            if not already_answered:
                radio_val = st.session_state.get("radio_" + q_key)
                if radio_val:
                    chosen_key = None
                    for ok, ov in opts.items():
                        if (ok + "  " + ov) == radio_val:
                            chosen_key = ok
                            break
                    if chosen_key:
                        st.session_state.selected_answers[q_key] = radio_val
                        is_correct = chosen_key == correct_key
                        st.session_state.answered[q_key] = is_correct
                        if is_correct:
                            st.session_state.score += 1
                        st.session_state.elapsed_times.append(
                            time.time() - st.session_state.q_start_time
                        )
                        if not st.session_state.instant_feedback:
                            st.session_state.current_q += 1
                            st.session_state.q_start_time = time.time()
                        st.rerun()
            else:
                st.session_state.current_q += 1
                st.session_state.q_start_time = time.time()
                st.rerun()

        if already_answered and st.session_state.instant_feedback:
            is_correct = st.session_state.answered[q_key]
            expl = list(q_data["answer"].values())[0]
            if is_correct:
                st.markdown(
                    '<div class="feedback-correct">Correct'
                    '<div class="feedback-explanation">' + expl + '</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                correct_display = correct_key + "  " + opts.get(correct_key, "")
                st.markdown(
                    '<div class="feedback-wrong">Incorrect &mdash; correct answer: ' + correct_display +
                    '<div class="feedback-explanation">' + expl + '</div></div>',
                    unsafe_allow_html=True,
                )

        if st.session_state.use_timer and not already_answered:
            time.sleep(0.5)
            st.rerun()