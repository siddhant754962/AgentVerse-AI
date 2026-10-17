import html
import json

import time

from datetime import datetime

from urllib.parse import urlparse



import streamlit as st



from graph.workflow import research_workflow, MAX_RESEARCH_ATTEMPTS





# ==================================================

# PAGE CONFIGURATION

# ==================================================



st.set_page_config(

    page_title="AgentVerse AI",

    page_icon="🔎",

    layout="wide",

    initial_sidebar_state="expanded",

)





# ==================================================

# DESIGN SYSTEM

# Dark evidence desk, light "paper" report.

# Verdict colours carry meaning everywhere they appear.

# ==================================================



CSS = """

<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap');



:root {

    --bg: #0d1218;

    --panel: #141b24;

    --panel-2: #19222d;

    --line: #243040;

    --text: #e7ecf3;

    --muted: #8a97a8;

    --accent: #7aa2ff;

    --verified: #3ecf8e;

    --disputed: #f0b429;

    --false: #ef5b5b;

    --unverified: #8a97a8;

    --paper: #f6f7f9;

    --paper-ink: #1b2230;

    --serif: 'Newsreader', Georgia, serif;

    --sans: 'Manrope', system-ui, sans-serif;

}



html, body, .stApp, [data-testid="stAppViewContainer"] {

    background: var(--bg);

    color: var(--text);

    font-family: var(--sans);

}



#MainMenu, footer { visibility: hidden; }

[data-testid="stHeader"] { background: transparent; }



.block-container {

    max-width: 1180px;

    padding-top: 2.2rem;

    padding-bottom: 5rem;

}



h1, h2, h3, h4 { font-family: var(--serif); letter-spacing: -0.01em; color: var(--text); }



/* ---------- Sidebar ---------- */

[data-testid="stSidebar"] {

    background: #0a0f14;

    border-right: 1px solid var(--line);

}

.side-brand { font-family: var(--serif); font-size: 24px; font-weight: 600; margin: 4px 0 2px; }

.side-sub { color: var(--muted); font-size: 13px; margin-bottom: 8px; }

.side-h { font-weight: 700; font-size: 13px; color: var(--muted); margin: 18px 0 8px; }

.side-step { display: flex; gap: 10px; align-items: baseline; font-size: 14px; padding: 5px 0; color: var(--text); }

.side-step b { color: var(--accent); font-weight: 700; width: 14px; }

.kb-pill {

    display: inline-block; padding: 4px 10px; border-radius: 999px;

    background: var(--panel-2); border: 1px solid var(--line);

    font-size: 12px; color: var(--muted); margin-top: 6px;

}

[data-testid="stFileUploaderDropzone"] {

    background: var(--panel); border: 1px dashed #34445a; border-radius: 12px;

}



/* ---------- Hero ---------- */

.hero {

    position: relative;

    padding: 38px 40px 34px;

    border: 1px solid var(--line);

    border-radius: 16px;

    margin-bottom: 26px;

    background:

        linear-gradient(rgba(122,162,255,.045) 1px, transparent 1px) 0 0 / 100% 28px,

        linear-gradient(90deg, rgba(122,162,255,.045) 1px, transparent 1px) 0 0 / 28px 100%,

        linear-gradient(135deg, #131c28, #10161f);

}

.hero-brand { font-weight: 700; font-size: 14px; color: var(--accent); margin-bottom: 14px; }

.hero h1 {

    font-family: var(--serif); font-weight: 500; font-size: 48px; line-height: 1.08;

    margin: 0 0 14px; color: #f2f5fa; max-width: 16ch;

}

.hero p { color: var(--muted); font-size: 17px; line-height: 1.6; max-width: 60ch; margin: 0; }



/* ---------- Inputs ---------- */

[data-testid="stTextArea"] textarea {

    background: #0f151d; color: var(--text);

    border: 1px solid var(--line); border-radius: 12px;

    font-family: var(--sans); font-size: 16px; padding: 14px 16px;

}

[data-testid="stTextArea"] textarea:focus {

    border-color: var(--accent); box-shadow: 0 0 0 3px rgba(122,162,255,.18);

}

[data-testid="stTextArea"] label p { font-weight: 700; color: var(--text); }



button[data-testid="stBaseButton-primary"] {

    background: var(--accent); color: #0b1020; border: 0; border-radius: 10px;

    min-height: 46px; font-weight: 800; font-family: var(--sans);

}

button[data-testid="stBaseButton-primary"]:hover { background: #95b4ff; color: #0b1020; border: 0; }

button[data-testid="stBaseButton-secondary"] {

    background: var(--panel); color: var(--muted); border: 1px solid var(--line);

    border-radius: 10px; font-size: 13px; font-weight: 600; text-align: left;

}

button[data-testid="stBaseButton-secondary"]:hover { color: var(--text); border-color: var(--accent); background: var(--panel-2); }

:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }



/* ---------- Pipeline tracker ---------- */

.track { display: flex; margin: 10px 0 6px; }

.stage { flex: 1; position: relative; padding-right: 14px; }

.stage:not(:last-child)::after {

    content: ""; position: absolute; top: 17px; left: 44px; right: 8px; height: 2px; background: var(--line);

}

.stage.s-completed:not(:last-child)::after { background: var(--verified); }

.node {

    position: relative; width: 36px; height: 36px; border-radius: 50%;

    display: grid; place-items: center; font-weight: 800; font-size: 14px;

    background: var(--bg); border: 2px solid var(--line); color: var(--muted);

    margin-bottom: 12px;

}

.s-completed .node { border-color: var(--verified); color: var(--verified); background: rgba(62,207,142,.1); }

.s-running .node { border-color: rgba(122,162,255,.3); color: var(--accent); }

.ring {

    position: absolute; inset: -2px; border-radius: 50%;

    border: 2px solid transparent; border-top-color: var(--accent);

    animation: spin 0.9s linear infinite;

}

@keyframes spin { to { transform: rotate(360deg); } }

.stage-name { font-weight: 700; font-size: 15px; color: var(--text); }

.stage-desc { font-size: 13px; color: var(--muted); margin-top: 3px; line-height: 1.45; }

.stage-detail { font-size: 12px; margin-top: 8px; font-weight: 700; color: var(--verified); min-height: 16px; }

.s-running .stage-detail { color: var(--accent); }

.s-waiting .stage-name { color: var(--muted); }

.loopback {

    margin: 14px 0 0; padding: 10px 14px; border-radius: 10px; font-size: 14px;

    background: rgba(240,180,41,.08); border: 1px solid rgba(240,180,41,.35); color: #f5cf6b;

}



/* ---------- Activity feed ---------- */

.feed { border-left: 2px solid var(--line); margin: 8px 0 0 6px; padding-left: 18px; }

.feed-item { position: relative; padding: 0 0 16px; }

.feed-item::before {

    content: ""; position: absolute; left: -25px; top: 6px; width: 10px; height: 10px;

    border-radius: 50%; background: var(--accent); border: 2px solid var(--bg);

}

.feed-time { font-size: 12px; color: var(--muted); font-variant-numeric: tabular-nums; }

.feed-agent { font-weight: 700; font-size: 14px; margin: 1px 0 2px; }

.feed-msg { font-size: 14px; color: #b9c4d3; line-height: 1.5; }



/* ---------- Verdict summary ---------- */

.verdict-head { font-family: var(--serif); font-size: 40px; font-weight: 500; line-height: 1.15; margin: 4px 0 6px; color: #f2f5fa; }

.verdict-sub { color: var(--muted); font-size: 15px; margin-bottom: 18px; }

.vbar { display: flex; height: 12px; border-radius: 999px; overflow: hidden; gap: 3px; background: var(--panel); }

.vbar i { display: block; min-width: 8px; }

.legend { display: flex; flex-wrap: wrap; gap: 18px; margin: 12px 0 0; font-size: 13px; color: var(--muted); }

.legend span { display: inline-flex; align-items: center; gap: 7px; }

.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }

.facts { display: flex; flex-wrap: wrap; gap: 0; margin: 26px 0 8px; border-top: 1px solid var(--line); }

.fact { flex: 1; min-width: 150px; padding: 16px 0 6px; }

.fact b { display: block; font-family: var(--serif); font-size: 30px; font-weight: 500; color: #f2f5fa; }

.fact span { font-size: 13px; color: var(--muted); }



.v-verified   { --vc: var(--verified); }

.v-disputed   { --vc: var(--disputed); }

.v-false      { --vc: var(--false); }

.v-unverified { --vc: var(--unverified); }



/* ---------- Claim cards ---------- */

.claim {

    background: var(--panel); border: 1px solid var(--line);

    border-left: 4px solid var(--vc); border-radius: 12px;

    padding: 18px 20px; margin-bottom: 14px;

}

.claim-top { display: flex; justify-content: space-between; gap: 18px; align-items: flex-start; }

.claim-text { font-family: var(--serif); font-size: 19px; line-height: 1.45; color: #f0f3f8; }

.stamp {

    flex-shrink: 0; padding: 4px 11px; border: 1.5px solid var(--vc); color: var(--vc);

    border-radius: 6px; font-weight: 800; font-size: 13px; transform: rotate(-2.5deg);

    background: color-mix(in srgb, var(--vc) 10%, transparent); white-space: nowrap;

}

.conf { display: flex; align-items: center; gap: 12px; margin: 14px 0 2px; font-size: 13px; color: var(--muted); }

.conf-bar { flex: 1; max-width: 240px; height: 6px; background: var(--panel-2); border-radius: 999px; overflow: hidden; }

.conf-bar i { display: block; height: 100%; background: var(--vc); border-radius: 999px; }

.conf b { color: var(--text); font-variant-numeric: tabular-nums; }

.evidence { margin-top: 12px; font-size: 14px; line-height: 1.6; color: #b9c4d3; }

.srcs { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; }

.srcs a, .srcs em {

    font-size: 12px; font-style: normal; font-weight: 600; text-decoration: none;

    padding: 4px 10px; border-radius: 999px; background: var(--panel-2); border: 1px solid var(--line); color: var(--accent);

}

.srcs em { color: var(--muted); }

.srcs a:hover { border-color: var(--accent); }



/* ---------- Source cards ---------- */

.src-card { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; margin-bottom: 12px; }

.src-domain { font-size: 12px; font-weight: 700; color: var(--muted); }

.src-title { font-family: var(--serif); font-size: 18px; margin: 4px 0 6px; }

.src-title a { color: #f0f3f8; text-decoration: none; }

.src-title a:hover { color: var(--accent); }

.src-snip { font-size: 14px; color: #b9c4d3; line-height: 1.55; }

.quote { border-left: 3px solid var(--accent); padding: 4px 0 4px 16px; margin-bottom: 16px; font-family: var(--serif); font-size: 17px; line-height: 1.6; color: #d6deea; }

.quote small { display: block; font-family: var(--sans); font-size: 12px; color: var(--muted); margin-top: 6px; }

.kb-answer { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; margin-bottom: 18px; font-size: 15px; line-height: 1.65; color: #cfd8e5; }



/* ---------- Report paper ---------- */

.st-key-report_paper {

    background: var(--paper); border-radius: 8px; padding: 46px 56px;

    box-shadow: 0 24px 60px rgba(0,0,0,.45); margin-top: 10px;

}

.paper-title { font-family: var(--serif); font-size: 34px; font-weight: 600; line-height: 1.2; color: var(--paper-ink); margin: 0 0 8px; }

.paper-meta { font-family: var(--sans); font-size: 13px; color: #5d6878; padding-bottom: 20px; margin-bottom: 26px; border-bottom: 2px solid var(--paper-ink); }

.st-key-report_paper p, .st-key-report_paper li {

    font-family: var(--serif); font-size: 18px; line-height: 1.75; color: var(--paper-ink); max-width: 72ch;

}

.st-key-report_paper h1, .st-key-report_paper h2, .st-key-report_paper h3, .st-key-report_paper h4 {

    font-family: var(--serif); color: var(--paper-ink); font-weight: 600;

}

.st-key-report_paper h2 { font-size: 26px; margin-top: 1.6em; }

.st-key-report_paper h3 { font-size: 21px; }

.st-key-report_paper strong, .st-key-report_paper em, .st-key-report_paper td, .st-key-report_paper th { color: var(--paper-ink); }

.st-key-report_paper a { color: #2456c7; }

.st-key-report_paper code { background: #e6e9ee; color: #1b2230; border-radius: 4px; padding: 1px 5px; }

.st-key-report_paper blockquote { border-left: 3px solid #b6c0cf; color: #4a5568; }



/* ---------- Tabs / progress / misc ---------- */

[data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--line); }

button[data-baseweb="tab"] { color: var(--muted); font-weight: 700; font-family: var(--sans); }

button[data-baseweb="tab"][aria-selected="true"] { color: var(--text); }

[data-baseweb="tab-highlight"] { background: var(--accent); }

div[data-testid="stProgressBar"] > div > div { background: var(--accent); }

.empty { padding: 28px; border: 1px dashed var(--line); border-radius: 12px; color: var(--muted); text-align: center; }



@media (max-width: 760px) {

    .hero { padding: 26px 22px; }

    .hero h1 { font-size: 34px; }

    .track { flex-direction: column; gap: 18px; }

    .stage::after { display: none; }

    .claim-top { flex-direction: column; }

    .verdict-head { font-size: 30px; }

    .st-key-report_paper { padding: 26px 22px; }

}

@media (prefers-reduced-motion: reduce) { .ring { animation: none; } }

</style>

"""



