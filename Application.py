from __future__ import annotations

import html
import re
from collections import Counter

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="OratorPulse — Speech Detective",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# RUBBER-HOSE-INSPIRED CARTOON STYLING
# CSS must remain inside this triple-quoted string.
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&family=Fredoka:wght@400;500;600;700&family=Special+Elite&display=swap');

:root {
    --ink: #171717;
    --cream: #f7f0df;
    --paper: #fffaf0;
    --red: #e94f37;
    --teal: #62c8bd;
    --blue: #79bce8;
    --orange: #f49a48;
    --muted: #675f54;
}

html, body, [data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] *,
[data-testid="stSidebar"] *,
button, input, textarea, label {
    font-family: 'Fredoka', 'Trebuchet MS', sans-serif !important;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: var(--cream) !important;
    color: var(--ink) !important;
}

/* No dotted wallpaper: a clean, warm paper background */
[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1160px;
    padding: 2rem 2rem 4rem;
}

h1, h2, h3, h4 {
    font-family: 'Bowlby One SC', 'Fredoka', sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: .3px !important;
    color: var(--ink) !important;
}

h1 { font-size: clamp(2.4rem, 5vw, 4.3rem) !important; }
h2 { font-size: 2rem !important; }
h3 { font-size: 1.35rem !important; }

p, li, label, small, input, textarea {
    font-family: 'Fredoka', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #e8ded0 !important;
    border-right: 3px solid var(--ink);
    box-shadow: 5px 0 0 var(--ink);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Bowlby One SC', sans-serif !important;
}

.hero {
    position: relative;
    overflow: hidden;
    background: var(--red);
    color: var(--paper);
    border: 4px solid var(--ink);
    border-radius: 48px 35px 45px 32px;
    padding: 32px 35px;
    box-shadow: 8px 8px 0 var(--ink);
    margin: 10px 0 30px;
    transform: rotate(-.25deg);
}

.hero:after {
    content: "★";
    position: absolute;
    right: 28px;
    bottom: 8px;
    font-size: 5rem;
    line-height: 1;
    color: var(--orange);
    -webkit-text-stroke: 3px var(--ink);
    transform: rotate(12deg);
}

.hero h1 {
    color: var(--paper) !important;
    text-shadow: 3px 3px 0 var(--ink);
    margin: 0 0 8px 0;
}

.hero p {
    color: var(--paper) !important;
    font-size: 1.06rem;
    max-width: 720px;
}

.hero-label {
    display: inline-block;
    color: var(--ink);
    background: var(--cream);
    border: 3px solid var(--ink);
    border-radius: 999px;
    padding: 6px 13px;
    font-family: 'Bowlby One SC', sans-serif !important;
    font-size: .8rem;
    margin-bottom: 13px;
    box-shadow: 3px 3px 0 var(--ink);
}

.cartoon-card {
    background: var(--paper);
    color: var(--ink);
    border: 3px solid var(--ink);
    border-radius: 28px 22px 30px 20px;
    padding: 22px;
    box-shadow: 5px 6px 0 var(--ink);
    margin: 12px 0 20px;
}

