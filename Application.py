
from __future__ import annotations

import re
import html
from collections import Counter

import streamlit as st

st.set_page_config(
    page_title="OratorPulse — Speech Detective",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- STYLE --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@400;600;700;800;900&display=swap');

:root {
    --ink: #28213d;
    --purple: #7957e8;
    --yellow: #ffdc65;
    --pink: #ff91b8;
    --blue: #8ce5f2;
    --paper: #fffaf0;
}

html, body, [data-testid="stAppViewContainer"], input, textarea, button, label {
    font-family: 'Nunito', sans-serif !important;
}

.stApp, [data-testid="stAppViewContainer"] {
    background: #f4efff;
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1120px;
    padding: 2rem 2rem 4rem;
}

h1, h2, h3 {
    font-family: 'Fredoka', sans-serif !important;
    color: var(--ink);
    letter-spacing: -.5px;
}

[data-testid="stSidebar"] {
    background: #ffedbd;
    border-right: 3px solid var(--ink);
}

.hero {
    background: var(--purple);
    border: 3px solid var(--ink);
    border-radius: 28px;
    padding: 30px;
    color: white;
    box-shadow: 7px 7px 0 var(--ink);
    margin-bottom: 26px;
    position: relative;
}

.hero h1 {
    color: white !important;
    font-size: 2.8rem;
    margin: 0;
}

.hero p {
    color: #f5efff;
    font-size: 1.05rem;
    margin-bottom: 0;
}

.sticker {
    display: inline-block;
    background: var(--yellow);
    color: var(--ink);
    padding: 6px 12px;
    border: 2px solid var(--ink);
    border-radius: 12px;
    font-weight: 900;
    transform: rotate(-2deg);
    margin-bottom: 12px;
}

.card {
    background: white;
    border: 3px solid var(--ink);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 5px 5px 0 var(--ink);
    margin-bottom: 20px;
}

.card-yellow {
    background: var(--yellow);
}

.card-pink {
    background: #ffd9e7;
}

.card-blue {
    background: #d5f8fc;
}

.small-label {
    font-size: .82rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.big-number {
    font-family: 'Fredoka', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.2;
}

.pill {
    display: inline-block;
    background: #eee7ff;
    border: 2px solid var(--ink);
    border-radius: 999px;
    padding: 5px 11px;
    font-weight: 800;
    margin: 4px 4px 4px 0;
}

.finding {
    border-left: 5px solid var(--purple);
    background: #f7f3ff;
    padding: 12px 14px;
    border-radius: 10px;
    margin: 10px 0;
}

.stButton > button {
    border: 3px solid var(--ink);
    border-radius: 14px;
    background: var(--yellow);
    color: var(--ink);
    font-weight: 900;
    box-shadow: 4px 4px 0 var(--ink);
    transition: .15s ease;
}

.stButton > button:hover {
    background: var(--pink);
    color: var(--ink);
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0 var(--ink);
}

.stTextArea textarea, .stTextInput input {
    border: 2px solid var(--ink) !important;
    border-radius: 14px !important;
    background: white !important;
}

[data-testid="stChatMessage"] {
    border: 2px solid var(--ink);
    border-radius: 18px;
    background: white;
}

[data-testid="stMetric"] {
    background: white;
    border: 2px solid var(--ink);
    border-radius: 16px;
    padding: 12px;
    box-shadow: 3px 3px 0 var(--ink);
}

hr {
    border-color: #d9cafa;
}

footer {
    visibility: hidden;
}

@media (max-width: 700px) {
    .hero { padding: 22px; }
    .hero h1 { font-size: 2rem; }
    .block-container { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)


# -------------------- TEXT ANALYSIS --------------------

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
            "repetition": 0,
            "ai_markers": [],
            "human_markers": [],
            "repeated_words": [],
            "score": None,
            "assessment": "Not enough text",
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
    repetition = sum(count - 1 for _, count in repeated)

    lower = clean.lower()
    ai_found = [p for p in AI_STYLE_PHRASES if p in lower]
    human_found = [p for p in PERSONAL_MARKERS if p in lower]

    # This is a transparent writing-style heuristic, NOT a trained AI detector.
    score = 50
    score += min(len(ai_found) * 7, 28)
    score += min(len(repeated) * 3, 12)
    if avg_sentence > 28:
        score += 8
    if len(sentences) >= 4 and avg_sentence < 8:
        score += 5
    score -= min(len(human_found) * 5, 25)
    score = max(0, min(100, score))

    if len(words) < 80:
        assessment = "Too little text"
        explanation = (
            "This sample is short. The style signals are too limited "
            "to support a meaningful authorship estimate."
        )
    elif score >= 65:
        assessment = "More formulaic signals"
        explanation = (
            "The text contains some formulaic phrases or repetition "
            "that can appear in AI-assisted writing. These signals "
            "can also appear in human writing."
        )
    elif score <= 35:
        assessment = "More personal-style signals"
        explanation = (
            "The text includes personal phrasing or fewer of the "
            "specific formulaic patterns checked here. That does not "
            "prove a human wrote it."
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
        "repetition": repetition,
        "ai_markers": ai_found,
        "human_markers": human_found,
        "repeated_words": repeated,
        "score": score,
        "assessment": assessment,
        "explanation": explanation,
        "limitations": [
            "The score is a rule-based style indicator, not the probability that AI wrote the text.",
            "Human writing can sound formulaic, and AI-assisted writing can sound personal.",
            "Editing, translation, topic, and text length can affect these signals.",
        ],
    }


def answer_question(question: str, text: str, result: dict) -> str:
    q = question.lower()

    if not text.strip():
        return "Paste a text in the Analysis tab first, and I'll help you understand it."

    if any(x in q for x in ["ai", "human", "written", "author", "انسان", "ذكاء"]):
        return (
            f"My style check says: **{result['assessment']}**. "
            f"{result['explanation']} "
            "This is not proof of authorship. I can point out patterns, "
            "but I cannot reliably determine whether a person or an AI wrote it."
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
                "they make the text clearer or simply make it feel repetitive."
            )
        return "I didn't find any longer words repeated three or more times in this sample."

    if any(x in q for x in ["sentence", "length", "long", "جمل"]):
        return (
            f"The text has **{result['sentence_count']} sentences** and "
            f"about **{result['avg_sentence']} words per sentence** on average. "
            "Mixing shorter sentences with longer ones can improve rhythm, "
            "depending on the audience and purpose."
        )

    if any(x in q for x in ["improve", "rewrite", "natural", "better", "تحسين"]):
        return (
            "To make the writing clearer and more natural, try replacing vague "
            "claims with specific examples, varying sentence openings, removing "
            "repeated ideas, and including details that are genuinely yours. "
            "Don't add personal experiences that did not happen."
        )

    if any(x in q for x in ["why", "explain", "reason", "سبب"]):
        found = result["ai_markers"]
        if found:
            return (
                "Some formulaic phrases I noticed are: "
                + ", ".join(f"**{p}**" for p in found)
                + ". These are common expressions, not proof of AI authorship. "
                + result["explanation"]
            )
        return (
            "I didn't find the specific formulaic phrases this simple check looks for. "
            "That doesn't establish who wrote the text. "
            + result["explanation"]
        )

    return (
        f"Here's what I can tell from the current sample: "
        f"**{result['word_count']} words**, "
        f"**{result['sentence_count']} sentences**, and an average of "
        f"**{result['avg_sentence']} words per sentence**. "
        f"My style assessment is **{result['assessment']}**. "
        "Ask me about authorship signals, repetition, sentence length, or how to improve clarity."
    )


# -------------------- STATE --------------------

if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hey! 🎙️ I'm your writing-style detective. Paste your text "
                "in the Analysis tab, then ask me what stands out. "
                "I'll explain the clues without pretending I can prove who wrote it."
            ),
        }
    ]


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## 🎙️ OratorPulse")
    st.caption("THE SPEECH & WRITING DETECTIVE")
    st.markdown("---")

    st.markdown("### 🧩 Your workspace")
    st.write("Analyze writing style, spot repetition, and explore how your text reads.")

    if st.button("✨ Start fresh", use_container_width=True):
        st.session_state.speech_text = ""
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Fresh start! Paste a text in Analysis and let's inspect it together. 🔎",
            }
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📂 Import text")
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
                import pandas as pd
                data = pd.read_csv(uploaded)
                if data.empty:
                    imported_text = ""
                else:
                    imported_text = "\n".join(
                        data.iloc[:, 0].dropna().astype(str).tolist()
                    )

            if imported_text.strip():
                st.session_state.speech_text = imported_text
                st.success("Text imported!")
        except Exception as exc:
            st.error(f"Couldn't read this file: {exc}")

    st.markdown("---")
    st.caption("Audio transcription is not enabled in this demo. Upload text to analyze it.")


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="sticker">🔎 CASE FILE #001</div>
    <h1>OratorPulse</h1>
    <p>Your playful detective for speech and writing style.</p>
    <p>Spot patterns. Understand the clues. Keep the human in the loop.</p>