st.markdown(CSS, unsafe_allow_html=True)





# ==================================================

# CONFIGURATION

# ==================================================



AGENTS = {

    "research": {

        "title": "Research",

        "description": "Searches the web for sources",

    },

    "rag": {

        "title": "Retrieval",

        "description": "Pulls passages from your documents",

    },

    "fact_checker": {

        "title": "Fact check",

        "description": "Tests each claim against the evidence",

    },

    "report": {

        "title": "Report",

        "description": "Writes the final report",

    },

}



NEXT_AGENT = {

    "research": "rag",

    "rag": "fact_checker",

    "report": None,

}



VERDICTS = {

    "verified": {"label": "Verified", "icon": "✓", "color": "var(--verified)"},

    "disputed": {"label": "Disputed", "icon": "!", "color": "var(--disputed)"},

    "false": {"label": "False", "icon": "✕", "color": "var(--false)"},

    "unverified": {"label": "Unverified", "icon": "?", "color": "var(--unverified)"},

}



EXAMPLE_QUERIES = [

    "How is generative AI changing healthcare in 2026?",

    "Does intermittent fasting improve longevity?",

    "What is the real effect of remote work on productivity?",

]



CHECK_SVG = (

    '<svg viewBox="0 0 16 16" width="15" height="15"><path d="M3 8.5l3.2 3L13 4.8" '

    'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '

    'stroke-linejoin="round"/></svg>'

)





