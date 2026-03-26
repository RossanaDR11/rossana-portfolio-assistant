import os
import streamlit as st
from rag_engine import answer, load_rag

st.set_page_config(
    page_title="Rossana De Rose — AI Portfolio",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    #MainMenu, footer, header { visibility: hidden; }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d1117 !important;
        color: #e6edf3;
    }
    .stApp { background-color: #0d1117 !important; }
    .main .block-container { max-width: 860px; padding: 1.5rem 2rem; }

    /* ── HEADER ─────────────────────────────────────── */
    .header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 1.4rem 1.8rem;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        margin-bottom: 1rem;
    }
    .avatar {
        width: 62px; height: 62px; flex-shrink: 0;
        background: linear-gradient(135deg, #58a6ff 0%, #3fb950 100%);
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700; font-size: 1.25rem; color: #0d1117;
    }
    .header-info { flex: 1; }
    .header-name {
        font-size: 2.3rem; font-weight: 700;
        color: #e6edf3; margin: 0 0 5px 0;
        letter-spacing: -0.8px;
        line-height: 1.1;
    }
    .header-role {
        font-size: 0.73rem; color: #8b949e; margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .header-badges { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
    .badge-green {
        background: #1a3a1a; color: #3fb950;
        border: 1px solid #2ea043;
        padding: 2px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 600;
    }
    .badge-blue {
        background: #1a2a3a; color: #58a6ff;
        border: 1px solid #1f6feb;
        padding: 2px 10px; border-radius: 20px; font-size: 0.7rem;
    }
    .badge-gray {
        background: #21262d; color: #8b949e;
        border: 1px solid #30363d;
        padding: 2px 10px; border-radius: 20px; font-size: 0.7rem;
    }
    .header-links { display: flex; flex-direction: column; gap: 4px; align-items: flex-end; }
    .hlink { font-size: 0.75rem; color: #58a6ff; text-decoration: none; }
    .hlink:hover { text-decoration: underline; }

    /* ── STATS ROW (first horizontal block on the page) ─ */
    [data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        height: 58px !important;
        white-space: pre-line !important;
        font-size: 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        line-height: 1.5 !important;
    }
    [data-testid="stHorizontalBlock"]:first-of-type .stButton > button p::first-line {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #58a6ff !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }
    [data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
        border-color: #58a6ff !important;
        background: #1a222e !important;
    }

    /* ── LANGUAGE PANEL ──────────────────────────────── */
    .lang-panel {
        display: flex; gap: 10px; flex-wrap: wrap;
        background: #161b22; border: 1px solid #3fb950;
        border-radius: 10px; padding: 0.8rem 1.2rem;
        margin-bottom: 0.8rem; align-items: center;
    }
    .lang-item {
        display: flex; align-items: center; gap: 8px;
        padding: 0.3rem 0.9rem;
        background: #21262d; border: 1px solid #30363d;
        border-radius: 20px;
    }
    .lang-flag { font-size: 1.1rem; }
    .lang-name { font-size: 0.8rem; font-weight: 600; color: #e6edf3; }
    .lang-level { font-size: 0.68rem; font-weight: 600; padding: 1px 7px; border-radius: 10px; }
    .lang-level.native { background: #1a3a1a; color: #3fb950; border: 1px solid #2ea043; }
    .lang-level.c1    { background: #1a2a3a; color: #58a6ff; border: 1px solid #1f6feb; }
    .lang-level.b2    { background: #2a2a1a; color: #e3b341; border: 1px solid #9e6a03; }

    /* ── SECTION LABELS ──────────────────────────────── */
    .section-label {
        font-size: 0.62rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.2px;
        color: #484f58; margin: 0.8rem 0 0.45rem 0;
        display: block;
    }
    .section-divider {
        border: none; border-top: 1px solid #21262d;
        margin: 0.6rem 0 0.8rem 0;
    }

    /* ── SKILLS ──────────────────────────────────────── */
    .skills-wrap {
        display: flex; flex-wrap: wrap; gap: 5px;
        margin-bottom: 0.5rem;
    }
    .skill-tag {
        background: #21262d; border: 1px solid #30363d;
        color: #8b949e; padding: 4px 11px;
        border-radius: 6px; font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.15s;
    }
    .skill-tag:hover { border-color: #3fb950; color: #3fb950; }

    /* ── QUICK QUESTIONS ─────────────────────────────── */
    .qlabel {
        font-size: 0.62rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.2px;
        color: #484f58; margin: 0.8rem 0 0.45rem 0;
    }
    .stButton > button {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 20px !important;
        color: #8b949e !important;
        font-size: 0.72rem !important;
        padding: 0 0.7rem !important;
        width: 100% !important;
        height: 3.4rem !important;
        white-space: normal !important;
        word-break: break-word !important;
        line-height: 1.3 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        background: #1f6feb !important;
        border-color: #58a6ff !important;
        color: #e6edf3 !important;
    }

    /* ── CHAT INPUT ──────────────────────────────────── */
    .stChatInput textarea {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        color: #e6edf3 !important;
        font-size: 0.88rem !important;
    }
    .stChatInput textarea:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88,166,255,0.1) !important;
    }

    /* ── CHAT MESSAGES ───────────────────────────────── */
    div[data-testid="stChatMessage"] {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.6rem !important;
    }
    div[data-testid="stChatMessage"] p { color: #e6edf3 !important; }

    /* ── DIVIDER ─────────────────────────────────────── */
    hr { border-color: #21262d !important; }

    /* ── EXPANDER ────────────────────────────────────── */
    details { background: #21262d !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
    summary { color: #8b949e !important; font-size: 0.8rem !important; }

    /* ── SPINNER ─────────────────────────────────────── */
    .stSpinner > div { border-top-color: #58a6ff !important; }

    /* ── PROJECTS PANEL ──────────────────────────────── */
    .proj-panel {
        background: #161b22; border: 1px solid #58a6ff;
        border-radius: 10px; padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .proj-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 10px; margin-top: 0.6rem;
    }
    .proj-card {
        background: #21262d; border: 1px solid #30363d;
        border-radius: 8px; padding: 0.75rem 0.9rem;
        display: flex; flex-direction: column; gap: 5px;
        transition: border-color 0.15s;
    }
    .proj-card:hover { border-color: #58a6ff; }
    .proj-title {
        font-size: 0.8rem; font-weight: 600;
        color: #e6edf3; margin: 0;
    }
    .proj-type {
        font-size: 0.65rem; font-weight: 600;
        padding: 2px 8px; border-radius: 10px;
        background: #1a2a3a; color: #58a6ff;
        border: 1px solid #1f6feb;
        display: inline-block; width: fit-content;
    }
    .proj-desc {
        font-size: 0.72rem; color: #8b949e;
        margin: 2px 0;
    }
    .proj-stack {
        font-size: 0.65rem; color: #484f58;
        font-family: 'JetBrains Mono', monospace;
    }
    .proj-link {
        font-size: 0.7rem; color: #58a6ff;
        text-decoration: none; margin-top: 4px;
        display: inline-block;
    }
    .proj-link:hover { text-decoration: underline; }
    .proj-panel-label {
        font-size: 0.62rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.2px;
        color: #58a6ff; margin: 0 0 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("vector_store/chunks.json"):
    with st.spinner("Building knowledge base..."):
        import subprocess
        subprocess.run(["python3", "1_ingest.py"], check=True)

load_rag()

# ── HEADER ────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <div class="avatar">RD</div>
    <div class="header-info">
        <p class="header-name">Rossana De Rose</p>
        <p class="header-role">~/data-analyst --data-science --ai-specialist</p>
        <div class="header-badges">
            <span class="badge-green">● Open to work</span>
            <span class="badge-blue">Remote · Hybrid · On-site</span>
            <span class="badge-gray">🇮🇹 🇬🇧 🇪🇸</span>
        </div>
    </div>
    <div class="header-links">
        <a class="hlink" href="mailto:rossanadero@hotmail.it">rossanadero@hotmail.it</a>
        <a class="hlink" href="https://linkedin.com/in/rossana-derose" target="_blank">↗ LinkedIn</a>
        <a class="hlink" href="https://github.com/RossanaDr11" target="_blank">↗ GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────
def _fire_question(q, key):
    if not st.session_state.get("messages"):
        st.session_state.messages = []
        st.session_state.sources  = []
    st.session_state.messages.append({"role": "user", "content": q})
    with st.spinner(""):
        history = [{"role": m["role"], "content": m["content"]}
                   for m in st.session_state.messages[:-1]]
        resp, srcs = answer(q, history)
    st.session_state.messages.append({"role": "assistant", "content": resp})
    st.session_state.sources = srcs
    st.rerun()

# ── STATS ─────────────────────────────────────────────────────────
st.markdown('<div class="stat-section"></div>', unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    if st.button("14+\n✈️ Aviation → AI", key="stat_exp"):
        _fire_question("What is your professional experience and career background?", "stat_exp")
with sc2:
    if st.button("7+\nProjects", key="stat_proj"):
        st.session_state.show_projects = not st.session_state.get("show_projects", False)
        st.rerun()
with sc3:
    if st.button("3\nLanguages", key="stat_lang"):
        st.session_state.show_languages = not st.session_state.get("show_languages", False)
        st.rerun()
with sc4:
    if st.button("🟢 Open\nto Work", key="stat_remote"):
        _fire_question("Remote available?", "stat_remote")

if st.session_state.get("show_languages", False):
    st.markdown("""
<div class="lang-panel">
    <div class="lang-item"><span class="lang-flag">🇮🇹</span><span class="lang-name">Italian</span><span class="lang-level native">Native</span></div>
    <div class="lang-item"><span class="lang-flag">🇬🇧</span><span class="lang-name">English</span><span class="lang-level c1">Proficient</span></div>
    <div class="lang-item"><span class="lang-flag">🇪🇸</span><span class="lang-name">Spanish</span><span class="lang-level b2">Proficient</span></div>
</div>
""", unsafe_allow_html=True)

if st.session_state.get("show_projects", False):
    st.markdown("""
<div class="proj-panel">
  <div class="proj-panel-label">AI &amp; Data Projects</div>
  <div class="proj-grid">

    <div class="proj-card">
      <p class="proj-title">Ryanair Customer Analytics</p>
      <span class="proj-type">Machine Learning · Streamlit</span>
      <p class="proj-desc">Random Forest model (95% accuracy, ROC-AUC 0.94) on 2,200+ real passenger reviews. Real-time Streamlit dashboard with ML inference.</p>
      <p class="proj-stack">Python · Scikit-Learn · Random Forest · Streamlit · Pandas</p>
      <a class="proj-link" href="https://github.com/RossanaDr11/Ryanair-Pr" target="_blank">↗ View on GitHub</a>
    </div>

    <div class="proj-card">
      <p class="proj-title">Gold Market Dashboard</p>
      <span class="proj-type">Business Intelligence · Power BI</span>
      <p class="proj-desc">Interactive Power BI dashboard analysing gold market trends with DAX measures, data modelling and KPI tracking.</p>
      <p class="proj-stack">Power BI · DAX · Power Query · Data Modelling</p>
      <a class="proj-link" href="https://github.com/RossanaDr11/gold-market-dashboard" target="_blank">↗ View on GitHub</a>
    </div>

    <div class="proj-card">
      <p class="proj-title">Golf Revenue Intelligence</p>
      <span class="proj-type">Analytics · Streamlit</span>
      <p class="proj-desc">Revenue analytics and business intelligence application for the golf industry, built with Streamlit.</p>
      <p class="proj-stack">Python · Streamlit · Pandas · Data Visualisation</p>
      <a class="proj-link" href="https://github.com/RossanaDr11/Golf-Revenue-Intelligence-" target="_blank">↗ View on GitHub</a>
    </div>

    <div class="proj-card">
      <p class="proj-title">Titanic — ML Classification</p>
      <span class="proj-type">Machine Learning · Streamlit</span>
      <p class="proj-desc">End-to-end ML pipeline on the Titanic dataset: EDA, feature engineering, classification model and interactive Streamlit app.</p>
      <p class="proj-stack">Python · Scikit-Learn · Pandas · Streamlit</p>
      <a class="proj-link" href="https://github.com/RossanaDr11/titanic" target="_blank">↗ View on GitHub</a>
    </div>

    <div class="proj-card">
      <p class="proj-title">Video Games Analysis</p>
      <span class="proj-type">EDA · Streamlit</span>
      <p class="proj-desc">Exploratory data analysis and interactive visualisation of video games sales and market data.</p>
      <p class="proj-stack">Python · Pandas · Streamlit · Matplotlib · Seaborn</p>
      <a class="proj-link" href="https://github.com/RossanaDr11/videojuegos" target="_blank">↗ View on GitHub</a>
    </div>

    <div class="proj-card">
      <p class="proj-title">Coffee Sales Analysis</p>
      <span class="proj-type">EDA · Streamlit</span>
      <p class="proj-desc">Sales analytics project exploring coffee sales data with interactive Streamlit dashboard and business insights.</p>
      <p class="proj-stack">Python · Pandas · Streamlit · Matplotlib · Seaborn</p>
      <a class="proj-link" href="https://github.com/RossanaDr11/proyecto_coffee_sales" target="_blank">↗ View on GitHub</a>
    </div>

    <div class="proj-card">
      <p class="proj-title">Portfolio Assistant (this app)</p>
      <span class="proj-type">AI · RAG · No external API</span>
      <p class="proj-desc">Interactive portfolio assistant using TF-IDF retrieval and local answer generation — no external AI API required.</p>
      <p class="proj-stack">Python · Scikit-Learn · Streamlit</p>
      <a class="proj-link" href="https://github.com/RossanaDr11" target="_blank">↗ GitHub Profile</a>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)

# ── SKILLS ────────────────────────────────────────────────────────
st.markdown("""
<hr class="section-divider">
<span class="section-label">Tech Stack</span>
<div class="skills-wrap">
    <span class="skill-tag">Python</span>
    <span class="skill-tag">SQL</span>
    <span class="skill-tag">Power BI</span>
    <span class="skill-tag">DAX</span>
    <span class="skill-tag">Machine Learning</span>
    <span class="skill-tag">RAG</span>
    <span class="skill-tag">NLP</span>
    <span class="skill-tag">Azure</span>
    <span class="skill-tag">Microsoft Fabric</span>
    <span class="skill-tag">Streamlit</span>
    <span class="skill-tag">Scikit-Learn</span>
    <span class="skill-tag">Pandas</span>
</div>
""", unsafe_allow_html=True)

# ── QUICK QUESTIONS ───────────────────────────────────────────────
st.markdown('<hr class="section-divider"><div class="qlabel">Quick questions</div>', unsafe_allow_html=True)

questions = [
    "Tell me about yourself",
    "Aviation → Data, why?",
    "Biggest project?",
    "Full tech stack?",
    "Power BI experience?",
    "Can she work under pressure?",
    "Remote available?",
    "What role is she looking for?",
    "Soft skills?",
    "¿Habla español?",
]

for i in range(0, len(questions), 2):
    c1, c2 = st.columns(2)
    with c1:
        if st.button(questions[i], key=f"q_{i}"):
            _fire_question(questions[i], i)
    with c2:
        if i + 1 < len(questions):
            if st.button(questions[i+1], key=f"q_{i+1}"):
                _fire_question(questions[i+1], i+1)

# ── CHAT AREA ─────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.sources  = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm Rossana's personal AI assistant.\n\nAsk me anything about her — skills, projects, experience, curiosities... I'll answer!\n\nYou can write in English, Spanish or Italian 🌍"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── CHAT INPUT ────────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything about Rossana..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner(""):
            history = [{"role": m["role"], "content": m["content"]}
                       for m in st.session_state.messages[1:-1]]
            response, sources = answer(prompt, history)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.sources = sources
    st.rerun()

# ── SOURCES + CLEAR ───────────────────────────────────────────────
if st.session_state.get("sources"):
    with st.expander("📄 Sources used for last answer"):
        for s in st.session_state.sources:
            st.caption(f"**{s['source'].replace('.txt','')}** — {s['text'][:180]}...")

col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources  = []
        st.rerun()
