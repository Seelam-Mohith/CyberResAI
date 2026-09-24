import os
import re
import sys
import time

import streamlit as st

sys.stdout.reconfigure(encoding="utf-8")

import config
from rag import answer_question
from utils.embeddings import embeddings

PAGE_TITLE = "CyberRes-AI"
PAGE_ICON = "🛡️"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 10

CSS = """
<style>
:root {
    --cyber-bg: #070b14;
    --cyber-panel: #0d1424;
    --cyber-border: #1b2740;
    --cyber-cyan: #00e5ff;
    --cyber-magenta: #ff2d78;
    --cyber-text: #d7e2f4;
    --cyber-dim: #7b8bab;
}

.stApp {
    background:
        radial-gradient(1200px 500px at 85% -10%, rgba(0, 229, 255, 0.09), transparent 60%),
        radial-gradient(900px 500px at 0% 110%, rgba(255, 45, 120, 0.07), transparent 60%),
        var(--cyber-bg);
    color: var(--cyber-text);
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
#MainMenu,
footer {
    display: none !important;
}

[data-testid="stSidebar"] {
    background: #0a101d;
    border-right: 1px solid var(--cyber-border);
}
[data-testid="stSidebar"] * {
    color: var(--cyber-text);
}
[data-testid="stSidebar"] a {
    color: var(--cyber-cyan);
    text-decoration: none;
}
[data-testid="stSidebar"] a:hover {
    color: #ffffff;
    text-decoration: underline;
}
[data-testid="stSidebar"] hr {
    border-color: var(--cyber-border);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
    font-family: "Segoe UI", "Consolas", monospace;
    font-size: 0.9rem;
}
[data-testid="stSidebarCollapseButton"] svg {
    fill: var(--cyber-dim);
}
[data-testid="collapsedControl"] {
    background: rgba(13, 20, 36, 0.0);
}
[data-testid="stSidebarCollapseButton"]:hover {
    border-color: rgba(0, 229, 255, 0.4) !important;
}
[data-testid="collapsedControl"] svg {
    fill: var(--cyber-dim);
}
@media (max-width: 991px) {
    [data-testid="stSidebar"] {
        border-right: 1px solid var(--cyber-border);
    }
}

.block-container {
    max-width: 880px;
    padding-top: 2.2rem;
    padding-bottom: 6rem;
}

/* nav bar */
.cyber-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.1rem;
    padding: 0.5rem 0.85rem;
    background: rgba(7, 11, 20, 0.92);
    backdrop-filter: blur(8px);
    border: none;
    border-bottom: 1px solid var(--cyber-border);
    border-radius: 0;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-height: 2.2rem;
}
.nav-logo {
    font-family: "Segoe UI", "Consolas", monospace;
    font-size: 1.02rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    background: linear-gradient(90deg, #00e5ff 0%, #ff2d78 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    white-space: nowrap;
}
.nav-status {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-family: "Consolas", monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    color: #2ee6a8;
    white-space: nowrap;
}
.nav-status::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #2ee6a8;
    box-shadow: 0 0 8px rgba(46, 230, 168, 0.8);
}
#cybernav [data-testid="stButton"] button {
    width: 100%;
    background: transparent;
    border: 1px solid transparent;
    color: var(--cyber-dim);
    font-family: "Consolas", "Courier New", monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.42rem 0.5rem;
    border-radius: 7px;
    transition: all 0.15s ease;
}
#cybernav [data-testid="stButton"] button:hover {
    color: var(--cyber-cyan);
    border-color: rgba(0, 229, 255, 0.35);
    background: rgba(0, 229, 255, 0.08);
    transform: translateY(-1px);
}

.user-bubble, .ai-bubble {
    border-radius: 14px;
    padding: 0.85rem 1.1rem;
    margin: 0.45rem 0;
    line-height: 1.55;
    font-size: 0.95rem;
    max-width: 100%;
    overflow-wrap: anywhere;
    word-break: break-word;
}
.user-bubble {
    background: linear-gradient(135deg, #123, #0e2233);
    border: 1px solid rgba(0, 229, 255, 0.35);
    box-shadow: 0 0 18px rgba(0, 229, 255, 0.08);
    margin-left: 1.5rem;
}
.ai-bubble {
    background: rgba(13, 20, 36, 0.9);
    border: 1px solid var(--cyber-border);
    border-left: 3px solid var(--cyber-cyan);
}
.ai-bubble p { margin: 0.35rem 0; }
.ai-bubble code {
    background: rgba(0, 229, 255, 0.1);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 4px;
    padding: 0.05rem 0.3rem;
    font-size: 0.88em;
}
.ai-bubble pre {
    background: #0a0f1c;
    border: 1px solid var(--cyber-border);
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    overflow-x: auto;
    max-width: 100%;
    box-sizing: border-box;
}
.ai-bubble img {
    max-width: 100%;
}
.ai-bubble table {
    display: block;
    max-width: 100%;
    overflow-x: auto;
}

.cyber-chip {
    font-family: "Consolas", monospace;
    font-size: 0.78rem;
}

/* inputs */
[data-testid="stChatInput"] textarea {
    background: var(--cyber-panel) !important;
    border: 1px solid var(--cyber-border) !important;
    border-radius: 12px !important;
    color: var(--cyber-text) !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--cyber-cyan) !important;
    box-shadow: 0 0 0 1px rgba(0, 229, 255, 0.4) !important;
}

[data-testid="stExpander"] {
    background: rgba(13, 20, 36, 0.7) !important;
    border: 1px solid var(--cyber-border) !important;
    border-radius: 10px !important;
}

/* status banner */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid var(--cyber-border) !important;
}

/* hero intelligence card */
.hero-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(160deg, rgba(10, 18, 33, 0.95), rgba(13, 20, 36, 0.85));
    border: 1px solid var(--cyber-border);
    border-radius: 16px;
    padding: 1.15rem 1.3rem 1.05rem;
    margin: 0.5rem 0 0.9rem;
    box-shadow: inset 0 0 0 1px rgba(0, 229, 255, 0.05), 0 14px 36px rgba(0, 0, 0, 0.35);
}
.hero-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(340px 150px at 100% 0%, rgba(0, 229, 255, 0.12), transparent 60%),
        radial-gradient(300px 150px at 0% 100%, rgba(255, 45, 120, 0.10), transparent 60%);
    pointer-events: none;
}
.hero-head {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.1rem;
}
.hero-title {
    font-family: "Segoe UI", "Consolas", monospace;
    font-size: 1.32rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: linear-gradient(90deg, #00e5ff 0%, #ff2d78 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-family: "Consolas", "Courier New", monospace;
    color: var(--cyber-dim);
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin: 0 0 0.85rem;
}
.hero-intro {
    color: var(--cyber-text);
    font-size: 0.95rem;
    line-height: 1.55;
    margin: 0 0 0.95rem;
}
.hero-intro b { color: #00e5ff; }

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.6rem;
}
.stat {
    background: rgba(9, 15, 27, 0.9);
    border: 1px solid var(--cyber-border);
    border-left: 3px solid var(--cyber-cyan);
    border-radius: 10px;
    padding: 0.5rem 0.7rem;
    min-width: 0;
}
.stat:nth-child(3n+2) { border-left-color: var(--cyber-magenta); }
.stat:nth-child(3n)   { border-left-color: #ffb300; }
.stat-value {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--cyber-text);
    line-height: 1.2;
    overflow-wrap: anywhere;
    word-break: break-word;
}
.stat-value .accent { color: var(--cyber-cyan); }
.stat-label {
    color: var(--cyber-dim);
    font-size: 0.66rem;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-top: 0.12rem;
}
.hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.1rem;
    margin-top: 0.9rem;
    padding-top: 0.75rem;
    border-top: 1px dashed rgba(27, 39, 64, 0.8);
    font-family: "Consolas", "Courier New", monospace;
    font-size: 0.74rem;
    color: var(--cyber-dim);
}
.hero-meta b { color: var(--cyber-cyan); font-weight: 600; }

.latency-chip {
    font-family: "Consolas", monospace;
    font-size: 0.72rem;
    color: var(--cyber-dim);
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    margin: 0.15rem 0 0.5rem 1.6rem;
}
.latency-chip b { color: var(--cyber-cyan); font-weight: 600; }

@media (max-width: 640px) {
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
}

</style>
"""

