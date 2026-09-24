import re
import sys

import streamlit as st

sys.stdout.reconfigure(encoding="utf-8")

import config
from rag import answer_question
from utils.embeddings import embeddings

PAGE_TITLE = "CyberResAI"
PAGE_ICON = "🛡️"

DEFAULT_WELCOME = (
    "Hi, I'm **CyberResAI** — your MITRE ATT&CK defense advisor.\n\n"
    "Ask me about attacker techniques, detection ideas, or mitigation steps."
)

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
    display: none;
}

.block-container {
    max-width: 880px;
    padding-top: 2.2rem;
    padding-bottom: 6rem;
}

/* title */
.cyber-title {
    font-family: "Segoe UI", "Consolas", monospace;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    background: linear-gradient(90deg, #00e5ff 0%, #ff2d78 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.cyber-sub {
    font-family: "Consolas", "Courier New", monospace;
    color: var(--cyber-dim);
    font-size: 0.82rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-top: 0.35rem;
}

.user-bubble, .ai-bubble {
    border-radius: 14px;
    padding: 0.85rem 1.1rem;
    margin: 0.45rem 0;
    line-height: 1.55;
    font-size: 0.95rem;
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
            "**GROQ_API_KEY is missing.** Add it to your `.env` file "
            "`(GROQ_API_KEY=... )` or the AI responses won't work.",
            icon="🔑",
        )
    try:
        embeddings
    except Exception as exc:
        st.error(f"Could not load the embedding model: {exc}", icon="🧠")
        ok = False
    return ok


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
    answer, sources = None, []
    try:
        with st.spinner("🛡️ Scanning threat intel…"):
            result = answer_question(
                question,
                k=st.session_state.get("k", 10),
                max_attempts=st.session_state.get("max_attempts", 5),
            )
            answer, sources = result.get("answer", ""), result.get("sources", [])
    except RuntimeError as exc:
        st.error(f"**LLM unavailable:** {exc}", icon="⚠️")
    except Exception as exc:
        st.error(f"Something went wrong.\n\n`{type(exc).__name__}: {exc}`", icon="🚨")
    else:
        if not answer:
            st.error("The model returned an empty response. Try asking differently.", icon="🤨")
    return answer, sources


def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered", initial_sidebar_state="collapsed")
    st.markdown(CSS, unsafe_allow_html=True)

    st.markdown(
        '<div class="cyber-title">CYBERRESAI</div>'
        '<div class="cyber-sub">// MITRE ATT&CK Defense Intelligence</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    ready = check_environment()

    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"], msg.get("sources"))

    if prompt := st.chat_input("Ask about a technique, e.g. 'How does an attacker dump credentials?'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_message("user", prompt)

        if ready:
            answer, sources = ask(prompt)
            if answer:
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
                render_message("assistant", answer, sources)
        else:
            st.info("Fix the environment issues above, then send your question again.", icon="🔧")

    if not st.session_state.messages:
        render_message("assistant", DEFAULT_WELCOME, avatar=False)
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