.card-red { background: #ffd1c7; }
.card-teal { background: #c8eee6; }
.card-blue { background: #d5eafa; }
.card-cream { background: #fffaf0; }
.card-orange { background: #ffdfbb; }

.big-number {
    font-family: 'Bowlby One SC', sans-serif !important;
    font-size: 2.8rem;
    line-height: 1.2;
}

.small-label {
    font-family: 'Bowlby One SC', sans-serif !important;
    font-size: .9rem;
    letter-spacing: .5px;
    text-transform: uppercase;
}

.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: var(--teal) !important;
    color: var(--ink) !important;
    border: 3px solid var(--ink) !important;
    border-radius: 18px 14px 19px 13px !important;
    min-height: 46px;
    font-weight: 700 !important;
    box-shadow: 4px 5px 0 var(--ink) !important;
    transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--orange) !important;
    color: var(--ink) !important;
    transform: translate(-2px, -2px) rotate(-.5deg);
    box-shadow: 6px 7px 0 var(--ink) !important;
    border-color: var(--ink) !important;
}

.stTextArea textarea,
.stTextInput input,
[data-testid="stChatInput"] textarea {
    background: var(--paper) !important;
    color: var(--ink) !important;
    border: 3px solid var(--ink) !important;
    border-radius: 20px !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
    font-family: 'Special Elite', 'Fredoka', monospace !important;
    font-size: 1.08rem !important;
}

[data-testid="stFileUploader"] section {
    background: var(--paper) !important;
    border: 3px dashed var(--ink) !important;
    border-radius: 20px !important;
}

[data-testid="stMetric"] {
    background: var(--paper);
    border: 3px solid var(--ink);
    border-radius: 23px 18px 24px 17px;
    padding: 15px;
    box-shadow: 4px 5px 0 var(--ink);
}

[data-testid="stMetricLabel"] {
    font-family: 'Bowlby One SC', sans-serif !important;
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Bowlby One SC', sans-serif !important;
    color: var(--ink) !important;
}

[data-testid="stChatMessage"] {
    background: var(--paper) !important;
    border: 3px solid var(--ink) !important;
    border-radius: 22px 18px 24px 17px !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
    padding: 12px;
    margin-bottom: 15px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 9px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: var(--paper);
    color: var(--ink);
    border: 3px solid var(--ink);
    border-radius: 16px 13px 18px 12px;
    padding: 10px 15px;
    font-family: 'Bowlby One SC', sans-serif !important;
    box-shadow: 3px 3px 0 var(--ink);
}

.stTabs [aria-selected="true"] {
    background: var(--teal) !important;
    color: var(--ink) !important;
}

[data-testid="stExpander"],
[data-testid="stAlert"] {
    background: var(--paper) !important;
    border: 3px solid var(--ink) !important;
    border-radius: 20px !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
}

[data-testid="stProgress"] > div {
    background: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 999px;
    padding: 3px;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--red), var(--orange), var(--teal));
    border-radius: 999px;
}

.pill {
    display: inline-block;
    background: var(--teal);
    color: var(--ink);
    border: 2px solid var(--ink);
    border-radius: 999px;
    padding: 6px 12px;
    font-weight: 700;
    box-shadow: 2px 3px 0 var(--ink);
    margin: 4px;
}

hr {
    border: none;
    border-top: 3px solid var(--ink);
    opacity: .22;
    margin: 26px 0;
}

footer { visibility: hidden; }

@media (max-width: 700px) {
    .block-container { padding: 1rem; }
    .hero { padding: 23px; }
    .hero:after { font-size: 3rem; right: 14px; }
    .cartoon-card { padding: 17px; }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# TEXT ANALYSIS — transparent heuristics, not an AI detector
# ============================================================

AI_STYLE_PHRASES = [
    "in conclusion", "it is important to note", "delve into",
    "furthermore", "moreover", "in today's world",
    "plays a crucial role", "comprehensive understanding",
    "multifaceted", "landscape of", "it is worth noting",
    "this highlights the importance", "not only that, but also",
    "in summary",
]

PERSONAL_MARKERS = [
    "i think", "i feel", "i believe", "in my experience",
    "i remember", "for me", "i learned", "i noticed",
    "my friend", "my family", "i tried", "i made a mistake",
    "i was", "i did", "i wanted", "i realized",
]


def split_sentences(text: str) -> list[str]:
    return [
        part.strip()
        for part in re.split(r"(?<=[.!?؟])\s+|\n+", text)
        if part.strip()
    ]


def analyze_text(text: str) -> dict:
    clean = text.strip()
    words = re.findall(r"\b[\w'-]+\b", clean.lower())
    sentences = split_sentences(clean)

    if not words:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "avg_sentence": 0,
            "ai_markers": [],
            "human_markers": [],
            "repeated_words": [],
            "score": 0,
            "assessment": "No text yet",
            "explanation": "Paste some text first.",
            "limitations": [],
        }

    counts = Counter(words)
    repeated = [
        (word, count)
        for word, count in counts.most_common()
        if len(word) > 4 and count >= 3
    ][:6]

    avg_sentence = len(words) / max(len(sentences), 1)
    lower = clean.lower()
    ai_found = [phrase for phrase in AI_STYLE_PHRASES if phrase in lower]
    personal_found = [phrase for phrase in PERSONAL_MARKERS if phrase in lower]

    # Style indicator only. This is not a probability of AI authorship.
    score = 50
    score += min(len(ai_found) * 7, 28)
    score += min(len(repeated) * 3, 12)

    if avg_sentence > 28:
        score += 8
    if len(sentences) >= 4 and avg_sentence < 8:
        score += 5

    score -= min(len(personal_found) * 5, 25)
    score = max(0, min(100, score))

    if len(words) < 80:
        assessment = "Too little text"
        explanation = (
            "This sample is short, so there are too few signals for a meaningful "
            "style assessment."
        )
    elif score >= 65:
        assessment = "More formulaic signals"
        explanation = (
            "Some formulaic phrases or repetition appear in this text. They can "
            "occur in AI-assisted writing, but also in human writing."
        )
    elif score <= 35:
        assessment = "More personal-style signals"
        explanation = (
            "The text includes personal phrasing or fewer of the formulaic patterns "
            "checked here. This does not prove a human wrote it."
        )
    else:
        assessment = "Mixed signals"
        explanation = (
            "The text contains a mixture of writing-style signals. This analysis "
            "cannot reliably identify its author."
        )

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_sentence": round(avg_sentence, 1),
        "ai_markers": ai_found,
        "human_markers": personal_found,
        "repeated_words": repeated,
        "score": score,
        "assessment": assessment,
        "explanation": explanation,
        "limitations": [
            "This score is a rule-based style indicator, not the probability that AI wrote the text.",
            "Human writing can sound formulaic, and AI-assisted writing can sound personal.",
            "Editing, translation, topic, and text length can affect these signals.",
        ],
    }


