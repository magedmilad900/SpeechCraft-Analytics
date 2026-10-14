from __future__ import annotations

import html
import re
from collections import Counter

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="OratorPulse — Speech Detective",
    page_icon="🎙️",
    layout="wide",
)

# ==================== CARTOON DESIGN ====================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Fredoka:wght@400;500;600;700&family=Patrick+Hand&display=swap');

:root {
    --ink: #171326;
    --purple: #9857ff;
    --pink: #ff5ca8;
    --green: #d6ff76;
    --cyan: #42f5ed;
    --paper: #fffdf5;
}

html, body, [data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] *,
[data-testid="stSidebar"] *,
button, input, textarea, label {
    font-family: 'Fredoka', 'Comic Sans MS', cursive !important;
}

.stApp, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 10%, #ff9ed0 0 2px, transparent 3px),
        radial-gradient(circle at 90% 30%, #70fff3 0 3px, transparent 4px),
        radial-gradient(circle at 30% 90%, #d6ff76 0 2px, transparent 3px),
        #eee5ff;
    background-size: 38px 38px, 51px 51px, 43px 43px, auto;
    color: var(--ink);
}

[data-testid="stHeader"] { background: transparent; }

.block-container {
    max-width: 1180px;
    padding: 2rem 2rem 4rem;
}

h1, h2, h3, h4, [data-testid="stMetricValue"] {
    font-family: 'Bangers', 'Fredoka', cursive !important;
    letter-spacing: 1px !important;
    color: var(--ink);
}

h1 { font-size: 3rem !important; }
h2 { font-size: 2rem !important; }
h3 { font-size: 1.55rem !important; }

p, li, label, input, textarea, small {
    font-family: 'Fredoka', cursive !important;
}

[data-testid="stSidebar"] {
    background: var(--green);
    border-right: 4px solid var(--ink);
    box-shadow: 6px 0 0 var(--ink);
}

.hero {
    position: relative;
    overflow: hidden;
    background: var(--purple);
    color: white;
    border: 4px solid var(--ink);
    border-radius: 30px;
    padding: 34px;
    box-shadow: 9px 9px 0 var(--ink);
    margin: 8px 0 32px;
}

.hero::after {
    content: "★ ✦ ●";
    position: absolute;
    right: 22px;
    top: 16px;
    color: var(--green);
    font-family: 'Bangers', cursive;
    font-size: 2rem;
    -webkit-text-stroke: 1px var(--ink);
}

.hero h1 {
    color: white !important;
    font-size: clamp(2.5rem, 6vw, 4.3rem) !important;
    text-shadow: 4px 4px 0 var(--ink);
    margin: 0;
}

.hero p {
    color: white !important;
    font-size: 1.1rem;
    font-weight: 600;
}

.sticker {
    display: inline-block;
    background: var(--green);
    color: var(--ink);
    padding: 7px 14px;
    border: 3px solid var(--ink);
    border-radius: 12px;
    font-family: 'Bangers', cursive !important;
    font-size: 1.15rem;
    transform: rotate(-3deg);
    box-shadow: 3px 3px 0 var(--ink);
    margin-bottom: 15px;
}

.cartoon-card {
    background: var(--paper);
    color: var(--ink);
    border: 3px solid var(--ink);
    border-radius: 24px;
    padding: 23px;
    box-shadow: 6px 6px 0 var(--ink);
    margin: 12px 0 22px;
}

.green-card { background: var(--green); }
.pink-card { background: #ffb4d2; }
.blue-card { background: #a7f7f4; }
.purple-card { background: #d7bdff; }

.small-label {
    font-family: 'Bangers', cursive !important;
    font-size: 1.05rem;
    letter-spacing: 1px;
}

.big-number {
    font-family: 'Bangers', cursive !important;
    font-size: 3rem;
    line-height: 1.2;
    text-shadow: 2px 2px white;
}

.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: var(--green);
    color: var(--ink);
    border: 3px solid var(--ink);
    border-radius: 15px;
    min-height: 46px;
    font-family: 'Fredoka', cursive !important;
    font-weight: 800;
    box-shadow: 5px 5px 0 var(--ink);
    transition: all .15s ease;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--pink);
    color: var(--ink);
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0 var(--ink);
}

.stTextArea textarea,
.stTextInput input,
[data-testid="stChatInput"] textarea {
    background: white !important;
    color: var(--ink) !important;
    border: 3px solid var(--ink) !important;
    border-radius: 17px !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.15rem !important;
}

[data-testid="stFileUploader"] section {
    border: 3px dashed var(--ink);
    border-radius: 17px;
    background: white;
}

[data-testid="stMetric"] {
    background: var(--green);
    border: 3px solid var(--ink);
    border-radius: 19px;
    padding: 15px;
    box-shadow: 5px 5px 0 var(--ink);
}

[data-testid="stMetricLabel"] {
    font-family: 'Bangers', cursive !important;
}

[data-testid="stChatMessage"] {
    background: white;
    border: 3px solid var(--ink);
    border-radius: 20px;
    box-shadow: 4px 4px 0 var(--ink);
    padding: 12px;
    margin-bottom: 16px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border: 3px solid var(--ink);
    border-radius: 13px;
    padding: 10px 16px;
    font-family: 'Fredoka', cursive !important;
    font-weight: 800;
    box-shadow: 3px 3px 0 var(--ink);
}

.stTabs [aria-selected="true"] {
    background: var(--green) !important;
    color: var(--ink) !important;
}

[data-testid="stExpander"],
[data-testid="stAlert"] {
    background: white;
    border: 3px solid var(--ink);
    border-radius: 18px;
    box-shadow: 4px 4px 0 var(--ink);
}

[data-testid="stProgress"] > div {
    background: white;
    border: 2px solid var(--ink);
    border-radius: 999px;
    padding: 3px;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--pink), var(--purple), var(--cyan));
    border-radius: 999px;
}