# ==================================================

# HELPERS: SAFE HTML + DATA NORMALISATION

# The workflow's output shape isn't fixed, so every

# reader below accepts several common key names.

# ==================================================



def esc(value):

    return html.escape(str(value), quote=True)





def render_html(markup):

    st.markdown(markup, unsafe_allow_html=True)





def domain_of(url):

    try:

        host = urlparse(url).netloc.lower()

        return host[4:] if host.startswith("www.") else host

    except Exception:

        return ""





def first_value(data, keys, default=None):

    for key in keys:

        value = data.get(key)

        if value not in (None, "", [], {}):

            return value

    return default





def normalize_verdict(value):

    if isinstance(value, bool):

        return "verified" if value else "unverified"



    text = str(value or "").strip().lower().replace("_", " ").replace("-", " ")



    if any(k in text for k in ("partial", "mixed", "disput", "misleading", "conflict", "outdated", "exaggerat", "unclear")):

        return "disputed"

    if any(k in text for k in ("not true", "false", "refut", "incorrect", "contradict", "wrong", "debunk", "fabricat")):

        return "false"

    if any(k in text for k in ("unverif", "not verif", "unsupported", "not supported", "insufficient", "no evidence", "unknown")):

        return "unverified"

    if any(k in text for k in ("verif", "support", "true", "correct", "confirm", "accurate", "valid")):

        return "verified"

    return "unverified"