def answer_question(question: str, text: str, result: dict) -> str:
    q = question.lower()

    if not text.strip():
        return "Paste a text in the Analyze tab first, and I'll help you inspect it."

    if any(term in q for term in ["ai", "human", "written", "author", "انسان", "ذكاء"]):
        return (
            f"My style check says: **{result['assessment']}**. "
            f"{result['explanation']} This is not proof of authorship."
        )

    if any(term in q for term in ["repeat", "repetition", "repeated", "تكرار"]):
        if result["repeated_words"]:
            items = ", ".join(
                f"**{word}** ({count} times)"
                for word, count in result["repeated_words"]
            )
            return (
                f"I found some words repeated at least three times: {items}. "
                "Repeated words are not automatically a problem. Check whether "
                "they help your point or make the writing repetitive."
            )
        return "I didn't find longer words repeated three or more times."

    if any(term in q for term in ["sentence", "length", "long", "جمل"]):
        return (
            f"The text has **{result['sentence_count']} sentences** and about "
            f"**{result['avg_sentence']} words per sentence** on average. "
            "Mixing shorter and longer sentences can create a more natural rhythm."
        )

    if any(term in q for term in ["improve", "rewrite", "natural", "better", "تحسين"]):
        return (
            "To improve the writing, use specific examples, vary sentence openings, "
            "remove repeated ideas, and include details that are genuinely yours. "
            "Don't invent personal experiences."
        )

    if any(term in q for term in ["why", "explain", "reason", "سبب"]):
        if result["ai_markers"]:
            phrases = ", ".join(f"**{phrase}**" for phrase in result["ai_markers"])
            return (
                f"Some formulaic phrases I noticed are: {phrases}. These are common "
                "expressions, not proof of AI authorship. " + result["explanation"]
            )
        return (
            "I didn't find the specific formulaic phrases this simple check looks for. "
            "That doesn't prove who wrote the text. " + result["explanation"]
        )

    return (
        f"The sample has **{result['word_count']} words**, "
        f"**{result['sentence_count']} sentences**, and an average of "
        f"**{result['avg_sentence']} words per sentence**. "
        f"My style assessment is **{result['assessment']}**. "
        "Ask about repetition, sentence length, writing style, or clarity."
    )