TECH_RE = re.compile(r"(?:^|[\\/])(T1\d{3}(?:\.\d{3})?)", re.IGNORECASE)


def badge(text, color):
    return f'<span style="background:{color};color:#04121c;font-weight:700;' \
           f'padding:0.1rem 0.5rem;border-radius:6px;margin-right:0.4rem;">{text}</span>'


def to_avatar(role):
    return {"user": "🧑‍💻", "assistant": "🛡️"}[role]


def source_tag(markdown):
    return badge(markdown, "#00e5ff")


def fallback_tag(_path):
    return badge("ATOMIC-TEST", "#39445c")


def has_key():
    return bool(getattr(config, "GROQ_API_KEY", None))


def check_environment():
    ok = has_key()
    if not ok:
        st.error(
            "**GROQ_API_KEY is missing.** The AI responses won't work until it's set.\n\n"
            "- **Running locally** → add it to your `.env` file:\n\n"
            "  `GROQ_API_KEY=<your-key>`\n\n"
            "- **Running on Streamlit Cloud** → open the deployed app → **⋮ → Settings → Secrets** "
            "and paste exactly (TOML format):\n\n"
            "  `GROQ_API_KEY = \"<your-key>\"`\n\n"
            "Save and the app will restart.",
            icon="🔑",
        )
    try:
        embeddings
    except Exception as exc:
        st.error(f"Could not load the embedding model: {exc}", icon="🧠")
        ok = False
    if not os.path.exists(os.path.join("db", "chroma.sqlite3")):
        st.error(
            "**Vector database not found.** Run `python ingest.py` to build it "
            "from the playbooks, then reload the app.",
            icon="🗄️",
        )
        ok = False
    return ok