def normalize_confidence(value):

    if value is None:

        return None



    if isinstance(value, str):

        word = value.strip().lower().rstrip("%")

        words = {"high": 85, "medium": 60, "moderate": 60, "low": 30}

        if word in words:

            return words[word]

        value = word



    try:

        number = float(value)

    except (TypeError, ValueError):

        return None



    if number <= 1:

        number *= 100



    return int(max(0, min(100, round(number))))





def collect_sources(value):

    """Return a list of (label, url_or_None)."""

    found = []



    if isinstance(value, str):

        if value.startswith(("http://", "https://")):

            found.append((domain_of(value) or value, value))

        elif value.strip():

            found.append((value.strip(), None))



    elif isinstance(value, dict):

        url = first_value(value, ["url", "link", "href"])

        label = first_value(value, ["title", "name", "source"]) or (domain_of(url) if url else None)

        if label:

            safe_url = url if isinstance(url, str) and url.startswith(("http://", "https://")) else None

            found.append((str(label), safe_url))



    elif isinstance(value, (list, tuple)):

        for item in value:

            found.extend(collect_sources(item))



    return found





def normalize_claim(raw):
   
  if isinstance(raw, str):
    try:
        parsed = json.loads(raw)

        if isinstance(parsed, dict):
            raw = parsed
        else:
            return {
                "text": raw,
                "verdict": "unverified",
                "confidence": None,
                "evidence": "",
                "sources": [],
            }

    except (json.JSONDecodeError, TypeError):
        return {
            "text": raw,
            "verdict": "unverified",
            "confidence": None,
            "evidence": "",
            "sources": [],
        }

    if not isinstance(raw, dict):
        return {
            "text": str(raw),
            "verdict": "unverified",
            "confidence": None,
            "evidence": "",
            "sources": [],
        }

    verdict_raw = first_value(
        raw,
        ["verdict", "status", "result", "label", "verified", "is_verified", "supported"],
    )

    sources = []
    for key in ("sources", "source", "urls", "url", "references"):
        if key in raw:
            sources.extend(collect_sources(raw[key]))

    return {
        "text": str(first_value(raw, ["claim", "statement", "text", "assertion"], "Untitled claim")),
        "verdict": normalize_verdict(verdict_raw),
        "confidence": normalize_confidence(
            first_value(raw, ["confidence", "confidence_score", "score"])
        ),
        "evidence": str(
            first_value(
                raw,
                ["evidence", "reasoning", "reason", "explanation", "justification", "notes", "rationale"],
                "",
            )
        ),
        "sources": sources,
    }