.pill {
    display: inline-block;
    background: var(--cyan);
    color: var(--ink);
    border: 2px solid var(--ink);
    border-radius: 999px;
    padding: 6px 12px;
    font-weight: 900;
    box-shadow: 2px 2px 0 var(--ink);
    margin: 4px;
}

hr {
    border: none;
    border-top: 3px dashed #9b82d6;
    margin: 26px 0;
}

footer { visibility: hidden; }

@media (max-width: 700px) {
    .block-container { padding: 1rem; }
    .hero { padding: 24px; }
    .hero h1 { font-size: 2.7rem !important; }
    .cartoon-card { padding: 17px; }
}
</style>
""", unsafe_allow_html=True)


# ==================== ANALYSIS ENGINE ====================

AI_STYLE_PHRASES = [
    "in conclusion",
    "it is important to note",
    "delve into",
    "furthermore",
    "moreover",
    "in today's world",
    "plays a crucial role",
    "comprehensive understanding",
    "multifaceted",
    "landscape of",
    "it is worth noting",
    "this highlights the importance",
    "not only that, but also",
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
        s.strip()
        for s in re.split(r"(?<=[.!?؟])\s+|\n+", text)
        if s.strip()
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

    ai_found = [p for p in AI_STYLE_PHRASES if p in lower]
    personal_found = [p for p in PERSONAL_MARKERS if p in lower]

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
            "This sample is short. There are too few signals to make "
            "a meaningful authorship estimate."
        )
    elif score >= 65:
        assessment = "More formulaic signals"
        explanation = (
            "Some formulaic phrases or repetition appear in this text. "
            "They can occur in AI-assisted writing, but also in human writing."
        )
    elif score <= 35:
        assessment = "More personal-style signals"
        explanation = (
            "The text contains personal phrasing or fewer of the formulaic "
            "patterns checked here. This does not prove a human wrote it."
        )
    else:
        assessment = "Mixed signals"
        explanation = (
            "The text contains a mixture of writing-style signals. "
            "This analysis cannot reliably identify its author."
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

    if any(x in q for x in ["ai", "human", "written", "author", "انسان", "ذكاء"]):
        return (
            f"My style check says: **{result['assessment']}**. "
            f"{result['explanation']} This is not proof of authorship."
        )

    if any(x in q for x in ["repeat", "repetition", "repeated", "تكرار"]):
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

    if any(x in q for x in ["sentence", "length", "long", "جمل"]):
        return (
            f"The text has **{result['sentence_count']} sentences** and about "
            f"**{result['avg_sentence']} words per sentence** on average. "
            "Try mixing shorter sentences with longer ones for a more natural rhythm."
        )

    if any(x in q for x in ["improve", "rewrite", "natural", "better", "تحسين"]):
        return (
            "To improve the writing, use specific examples, vary sentence openings, "
            "remove repeated ideas, and include details that are genuinely yours. "
            "Don't invent personal experiences."
        )

    if any(x in q for x in ["why", "explain", "reason", "سبب"]):
        if result["ai_markers"]:
            phrases = ", ".join(f"**{p}**" for p in result["ai_markers"])
            return (
                f"Some formulaic phrases I noticed are: {phrases}. "
                "These are common expressions, not proof of AI authorship. "
                + result["explanation"]
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


# ==================== SESSION STATE ====================

if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hey! I'm your writing-style detective. Paste text in the Analyze tab, "
                "then ask me what stands out. I'll explain the clues without pretending "
                "I can prove who wrote it."
            ),
        }
    ]

if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("## ORATORPULSE")
    st.caption("THE SPEECH & WRITING DETECTIVE")
    st.markdown("---")
    st.markdown("### YOUR WORKSPACE")
    st.write("Inspect writing style, spot repetition, and explore how your text reads.")

    if st.button("START FRESH", use_container_width=True):
        st.session_state.speech_text = ""
        st.session_state.analysis_requested = False
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Fresh start! Paste some text in Analyze and let's inspect it.",
            }
        ]
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
                imported_text = uploaded.getvalue().decode(
                    "utf-8", errors="replace"
                )
            else:
                data = pd.read_csv(uploaded)
                imported_text = (
                    "\n".join(data.iloc[:, 0].dropna().astype(str).tolist())
                    if not data.empty else ""
                )

            if imported_text.strip():
                st.session_state.speech_text = imported_text
                st.session_state.analysis_requested = False
                st.success("Text imported!")
        except Exception as exc:
            st.error(f"Couldn't read this file: {exc}")

    st.markdown("---")
    st.caption("Audio transcription is not enabled in this demo.")


# ==================== HEADER ====================

st.markdown("""
<div class="hero">
    <div class="sticker">CASE FILE #001</div>
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