def embed_dim():
    try:
        return len(embeddings.embed_query("status"))
    except Exception:
        return None


def chunk_count():
    try:
        from utils.retriever import get_vector_db

        return get_vector_db()._collection.count()
    except Exception:
        return None


def playbook_count():
    root = os.path.join("data", "atomics")
    if not os.path.isdir(root):
        return None
    count = 0
    for _, _, files in os.walk(root):
        count += sum(1 for f in files if f.lower().endswith(".md"))
    return count


def technique_count():
    root = os.path.join("data", "atomics")
    if not os.path.isdir(root):
        return None
    return sum(1 for d in os.listdir(root) if re.match(r"^T\d{4}(?:\.\d{3})?$", d))


def latency_summary():
    latencies = st.session_state.get("latencies", [])
    if not latencies:
        return None
    return sum(latencies) / len(latencies), len(latencies)


def _stat(value, label, accent=False):
    value_html = f'<span class="accent">{value}</span>' if accent else value
    return (
        f'<div class="stat"><div class="stat-value">{value_html}</div>'
        f'<div class="stat-label">{label}</div></div>'
    )


def welcome_card_html():
    playbooks, techs, vecs = playbook_count(), technique_count(), chunk_count()
    dim = embed_dim()
    dim_label = f"Embeddings · {dim}-d" if dim else "Embedding model"

    latency = latency_summary()
    if latency:
        avg, n = latency
        latency_html = f"avg response <b>{avg:.1f}s</b> <span>· {n} quer{'y' if n == 1 else 'ies'}</span>"
    else:
        latency_html = "awaiting <b>first query</b>"

    stats = "".join(
        [
            _stat(f"{playbooks:,}" if playbooks else "—", "Playbooks loaded"),
            _stat(str(techs) if techs else "—", "Techniques covered", accent=True),
            _stat(f"{vecs:,}" if vecs else "—", "Vectors indexed", accent=True),
            _stat(embeddings.model_name, dim_label),
            _stat("ChromaDB", "Vector store", accent=True),
            _stat("gpt-oss-120b", "LLM model · Groq"),
        ]
    )

    return f"""
    <div class="hero-card">
      <div class="hero-head">🛡️ <span class="hero-title">CYBERRES-AI</span></div>
      <p class="hero-sub">// MITRE ATT&amp;CK Defense Intelligence · RAG Engine Online</p>
      <p class="hero-intro">Hi, I'm <b>CyberResAI</b> — your MITRE ATT&amp;CK defense advisor.
      Ask me about attacker techniques, detection ideas, or mitigation steps.</p>
      <div class="stat-grid">{stats}</div>
      <div class="hero-meta">
        <span>⚡ {latency_html}</span>
        <span>🧩 chunk <b>{CHUNK_SIZE}</b> / overlap <b>{CHUNK_OVERLAP}</b></span>
        <span>🔎 top-k <b>{TOP_K}</b></span>
      </div>
    </div>
    """


def render_message(role, content, sources=None, avatar=True):
    bubble_class = "user-bubble" if role == "user" else "ai-bubble"
    avatar_html = (
        f'<span style="font-size:1.5rem;vertical-align:top;margin-right:0.5rem;">{to_avatar(role)}</span>'
        if avatar else ""
    )
    st.markdown(
        f'<div class="{bubble_class}">{avatar_html}{content}</div>',
        unsafe_allow_html=True,
    )
    if sources:
        with st.expander(f"Sources — {len(sources)} retrieved"):
            for src in sources:
                matched = TECH_RE.search(src.replace("/", "\\"))
                tag = matched.group(1).upper() if matched else "playbook"
                tactic_id = source_tag(tag) if matched else fallback_tag(src)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.6rem;'
                    f'font-family:Consolas,monospace;font-size:0.83rem;">'
                    f'<span style="color:#7b8bab;">📄</span>{tactic_id}'
                    f'<span style="color:#94a7c8;word-break:break-all;">{src}</span></div>',
                    unsafe_allow_html=True,
                )