def normalize_web_result(raw):

    if isinstance(raw, str):

        return {"title": raw[:90], "url": "", "snippet": raw}



    if not isinstance(raw, dict):

        return {"title": str(raw)[:90], "url": "", "snippet": ""}



    url = first_value(raw, ["url", "link", "href"], "")



    return {

        "title": str(first_value(raw, ["title", "name"], domain_of(url) or "Untitled source")),

        "url": url if isinstance(url, str) and url.startswith(("http://", "https://")) else "",

        "snippet": str(first_value(raw, ["content", "snippet", "description", "text", "summary"], "")),

    }





def normalize_context(raw):

    if isinstance(raw, str):

        return {"text": raw, "source": ""}



    if isinstance(raw, dict):

        metadata = raw.get("metadata") if isinstance(raw.get("metadata"), dict) else {}

        return {

            "text": str(first_value(raw, ["page_content", "content", "text", "chunk"], "")),

            "source": str(first_value(metadata, ["source", "file", "filename"], first_value(raw, ["source"], ""))),

        }



    text = getattr(raw, "page_content", None)

    if text is not None:

        metadata = getattr(raw, "metadata", {}) or {}

        return {"text": str(text), "source": str(metadata.get("source", ""))}



    return {"text": str(raw), "source": ""}





def shorten(text, limit):

    text = " ".join(str(text).split())

    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"





# ==================================================

# SIDEBAR

# ==================================================



if "kb_added" not in st.session_state:

    st.session_state["kb_added"] = []



with st.sidebar:

    render_html(

        '<div class="side-brand">AgentVerse AI</div>'

        '<div class="side-sub">Multi-agent research workspace</div>'

    )



    render_html('<div class="side-h">Knowledge base</div>')



    uploaded_files = st.file_uploader(

        "Upload documents for retrieval",

        type=["pdf", "txt", "md"],

        accept_multiple_files=True,

        help="Add PDFs or text files. Agents will cite them alongside web sources.",

    )



    if uploaded_files:

        st.caption(f"{len(uploaded_files)} document(s) selected")



        if st.button("Add to knowledge base", use_container_width=True):

            from io import BytesIO



            from pypdf import PdfReader



            # Import your existing ingestion function.

            from rag.ingest import ingest_text



            success_count = 0



            for uploaded_file in uploaded_files:

                try:

                    if uploaded_file.name.lower().endswith(".pdf"):

                        reader = PdfReader(BytesIO(uploaded_file.getvalue()))

                        text = "\n".join(

                            page.extract_text() or "" for page in reader.pages

                        )

                    else:

                        text = uploaded_file.getvalue().decode("utf-8", errors="replace")



                    if not text.strip():

                        st.warning(f"No extractable text found in {uploaded_file.name}")

                        continue



                    # Check the signature of ingest_text in your

                    # existing rag/ingest.py before using this call.

                    ingest_text(text, source=uploaded_file.name)



                    success_count += 1

                    st.session_state["kb_added"].append(uploaded_file.name)

                    st.success(f"Added {uploaded_file.name}")



                except Exception as exc:

                    st.error(f"Could not process {uploaded_file.name}: {exc}")



            if success_count:

                st.success(f"{success_count} document(s) added to the knowledge base.")



    if st.session_state["kb_added"]:

        render_html(

            f'<span class="kb-pill">{len(st.session_state["kb_added"])} document(s) added this session</span>'

        )



    render_html('<div class="side-h">How a check runs</div>')

    render_html(

        '<div class="side-step"><b>1</b>Research the web</div>'

        '<div class="side-step"><b>2</b>Retrieve from your documents</div>'

        '<div class="side-step"><b>3</b>Verify each claim</div>'

        '<div class="side-step"><b>4</b>Write the report</div>'

    )



    st.divider()

    st.caption("Built with LangGraph and Streamlit")





# ==================================================

# HERO + QUERY