</div>
""", unsafe_allow_html=True)

tab_analyze, tab_chat, tab_about = st.tabs(
    ["🕵️ Analyze", "💬 Ask the Detective", "🎨 How it works"]
)


# -------------------- ANALYSIS TAB --------------------

with tab_analyze:
    st.markdown("## 📝 Drop your text here")
    st.write("A paragraph, an essay, a speech draft — let's see what patterns show up.")

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

    col_a, col_b = st.columns([1, 1])
    with col_a:
        analyze_clicked = st.button(
            "🔎 Inspect my text",
            use_container_width=True,
        )
    with col_b:
        if st.button("🪄 Try an example", use_container_width=True):
            st.session_state.speech_text = example_text
            st.rerun()

    if analyze_clicked:
        st.session_state.analysis_requested = True

    if st.session_state.get("analysis_requested", False):
        result = analyze_text(text_input)

        if result["word_count"] == 0:
            st.warning("Paste a little text first, detective!")
        else:
            st.markdown("---")
            st.markdown("## 🧠 What the clues say")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f"""<div class="card card-yellow">
                    <div class="small-label">📝 Word count</div>
                    <div class="big-number">{result['word_count']}</div>
                    <div>Words in this sample</div></div>""",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""<div class="card card-pink">
                    <div class="small-label">💬 Sentences</div>
                    <div class="big-number">{result['sentence_count']}</div>
                    <div>Average length: {result['avg_sentence']} words</div></div>""",
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""<div class="card card-blue">
                    <div class="small-label">🔎 Style signals</div>
                    <div class="big-number">{len(result['ai_markers']) + len(result['human_markers'])}</div>
                    <div>Patterns detected by simple rules</div></div>""",
                    unsafe_allow_html=True,
                )

            st.markdown("### 🎭 Does it sound AI-written?")
            st.markdown(
                f"""<div class="card">
                <div class="sticker">STYLE CHECK — NOT A VERDICT</div>
                <h2>{html.escape(result['assessment'])}</h2>
                <p>{html.escape(result['explanation'])}</p>
                </div>""",
                unsafe_allow_html=True,
            )

            if result["score"] is not None:
                st.caption(
                    f"Experimental formulaic-style indicator: {result['score']}/100. "
                    "This is NOT the probability that AI wrote the text."
                )
                st.progress(result["score"] / 100)

            left, right = st.columns(2)

            with left:
                st.markdown(
                    '<div class="card card-pink"><h3>🤖 Formulaic phrases</h3>',
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
                    '<div class="card card-blue"><h3>💛 Personal-style clues</h3>',
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

            st.markdown("### 🔁 Repetition radar")
            if result["repeated_words"]:
                for word, count in result["repeated_words"]:
                    st.markdown(
                        f'<span class="pill">{html.escape(word)} × {count}</span>',
                        unsafe_allow_html=True,
                    )
            else:
                st.write("No longer words were repeated three or more times.")

            with st.expander("🧪 Limits of this analysis"):
                for limitation in result["limitations"]:
                    st.write(f"• {limitation}")

            st.info(
                "This demo uses transparent text rules, not a trained AI detector. "
                "It does not analyze voice tone, pitch, pauses, or audio."
            )


# -------------------- CHAT TAB --------------------

with tab_chat:
    st.markdown("## 💬 Ask the Detective")
    st.write("Ask a question about the text you've inspected.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(
        "Why does it sound formulaic? How can I improve it?"
    )

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        result = analyze_text(st.session_state.speech_text)
        response = answer_question(
            prompt,
            st.session_state.speech_text,
            result,
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
        st.rerun()


# -------------------- ABOUT TAB --------------------

with tab_about:
    st.markdown("## 🎨 Meet your detective")
    st.markdown(
        """<div class="card card-yellow">
        <h2>🕵️ A clue finder, not a judge.</h2>
        OratorPulse checks for repeated words, sentence length, selected
        formulaic phrases, and personal-style expressions. It explains the
        patterns it finds in simple language.
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="card card-pink">
        <h3>💡 What this demo can do</h3>
        - Inspect pasted text and imported TXT or CSV files
        - Find repeated words and selected writing patterns
        - Explain why a text may sound formulaic
        - Suggest ways to improve clarity and variation
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="card card-blue">
        <h3>🚧 What's not connected yet</h3>
        - No external AI model or live chatbot API
        - No speech-to-text transcription
        - No acoustic analysis of pitch, pauses, or voice
        - No reliable proof of whether a person or AI wrote a text
        </div>""",
        unsafe_allow_html=True,
    )

    st.caption(
        "OratorPulse demo • Built for exploring speech and writing style."
    )