# ============================================================
# SESSION STATE
# ============================================================

if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Hello, detective! Paste a text in Analyze and ask me what stands out. "
            "I'll explain the clues without pretending I can prove who wrote it."
        ),
    }]

if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False

if "example_pending" not in st.session_state:
    st.session_state.example_pending = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ORATORPULSE")
    st.caption("THE SPEECH & WRITING DETECTIVE")
    st.markdown("---")
    st.markdown("### YOUR WORKSPACE")
    st.write("Inspect writing style, spot repetition, and explore how your text reads.")

    if st.button("START FRESH", use_container_width=True):
        st.session_state.example_pending = ""
        st.session_state.analysis_requested = False
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Fresh start! Paste a text in Analyze and let's inspect it.",
        }]
        st.rerun()

    st.markdown("---")
    st.markdown("### IMPORT TEXT")
    uploaded = st.file_uploader(
        "Upload a TXT or CSV file",
        type=["txt", "csv"],
        help="TXT loads as text. CSV loads the first column as text.",
    )

    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".txt"):
                imported_text = uploaded.getvalue().decode("utf-8", errors="replace")
            else:
                data = pd.read_csv(uploaded)
                imported_text = (
                    "\n".join(data.iloc[:, 0].dropna().astype(str).tolist())
                    if not data.empty else ""
                )

            if imported_text.strip():
                st.session_state.example_pending = imported_text
                st.session_state.analysis_requested = False
                st.success("Text imported! It will appear in the editor.")
                st.rerun()
        except Exception as exc:
            st.error(f"Couldn't read this file: {exc}")

    st.markdown("---")
    st.caption("Audio transcription is not enabled in this demo.")


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-label">CASE FILE #001 · EST. 1930-SOMETHING</div>
    <h1>OratorPulse</h1>
    <p>Your playful detective for speech and writing style.</p>
    <p>Spot patterns. Understand the clues. Keep the human in the loop.</p>