# ==================================================



render_html(

    '<div class="hero">'

    '<div class="hero-brand">AgentVerse AI</div>'

    "<h1>Every claim, checked before it is written.</h1>"

    "<p>Four agents search the web, read your documents, test each claim "

    "against the evidence, then write the report. Follow every step as it happens.</p>"

    "</div>"

)



if "query" not in st.session_state:

    st.session_state["query"] = ""





def use_example(text):

    st.session_state["query"] = text





query = st.text_area(

    "What do you want to investigate?",

    key="query",

    placeholder="Example: How is generative AI changing healthcare in 2026?",

    height=110,

)



chip_columns = st.columns(len(EXAMPLE_QUERIES))

for column, example in zip(chip_columns, EXAMPLE_QUERIES):

    column.button(

        example,

        key=f"chip_{example}",

        on_click=use_example,

        args=(example,),

        use_container_width=True,

    )



start_research = st.button(

    "Start fact-checked research",

    type="primary",

    use_container_width=True,

)





# ==================================================

# WORKFLOW VISUALISATION

# ==================================================



def render_agents(statuses, details, attempts=0):

    stages = []



    for index, (node, agent) in enumerate(AGENTS.items(), start=1):

        status = statuses[node]



        if status == "completed":

            marker = CHECK_SVG

            ring = ""

        elif status == "running":

            marker = str(index)

            ring = '<span class="ring"></span>'

        else:

            marker = str(index)

            ring = ""



        detail = details.get(node, "")

        if status == "running" and not detail:

            detail = "Working…"



        stages.append(

            f'<div class="stage s-{status}">'

            f'<div class="node">{ring}{marker}</div>'

            f'<div class="stage-name">{esc(agent["title"])}</div>'

            f'<div class="stage-desc">{esc(agent["description"])}</div>'

            f'<div class="stage-detail">{esc(detail)}</div>'

            "</div>"

        )



    markup = f'<div class="track">{"".join(stages)}</div>'



    if attempts > 1 and statuses["report"] != "completed":

        markup += (

            f'<div class="loopback">The fact checker asked for more evidence. '

            f"Research pass {attempts} of {MAX_RESEARCH_ATTEMPTS}.</div>"

        )



    render_html(markup)





def render_feed(entries):

    if not entries:

        return



    items = "".join(

        '<div class="feed-item">'

        f'<div class="feed-time">{esc(entry["time"])}</div>'

        f'<div class="feed-agent">{esc(entry["agent"])}</div>'

        f'<div class="feed-msg">{esc(entry["message"])}</div>'

        "</div>"

        for entry in entries[:10]

    )



    render_html(f'<div class="feed">{items}</div>')





def next_node_after_fact_check(state):

    """Match the conditional routing in workflow.py."""



    needs_more_research = state.get("needs_more_research", False)

    attempts = state.get("research_attempts", 0)



    if needs_more_research and attempts < MAX_RESEARCH_ATTEMPTS:

        return "research"



    return "report"





def describe_update(node, update):

    if node == "research":

        results = update.get("web_results", [])

        attempts = update.get("research_attempts", 0)

        return f"Finished search pass {attempts} and found {len(results)} web results."



    if node == "rag":

        context = update.get("retrieved_context", [])

        return f"Pulled {len(context)} passage(s) from the knowledge base."



    if node == "fact_checker":

        claims = update.get("verified_claims", [])

        needs_more = update.get("needs_more_research", False)



        if needs_more:

            return f"Checked {len(claims)} claim(s). Some lacked evidence, so another search pass was requested."



        return f"Checked {len(claims)} claim(s) against the collected evidence."



    if node == "report":

        return "Report written and ready to read."



    return f"{node} finished."





def stage_detail(node, state):

    if node == "research":

        return f'{len(state.get("web_results", []))} results'

    if node == "rag":

        return f'{len(state.get("retrieved_context", []))} passages'

    if node == "fact_checker":

        return f'{len(state.get("verified_claims", []))} claims checked'

    if node == "report":

        return "Ready"

    return ""





# ==================================================

# RUN THE LANGGRAPH WORKFLOW

# ==================================================