# ==================== ANALYSIS TAB ====================

with tab_analyze:
    st.markdown("## DROP YOUR TEXT HERE")
    st.write("A paragraph, an essay, or a speech draft. Let's inspect the clues.")

    example_text = (
        "I remember the first time I tried to explain my idea to a friend. "
        "I was nervous, and I kept repeating the same point. After a while, "
        "I realized that a simple example made the idea much easier to understand."
    )

    text_input = st.text_area(
        "Text to inspect",
        key="speech_text",
        height=230,
        placeholder="Paste your speech or writing here...",
        label_visibility="collapsed",
    )

    col_a, col_b = st.columns(2)

    with col_a:
        analyze_clicked = st.button(
            "INSPECT MY TEXT",
            use_container_width=True,
        )

    with col_b:
        example_clicked = st.button(
            "TRY AN EXAMPLE",
            use_container_width=True,
        )

    if example_clicked:
        st.session_state.speech_text = example_text
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

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="cartoon-card green-card">
                    <div class="small-label">WORD COUNT</div>
                    <div class="big-number">{result['word_count']}</div>
                    <div>Words in this sample</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="cartoon-card pink-card">
                    <div class="small-label">SENTENCES</div>
                    <div class="big-number">{result['sentence_count']}</div>
                    <div>Average length: {result['avg_sentence']} words</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                signal_count = (
                    len(result["ai_markers"]) + len(result["human_markers"])
                )
                st.markdown(f"""
                <div class="cartoon-card blue-card">
                    <div class="small-label">STYLE SIGNALS</div>
                    <div class="big-number">{signal_count}</div>
                    <div>Patterns detected by simple rules</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### DOES IT SOUND AI-WRITTEN?")

            st.markdown(f"""
            <div class="cartoon-card">
                <div class="sticker">STYLE CHECK — NOT A VERDICT</div>
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
                    '<div class="cartoon-card pink-card"><h3>FORMULAIC PHRASES</h3>',
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
                    '<div class="cartoon-card blue-card"><h3>PERSONAL-STYLE CLUES</h3>',
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


# ==================== CHAT TAB ====================

with tab_chat:
    st.markdown("## ASK THE DETECTIVE")
    st.write("Ask a question about the text you've inspected.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(
        "Why does it sound formulaic? How can I improve it?"
    )

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })

        result = analyze_text(st.session_state.speech_text)
        response = answer_question(
            prompt,
            st.session_state.speech_text,
            result,
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })
        st.rerun()


# ==================== ABOUT TAB ====================

with tab_about:
    st.markdown("## MEET YOUR DETECTIVE")

    st.markdown("""
    <div class="cartoon-card green-card">
        <h2>A CLUE FINDER, NOT A JUDGE.</h2>
        OratorPulse checks repeated words, sentence length, selected formulaic
        phrases, and personal-style expressions. It explains the patterns it
        finds in simple language.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cartoon-card pink-card">
        <h3>WHAT THIS DEMO CAN DO</h3>
        - Inspect pasted text and imported TXT or CSV files
        - Find repeated words and selected writing patterns
        - Explain why a text may sound formulaic
        - Suggest ways to improve clarity and variation
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cartoon-card blue-card">
        <h3>WHAT'S NOT CONNECTED YET</h3>
        - No external AI model or live chatbot API
        - No speech-to-text transcription
        - No acoustic analysis of pitch, pauses, or voice
        - No reliable proof of whether a person or AI wrote a text
    </div>
    """, unsafe_allow_html=True)

    st.caption("OratorPulse Demo — Speech & Writing Style Detective")