</div>
""", unsafe_allow_html=True)

tab_analyze, tab_chat, tab_about = st.tabs([
    "ANALYZE",
    "THE DETECTIVE",
    "HOW IT WORKS",
])


# ============================================================
# ANALYSIS TAB
# ============================================================

with tab_analyze:
    st.markdown("## DROP YOUR TEXT HERE")
    st.write("An essay, a paragraph, or a speech draft. Let's inspect the clues.")

    example_text = (
        "I remember the first time I tried to explain my idea to a friend. "
        "I was nervous, and I kept repeating the same point. After a while, "
        "I realized that a simple example made the idea much easier to understand."
    )

    # IMPORTANT: set the widget value before creating the text_area.
    if st.session_state.example_pending is not None:
        st.session_state.speech_text = st.session_state.example_pending
        st.session_state.example_pending = None

    text_input = st.text_area(
        "Text to inspect",
        key="speech_text",
        height=230,
        placeholder="Paste your speech or writing here...",
        label_visibility="collapsed",
    )

    col_a, col_b = st.columns(2)

    with col_a:
        analyze_clicked = st.button("INSPECT MY TEXT", use_container_width=True)

    with col_b:
        example_clicked = st.button("TRY AN EXAMPLE", use_container_width=True)

    if example_clicked:
        st.session_state.example_pending = example_text
        st.session_state.analysis_requested = False
        st.rerun()

    if analyze_clicked:
        st.session_state.analysis_requested = True

    if st.session_state.analysis_requested:
        result = analyze_text(text_input)

        if result["word_count"] == 0:
            st.warning("Paste a little text first, detective!")
        else:
            st.markdown("---")
            st.markdown("## WHAT THE CLUES SAY")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="cartoon-card card-red">
                    <div class="small-label">WORD COUNT</div>
                    <div class="big-number">{result['word_count']}</div>
                    <div>Words in this sample</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="cartoon-card card-teal">
                    <div class="small-label">SENTENCES</div>
                    <div class="big-number">{result['sentence_count']}</div>
                    <div>Average: {result['avg_sentence']} words</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                signal_count = len(result["ai_markers"]) + len(result["human_markers"])
                st.markdown(f"""
                <div class="cartoon-card card-blue">
                    <div class="small-label">STYLE CLUES</div>
                    <div class="big-number">{signal_count}</div>
                    <div>Patterns spotted by the demo</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### DOES IT SOUND AI-WRITTEN?")
            st.markdown(f"""
            <div class="cartoon-card">
                <div class="hero-label">STYLE CHECK — NOT A VERDICT</div>
                <h2>{html.escape(result['assessment'])}</h2>
                <p>{html.escape(result['explanation'])}</p>
            </div>
            """, unsafe_allow_html=True)

            st.caption(
                f"Experimental formulaic-style indicator: {result['score']}/100. "
                "This is NOT the probability that AI wrote the text."
            )
            st.progress(result["score"] / 100)

            left, right = st.columns(2)

            with left:
                st.markdown(
                    '<div class="cartoon-card card-red"><h3>FORMULAIC PHRASES</h3>',
                    unsafe_allow_html=True,
                )
                if result["ai_markers"]:
                    for phrase in result["ai_markers"]:
                        st.markdown(f"- “{phrase}”")
                else:
                    st.write("No checked phrases found.")
                st.markdown(
                    "<small>These phrases can also be used naturally by people.</small></div>",
                    unsafe_allow_html=True,
                )

            with right:
                st.markdown(
                    '<div class="cartoon-card card-teal"><h3>PERSONAL-STYLE CLUES</h3>',
                    unsafe_allow_html=True,
                )
                if result["human_markers"]:
                    for phrase in result["human_markers"]:
                        st.markdown(f"- “{phrase}”")
                else:
                    st.write("No checked personal phrases found.")
                st.markdown(
                    "<small>Personal wording does not prove human authorship.</small></div>",
                    unsafe_allow_html=True,
                )

            st.markdown("### REPETITION RADAR")
            if result["repeated_words"]:
                for word, count in result["repeated_words"]:
                    st.markdown(
                        f'<span class="pill">{html.escape(word)} × {count}</span>',
                        unsafe_allow_html=True,
                    )
            else:
                st.write("No longer words were repeated three or more times.")

            with st.expander("LIMITS OF THIS ANALYSIS"):
                for limitation in result["limitations"]:
                    st.write(f"• {limitation}")

            st.info(
                "This demo uses transparent text rules, not a trained AI detector. "
                "It does not analyze voice tone, pitch, pauses, or audio."
            )


# ============================================================
# CHAT TAB
# ============================================================

with tab_chat:
    st.markdown("## ASK THE DETECTIVE")
    st.write("Ask a question about the text you've inspected.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Why does it sound formulaic? How can I improve it?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        result = analyze_text(st.session_state.speech_text)
        response = answer_question(prompt, st.session_state.speech_text, result)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


# ============================================================
# ABOUT TAB
# ============================================================

with tab_about:
    st.markdown("## MEET YOUR DETECTIVE")

    st.markdown("""
    <div class="cartoon-card card-cream">
        <h2>A CLUE FINDER, NOT A JUDGE.</h2>
        OratorPulse checks repeated words, sentence length, selected formulaic
        phrases, and personal-style expressions. It explains the patterns it
        finds in simple language.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cartoon-card card-red">
        <h3>WHAT THIS DEMO CAN DO</h3>
        - Inspect pasted text and imported TXT or CSV files
        - Find repeated words and selected writing patterns
        - Explain why a text may sound formulaic
        - Suggest ways to improve clarity and variation
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cartoon-card card-teal">
        <h3>WHAT'S NOT CONNECTED YET</h3>
        - No external AI model or live chatbot API
        - No speech-to-text transcription
        - No acoustic analysis of pitch, pauses, or voice
        - No reliable proof of whether a person or AI wrote a text
    </div>
    """, unsafe_allow_html=True)

    st.caption("OratorPulse Demo — Speech & Writing Style Detective")