if start_research:



    if not query.strip():

        st.warning("Enter a research question to begin.")



    else:

        state = {

            "query": query.strip(),

            "research_results": [],

            "web_results": [],

            "retrieved_context": [],

            "rag_answer": "",

            "verified_claims": [],

            "final_report": "",

            "needs_more_research": False,

            "research_attempts": 0,

        }



        statuses = {node: "waiting" for node in AGENTS}

        details = {}

        activity_log = []

        completed_nodes = set()

        started_at = time.time()



        st.divider()

        st.subheader("Live workflow")



        workflow_placeholder = st.empty()

        progress_bar = st.progress(0)

        status_message = st.empty()

        activity_placeholder = st.empty()



        statuses["research"] = "running"



        try:

            with workflow_placeholder.container():

                render_agents(statuses, details)



            status_message.info("Research agent is searching the web…")



            for event in research_workflow.stream(state, stream_mode="updates"):

                for node, update in event.items():



                    if node not in AGENTS:

                        continue



                    update = update if isinstance(update, dict) else {}

                    state.update(update)



                    statuses[node] = "completed"

                    completed_nodes.add(node)

                    details[node] = stage_detail(node, state)



                    activity_log.insert(

                        0,

                        {

                            "time": datetime.now().strftime("%H:%M:%S"),

                            "agent": AGENTS[node]["title"],

                            "message": describe_update(node, update),

                        },

                    )



                    if node == "fact_checker":

                        next_node = next_node_after_fact_check(state)

                    else:

                        next_node = NEXT_AGENT.get(node)



                    if next_node == "research":

                        # The fact checker wants more evidence: rewind the tracker.

                        for loop_node in ("research", "rag", "fact_checker"):

                            statuses[loop_node] = "waiting"

                            details[loop_node] = ""

                            completed_nodes.discard(loop_node)



                    if next_node:

                        statuses[next_node] = "running"



                    with workflow_placeholder.container():

                        render_agents(

                            statuses,

                            details,

                            state.get("research_attempts", 0),

                        )



                    progress_bar.progress(len(completed_nodes) / len(AGENTS))



                    with activity_placeholder.container():

                        st.markdown("#### Activity")

                        render_feed(activity_log)



                    if next_node:

                        status_message.info(

                            f"{AGENTS[next_node]['title']} agent is working…"

                        )



            for node in AGENTS:

                statuses[node] = "completed"



            with workflow_placeholder.container():

                render_agents(statuses, details)



            progress_bar.progress(1.0)



            elapsed = int(time.time() - started_at)

            status_message.success(f"Research complete in {elapsed}s.")



            st.session_state["latest_research_state"] = state



        except Exception as exc:

            status_message.error(

                "The workflow stopped before finishing. "

                "Check the terminal for the full traceback."

            )

            st.exception(exc)





# ==================================================

# RESULTS

# ==================================================



def render_claims_tab(claims):

    if not claims:

        render_html(

            '<div class="empty">The fact checker returned no claims. '

            "The report was written without claim-level verification.</div>"

        )

        return



    counts = {key: sum(1 for c in claims if c["verdict"] == key) for key in VERDICTS}



    options = ["all"] + [key for key in VERDICTS if counts[key]]



    def option_label(key):

        if key == "all":

            return f"All ({len(claims)})"

        return f"{VERDICTS[key]['label']} ({counts[key]})"



    selected = st.radio(

        "Filter claims",

        options,

        format_func=option_label,

        horizontal=True,

        label_visibility="collapsed",

    )



    shown = claims if selected == "all" else [c for c in claims if c["verdict"] == selected]



    for claim in shown:

        verdict = VERDICTS[claim["verdict"]]



        confidence_html = ""

        if claim["confidence"] is not None:

            confidence_html = (

                '<div class="conf"><span>Confidence</span>'

                f'<div class="conf-bar"><i style="width:{claim["confidence"]}%"></i></div>'

                f'<b>{claim["confidence"]}%</b></div>'

            )



        evidence_html = (

            f'<div class="evidence">{esc(claim["evidence"])}</div>'

            if claim["evidence"]

            else ""

        )



        source_chips = []

        for label, url in claim["sources"][:5]:

            if url:

                source_chips.append(

                    f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(shorten(label, 40))}</a>'

                )

            else:

                source_chips.append(f"<em>{esc(shorten(label, 40))}</em>")



        sources_html = f'<div class="srcs">{"".join(source_chips)}</div>' if source_chips else ""



        render_html(

            f'<div class="claim v-{claim["verdict"]}">'

            '<div class="claim-top">'

            f'<div class="claim-text">{esc(claim["text"])}</div>'

            f'<div class="stamp">{verdict["icon"]} {verdict["label"]}</div>'

            "</div>"

            f"{confidence_html}{evidence_html}{sources_html}"

            "</div>"

        )





