import re
from collections import Counter

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="OratorPulse — Cartoon Writing Lab",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Session state (set widget values BEFORE creating widgets) ----------
defaults = {
    "speech_text": "",
    "example_pending": None,
    "chat_history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.example_pending is not None:
    st.session_state.speech_text = st.session_state.example_pending
    st.session_state.example_pending = None

# ---------- Cute vintage rubber-hose visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Rye&family=Patrick+Hand&display=swap');

:root {
  --paper: #f7f4eb;
  --ink: #171717;
  --white: #fffef9;
  --grey: #e8e5dc;
  --mid: #77746e;
  --soft: #d6d2c8;
}
html, body, [class*="css"] {
  font-family: 'Fredoka', sans-serif;
  color: var(--ink);
}
.stApp {
  background: var(--paper);
  color: var(--ink);
}
[data-testid="stHeader"] { background: transparent; }
.block-container {
  max-width: 1180px;
  padding-top: 1.5rem;
  padding-bottom: 3rem;
}
h1, h2, h3 { color: var(--ink) !important; }
h1 {
  font-family: 'Rye', serif !important;
  letter-spacing: 1px;
}
p, li, label, .stCaption { color: var(--ink); }
.hero {
  position: relative;
  border: 4px solid var(--ink);
  border-radius: 28px 28px 24px 24px;
  padding: 28px 30px 24px;
  background: var(--white);
  box-shadow: 7px 7px 0 var(--ink);
  overflow: hidden;
  margin-bottom: 25px;
}
.hero:after {
  content: "✦";
  position: absolute;
  right: 25px;
  top: 6px;
  font-size: 58px;
  color: var(--ink);
  transform: rotate(12deg);
}
.hero-kicker {
  display: inline-block;
  border: 2px solid var(--ink);
  border-radius: 999px;
  background: var(--grey);
  padding: 4px 12px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 10px;
}
.hero-title {
  font-family: 'Rye', serif;
  font-size: clamp(34px, 5vw, 58px);
  line-height: 1.04;
  margin: 0 0 10px;
}
.hero-sub {
  font-family: 'Patrick Hand', cursive;
  font-size: 22px;
  max-width: 750px;
  line-height: 1.35;
}
.mascot {
  float: right;
  margin: 0 35px 4px 18px;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--ink);
  color: white;
  border: 4px solid var(--ink);
  border-radius: 48% 52% 47% 53%;
  font-size: 62px;
  transform: rotate(5deg);
  box-shadow: 4px 4px 0 var(--soft);
}
.stTabs [data-baseweb="tab-list"] {
  gap: 10px;
  border-bottom: 3px solid var(--ink);
}
.stTabs [data-baseweb="tab"] {
  background: var(--white);
  border: 2px solid var(--ink);
  border-bottom: 0;
  border-radius: 14px 14px 0 0;
  padding: 9px 18px;
  font-family: 'Fredoka', sans-serif;
  font-weight: 700;
}
.stTabs [aria-selected="true"] {
  background: var(--ink) !important;
  color: var(--white) !important;
}
.stTextArea textarea, .stTextInput input {
  background: var(--white) !important;
  color: var(--ink) !important;
  border: 3px solid var(--ink) !important;
  border-radius: 16px !important;
  font-family: 'Patrick Hand', cursive !important;
  font-size: 21px !important;
}
.stSelectbox [data-baseweb="select"] > div {
  background: var(--white);
  border: 2px solid var(--ink);
  border-radius: 12px;
}
.stButton button, .stDownloadButton button {
  background: var(--white);
  color: var(--ink);
  border: 3px solid var(--ink);
  border-radius: 14px;
  box-shadow: 4px 4px 0 var(--ink);
  font-family: 'Fredoka', sans-serif;
  font-weight: 700;
  transition: transform .12s ease, box-shadow .12s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
  background: var(--grey);
  color: var(--ink);
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 var(--ink);
  border-color: var(--ink);
}
.stButton button:active, .stDownloadButton button:active {
  transform: translate(4px, 4px);
  box-shadow: none;
}
.panel {
  background: var(--white);
  border: 3px solid var(--ink);
  border-radius: 20px;
  padding: 19px 20px;
  box-shadow: 5px 5px 0 var(--ink);
  margin: 8px 0 17px;
}
.panel-title {
  font-family: 'Rye', serif;
  font-size: 21px;
  margin-bottom: 8px;
}
.metric-card {
  background: var(--white);
  border: 3px solid var(--ink);
  border-radius: 18px;
  padding: 16px 14px;
  min-height: 112px;
  box-shadow: 4px 4px 0 var(--ink);
}
.metric-label {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.metric-value {
  font-family: 'Rye', serif;
  font-size: 31px;
  margin-top: 5px;
}
.stAlert {
  border: 2px solid var(--ink);
  border-radius: 14px;
}
hr { border-top: 2px dashed var(--soft); }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
@media (max-width: 650px) {
 .hero { padding: 22px 18px; }
 .mascot { width: 76px; height: 76px; font-size: 40px; margin-right: 12px; }
 .hero-title { font-size: 34px; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Analysis helpers ----------
AI_STYLE_PHRASES = [
    "in conclusion", "it is important to note", "delve into", "furthermore",
    "moreover", "plays a crucial role", "in today's world", "overall",
    "this highlights the importance", "a testament to", "multifaceted",
    "it is worth noting", "navigate the complexities"
]
PERSONAL_CUES = [
    "i think", "i feel", "i remember", "for me", "in my experience",
    "honestly", "i learned", "i noticed", "i tried", "my friend",
    "when i was", "i don't know", "i'm not sure"
]

def analyze_text(text):
    text = text.strip()
    if not text:
        return None
    words = re.findall(r"\b[\w’'-]+\b", text.lower())
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    word_count = len(words)
    sentence_count = max(len(sentences), 1)
    avg_sentence = word_count / sentence_count
    unique_ratio = len(set(words)) / max(word_count, 1)
    phrase_hits = [p for p in AI_STYLE_PHRASES if p in text.lower()]
    personal_hits = [p for p in PERSONAL_CUES if p in text.lower()]
    repeated = [(w, c) for w, c in Counter(words).most_common()
                if c >= 4 and len(w) > 3 and w not in {"that", "this", "with", "from", "have", "there", "about"}]
    punctuation = sum(text.count(x) for x in ["!", "?", "—", "..."])
    score = 50
    score += min(len(phrase_hits) * 6, 24)
    score -= min(len(personal_hits) * 5, 20)
    if avg_sentence > 28:
        score += 8
    elif avg_sentence < 10:
        score -= 4
    if unique_ratio < 0.42 and word_count > 40:
        score += 5
    if punctuation >= 4:
        score -= 2
    score = max(0, min(100, score))
    return {
        "words": word_count,
        "sentences": sentence_count,
        "avg_sentence": round(avg_sentence, 1),
        "unique_ratio": round(unique_ratio * 100),
        "phrase_hits": phrase_hits,
        "personal_hits": personal_hits,
        "repeated": repeated[:8],
        "score": score,
    }

def metric(label, value, note=""):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div style="font-size:13px;color:#555;margin-top:4px">{note}</div></div>',
        unsafe_allow_html=True
    )

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="mascot" aria-label="cute cartoon mascot">☺</div>
  <div class="hero-kicker">✦ THE LITTLE WRITING DETECTIVE ✦</div>
  <div class="hero-title">OratorPulse</div>
  <div class="hero-sub">A cute old-cartoon lab for exploring writing patterns. Big smiles, bendy lines, black ink, paper-white panels — zero spooky vibes.</div>
</div>
""", unsafe_allow_html=True)

tab_analyze, tab_detective, tab_about = st.tabs(["✍️  Text Lab", "🔎  Pattern Detective", "🎞️  Behind the Cartoon"])

with tab_analyze:
    left, right = st.columns([1.35, 0.85], gap="large")
    with left:
        st.markdown('<div class="panel-title">Drop your writing here!</div>', unsafe_allow_html=True)
        st.caption("Paste a paragraph, an essay, a post, or a sample you want to inspect.")
        text_value = st.text_area(
            "Your text",
            key="speech_text",
            height=260,
            placeholder="Once upon a time, I had an idea..."
            , label_visibility="collapsed"
        )
        b1, b2 = st.columns(2)
        with b1:
            analyze_clicked = st.button("✨ ANALYZE MY TEXT", use_container_width=True, type="primary")
        with b2:
            if st.button("🎈 TRY A CUTE EXAMPLE", use_container_width=True):
                st.session_state.example_pending = (
                    "Honestly, I wasn't sure how to start this project. I tried a few ideas, "
                    "made mistakes, and changed my plan. I think the most useful thing I learned "
                    "was to test one small part at a time instead of trying to make everything perfect."
                )
                st.rerun()
        if st.button("🧽 START FRESH", use_container_width=True):
            st.session_state.example_pending = ""
            st.rerun()
    with right:
        st.markdown("""
        <div class="panel">
          <div class="panel-title">Meet Pip!</div>
          <div style="font-size:64px;text-align:center;line-height:1.2">◕‿◕</div>
          <p style="font-family:'Patrick Hand',cursive;font-size:21px;text-align:center">
          “I look for patterns, not people to accuse!”
          </p>
          <hr>
          <b>What this lab checks</b>
          <ul>
            <li>Sentence length and variety</li>
            <li>Common polished-sounding phrases</li>
            <li>Personal-sounding language</li>
            <li>Repeated words and expressions</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    if analyze_clicked:
        result = analyze_text(text_value)
        if not result:
            st.warning("Psst! Paste some text first, then I'll take a look.")
        else:
            st.markdown("## 🎉 Your text report")
            cols = st.columns(4)
            with cols[0]: metric("Words", result["words"])
            with cols[1]: metric("Sentences", result["sentences"])
            with cols[2]: metric("Avg. sentence", result["avg_sentence"], "words")
            with cols[3]: metric("Vocabulary variety", f'{result["unique_ratio"]}%', "unique words")

            st.markdown('<div class="panel"><div class="panel-title">The pattern-o-meter</div>', unsafe_allow_html=True)
            st.progress(result["score"])
            if result["score"] >= 65:
                st.write(f'**Pattern score: {result["score"]}/100** — this sample contains several patterns often associated with polished, formulaic writing.')
            elif result["score"] <= 40:
                st.write(f'**Pattern score: {result["score"]}/100** — this sample contains some conversational or personal-language cues.')
            else:
                st.write(f'**Pattern score: {result["score"]}/100** — this sample has a mix of patterns.')
            st.caption("Important: this is a rough style indicator, NOT an AI detector. It cannot reliably determine who or what wrote the text.")
            st.markdown("</div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="panel"><div class="panel-title">🪄 Polished phrase clues</div>', unsafe_allow_html=True)
                if result["phrase_hits"]:
                    for phrase in result["phrase_hits"]:
                        st.write(f"• “{phrase}”")
                else:
                    st.write("No phrases from the small built-in list were found.")
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="panel"><div class="panel-title">💛 Personal voice clues</div>', unsafe_allow_html=True)
                if result["personal_hits"]:
                    for phrase in result["personal_hits"]:
                        st.write(f"• “{phrase}”")
                else:
                    st.write("No phrases from the small personal-language list were found.")
                st.markdown("</div>", unsafe_allow_html=True)

            if result["repeated"]:
                st.markdown('<div class="panel"><div class="panel-title">🔁 Words that repeat</div>', unsafe_allow_html=True)
                st.write(", ".join(f"**{word}** ({count}×)" for word, count in result["repeated"]))
                st.markdown("</div>", unsafe_allow_html=True)

            report = (
                "ORATORPULSE TEXT REPORT\n"
                f'Words: {result["words"]}\nSentences: {result["sentences"]}\n'
                f'Average sentence length: {result["avg_sentence"]}\n'
                f'Vocabulary variety: {result["unique_ratio"]}%\n'
                f'Pattern score (not AI probability): {result["score"]}/100\n'
                f'Polished phrase clues: {", ".join(result["phrase_hits"]) or "None"}\n'
                f'Personal voice clues: {", ".join(result["personal_hits"]) or "None"}\n'
            )
            st.download_button("⬇️ SAVE REPORT AS TXT", report, file_name="oratorpulse_report.txt")

with tab_detective:
    st.markdown('<div class="panel-title">🔎 The Repeat-O-Scope</div>', unsafe_allow_html=True)
    st.write("Upload a CSV or TXT file and Pip will help inspect the text. For a CSV, choose the column containing the writing.")
    uploaded = st.file_uploader("Choose a CSV or TXT file", type=["csv", "txt"])
    if uploaded:
        try:
            if uploaded.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded)
                st.dataframe(df.head(8), use_container_width=True)
                column = st.selectbox("Which column contains the text?", df.columns.tolist())
                combined = "\n".join(df[column].dropna().astype(str).tolist())
            else:
                combined = uploaded.getvalue().decode("utf-8", errors="replace")
            if st.button("🕵️ INSPECT FILE"):
                result = analyze_text(combined)
                if result:
                    st.success(f'Inspected {result["words"]} words across {result["sentences"]} sentences.')
                    st.write(f'Pattern score: **{result["score"]}/100** (not AI probability)')
                    if result["repeated"]:
                        st.write("Repeated words:", ", ".join(f"{w} ({c}×)" for w, c in result["repeated"]))
                    else:
                        st.write("No strong repeated-word patterns found.")
                else:
                    st.info("This file doesn't seem to contain text yet.")
        except Exception as exc:
            st.error(f"Couldn't read that file: {exc}")

with tab_about:
    st.markdown("""
    <div class="panel">
      <div class="panel-title">🎞️ How the little lab works</div>
      <p>This app uses a small set of transparent text rules. It counts words and sentences, checks for a short list of phrases, and notices a few personal-language cues.</p>
      <p><b>It does not connect to an AI model</b>, and it does not prove whether a human or AI wrote a passage. Human writing can sound formal; AI writing can sound personal. Treat the report as a writing-style checklist only.</p>
      <hr>
      <div class="panel-title">🖤 The visual recipe</div>
      <p>Original cute rubber-hose-inspired design: rounded silhouettes, simple smiling mascot, thick ink outlines, cream paper, black-and-white contrast, hand-drawn energy, and playful vintage typography. No villain mood, no yellow dots, no copied Bendy character.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<hr>
<div style="text-align:center;font-family:'Patrick Hand',cursive;font-size:18px">
Made with a little ink, a little bounce, and a whole lot of curiosity. ✦
</div>
""", unsafe_allow_html=True)