def ask(question):
    answer, sources, latency = None, [], None
    try:
        with st.spinner("🛡️ Scanning threat intel…"):
            started = time.perf_counter()
            result = answer_question(
                question,
                k=st.session_state.get("k", TOP_K),
                max_attempts=st.session_state.get("max_attempts", 5),
            )
            latency = time.perf_counter() - started
            answer, sources = result.get("answer", ""), result.get("sources", [])
            if latency is not None:
                st.session_state.setdefault("latencies", []).append(latency)
    except RuntimeError as exc:
        st.error(f"**LLM unavailable:** {exc}", icon="⚠️")
    except Exception as exc:
        st.error(f"Something went wrong.\n\n`{type(exc).__name__}: {exc}`", icon="🚨")
    else:
        if not answer:
            st.error("The model returned an empty response. Try asking differently.", icon="🤨")
    return answer, sources, latency


CLEAR_ACTION = "__clear__"


def render_navbar():
    st.markdown('<div id="cybernav" class="cyber-nav">', unsafe_allow_html=True)
    brand_col, cd_col, c2_col, ph_col, new_col = st.columns(
        [2.6, 1.35, 1.25, 1.25, 1.2], gap="small", vertical_alignment="center"
    )
    with brand_col:
        st.markdown(
            '<div class="nav-left">🛡️ <span class="nav-logo">CYBERRES-AI</span>'
            '<span class="nav-status">ONLINE</span></div>',
            unsafe_allow_html=True,
        )
    selection = None
    with cd_col:
        if st.button("Credential Dump", key="nav_cd", use_container_width=True):
            selection = "How does an attacker dump credentials?"
    with c2_col:
        if st.button("C2 Beaconing", key="nav_c2", use_container_width=True):
            selection = "How can I detect C2 beaconing traffic on endpoints?"
    with ph_col:
        if st.button("Phishing", key="nav_ph", use_container_width=True):
            selection = "How can I defend against phishing with payload delivery?"
    with new_col:
        if st.button("New chat", key="nav_new", use_container_width=True):
            selection = CLEAR_ACTION
    st.markdown("</div>", unsafe_allow_html=True)
    return selection


REPO_URL = "https://github.com/Seelam-Mohith/CyberResAI"
ISSUES_URL = "https://github.com/Seelam-Mohith/CyberResAI/issues"


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="nav-left">🛡️ <span class="nav-logo" style="font-size:1.05rem;">'
            "CYBERRES-AI</span></div>",
            unsafe_allow_html=True,
        )
        st.caption("MITRE ATT&CK Defense Intelligence — RAG assistant over Atomic Red Team playbooks.")

        st.markdown("---")

        st.markdown("**📍 Project**")
        st.markdown(f"- **[Repository]({REPO_URL})**")
        st.markdown(f"- **[Report an issue]({ISSUES_URL})**")

        st.markdown("---")

        st.markdown("**👨‍💻 Developed by**")
        st.markdown("**Seelam Mohith**")
        st.caption("Cybersecurity enthusiast · Detection & response")

        st.markdown("---")

        st.markdown("**⚙️ Stack**")
        st.markdown(
            "- Embeddings: `all-MiniLM-L6-v2`\n"
            "- Vector DB: `ChromaDB`\n"
            "- LLM: `gpt-oss-120b` (Groq)\n"
            "- Framework: `LangChain` + `Streamlit`"
        )

        st.markdown("---")

        st.markdown(
            "> ⚠️ **Disclaimer** — For educational and defensive security only. "
            "Atomic tests contain simulated adversarial behavior; never run them on production systems."
        )


def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered", initial_sidebar_state="collapsed")
    st.markdown(CSS, unsafe_allow_html=True)

    render_sidebar()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    nav_prompt = render_navbar()
    if nav_prompt == CLEAR_ACTION:
        st.session_state.messages = []
        st.rerun()

    ready = check_environment()

    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"], msg.get("sources"))

    prompt = nav_prompt or st.chat_input("Ask about a technique, e.g. 'How does an attacker dump credentials?'")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_message("user", prompt)

        if ready:
            answer, sources, latency = ask(prompt)
            if answer:
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
                render_message("assistant", answer, sources)
                if latency is not None:
                    st.markdown(
                        f'<div class="latency-chip">⚡ retrieval + generation in '
                        f'<b>{latency:.1f}s</b></div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Fix the environment issues above, then send your question again.", icon="🔧")

    if not st.session_state.messages:
        st.markdown(welcome_card_html(), unsafe_allow_html=True)
        with st.expander("💡 Say hello by asking…"):
            st.markdown(
                "- **Credential dumping** — how it works & how to stop it\n"
                "- **Detecting C2 beaconing** traffic on endpoints\n"
                "- **Defending against phishing** with payload delivery\n"
                "- A MITRE technique ID like **T1021.001**"
            )

    if st.session_state.messages:
        if st.button("Clear conversation", use_container_width=False, type="secondary"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()