def render_sources_tab(web_results):

    if not web_results:

        render_html('<div class="empty">No web sources were collected.</div>')

        return



    for item in web_results:

        domain = domain_of(item["url"]) or "Source"

        title = esc(shorten(item["title"], 110))



        title_html = (

            f'<a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{title}</a>'

            if item["url"]

            else title

        )



        snippet_html = (

            f'<div class="src-snip">{esc(shorten(item["snippet"], 260))}</div>'

            if item["snippet"]

            else ""

        )



        render_html(

            '<div class="src-card">'

            f'<div class="src-domain">{esc(domain)}</div>'

            f'<div class="src-title">{title_html}</div>'

            f"{snippet_html}"

            "</div>"

        )





def render_context_tab(context_items, rag_answer):

    if rag_answer:

        render_html(

            '<div class="kb-answer"><b>Answer from your documents</b><br>'

            f"{esc(rag_answer)}</div>"

        )



    if not context_items:

        render_html(

            '<div class="empty">No passages were retrieved. '

            "Add documents in the sidebar to ground answers in your own material.</div>"

        )

        return



    for item in context_items:

        source_html = f'<small>{esc(item["source"])}</small>' if item["source"] else ""

        render_html(

            f'<div class="quote">{esc(shorten(item["text"], 600))}{source_html}</div>'

        )





if "latest_research_state" in st.session_state:



    result = st.session_state["latest_research_state"]



    claims = [normalize_claim(c) for c in result.get("verified_claims", [])]

    web_results = [normalize_web_result(r) for r in result.get("web_results", [])]

    context_items = [normalize_context(c) for c in result.get("retrieved_context", [])]



    counts = {key: sum(1 for c in claims if c["verdict"] == key) for key in VERDICTS}

    total = len(claims)



    st.divider()



    # ---------- Verdict summary ----------

    if total:

        headline = f'{counts["verified"]} of {total} claims hold up.'



        notes = []

        if counts["disputed"]:

            notes.append(f'{counts["disputed"]} disputed')

        if counts["false"]:

            notes.append(f'{counts["false"]} false')

        if counts["unverified"]:

            notes.append(f'{counts["unverified"]} unverified')



        sub = (", ".join(notes).capitalize() + ". ") if notes else "Nothing was disputed. "

        sub += f"Checked against {len(web_results)} web source(s)."



        segments = "".join(

            f'<i style="flex:{counts[key]};background:{VERDICTS[key]["color"]}"></i>'

            for key in VERDICTS

            if counts[key]

        )



        legend = "".join(

            f'<span><b class="dot" style="background:{VERDICTS[key]["color"]}"></b>'

            f'{counts[key]} {VERDICTS[key]["label"].lower()}</span>'

            for key in VERDICTS

            if counts[key]

        )



        render_html(

            f'<div class="verdict-head">{esc(headline)}</div>'

            f'<div class="verdict-sub">{esc(sub)}</div>'

            f'<div class="vbar">{segments}</div>'

            f'<div class="legend">{legend}</div>'

        )

    else:

        render_html(

            '<div class="verdict-head">No claims were extracted.</div>'

            '<div class="verdict-sub">The report below was written without claim-level verification.</div>'

        )



    render_html(

        '<div class="facts">'

        f'<div class="fact"><b>{len(web_results)}</b><span>Web sources</span></div>'

        f'<div class="fact"><b>{len(context_items)}</b><span>Passages from your documents</span></div>'

        f'<div class="fact"><b>{total}</b><span>Claims checked</span></div>'

        f'<div class="fact"><b>{result.get("research_attempts", 0)}</b><span>Research passes</span></div>'

        "</div>"

    )



    # ---------- Tabs ----------

    tab_report, tab_claims, tab_sources, tab_context = st.tabs(

        [

            "Report",

            f"Claims ({total})",

            f"Sources ({len(web_results)})",

            f"Your documents ({len(context_items)})",

        ]

    )



    with tab_report:

        report = result.get("final_report", "")



        if report:

            st.download_button(

                "Download report (Markdown)",

                data=report,

                file_name="agentverse_research_report.md",

                mime="text/markdown",

            )



            with st.container(key="report_paper"):

                render_html(

                    f'<div class="paper-title">{esc(result.get("query", "Research report"))}</div>'

                    f'<div class="paper-meta">Prepared {datetime.now().strftime("%d %B %Y")}. '

                    f"{total} claim(s) reviewed against {len(web_results)} web source(s).</div>"

                )

                st.markdown(report)

        else:

            st.warning("The workflow finished without returning a report.")



    with tab_claims:

        render_claims_tab(claims)



        with st.expander("Raw fact-checker output"):

            st.json(result.get("verified_claims", []))



    with tab_sources:

        render_sources_tab(web_results)



    with tab_context:

        render_context_tab(context_items, result.get("rag_answer", ""))
