
import re
import html
from collections import Counter

import pandas as pd
import streamlit as st


# ============================================================
# ORATORPULSE — THE VINTAGE CARTOON TEXT STUDIO
# ============================================================

st.set_page_config(
    page_title="OratorPulse | The Cartoon Text Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

INK = "#171717"
PAPER = "#F7F3E9"
WHITE = "#FFFEF8"
GRAY = "#E4E0D7"

SAMPLE_TEXT = (
    "I remember the first time I tried to explain an idea clearly. "
    "I thought a longer sentence would make my point stronger, but "
    "it often made the idea harder to follow. In my experience, "
    "simple words and specific examples help people understand what "
    "I mean. I want to keep improving, so I read my drafts aloud and "
    "notice where the rhythm feels awkward."
)


# ============================================================
# CSS — PAPER TEXTURE, VINTAGE FRAMES, CARTOON MOTION
# ============================================================

st.markdown(
    r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Nunito:wght@400;600;700;800;900&family=Rye&display=swap');

:root {
    --ink: #171717;
    --paper: #F7F3E9;
    --white: #FFFEF8;
    --gray: #E4E0D7;
    --muted: #69645b;
}

html, body, [class*="css"] {
    font-family: 'Nunito', system-ui, sans-serif;
    color: var(--ink);
}

.stApp {
    background-color: var(--paper);
    background-image:
        radial-gradient(ellipse at 12% 18%, rgba(23,23,23,.035) 0 1px, transparent 2px),
        radial-gradient(ellipse at 82% 71%, rgba(23,23,23,.03) 0 1px, transparent 2px);
    background-size: 31px 35px, 43px 47px;
}

[data-testid="stHeader"] {
    background: rgba(247,243,233,.94);
}

.block-container {
    max-width: 1320px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #ebe6da;
    border-right: 3px solid var(--ink);
}

h1, h2, h3 {
    color: var(--ink) !important;
}

h1 {
    font-family: 'Rye', Georgia, serif !important;
    font-size: clamp(2.4rem, 5vw, 4.4rem) !important;
    line-height: 1.08 !important;
}

h2, h3 {
    font-weight: 900 !important;
    letter-spacing: -.025em;
}

p, label, li {
    color: var(--ink);
}

.op-kicker {
    font: 500 .72rem 'DM Mono', monospace;
    letter-spacing: .13em;
    text-transform: uppercase;
    color: #625c52;
}

.op-title {
    font-family: 'Rye', Georgia, serif;
    font-size: clamp(2.6rem, 5.8vw, 4.8rem);
    line-height: 1.04;
    margin: .2rem 0 .8rem;
}

.op-subtitle {
    max-width: 650px;
    font-size: 1.08rem;
    line-height: 1.7;
    color: #4f4a43;
}

.op-panel {
    position: relative;
    background: var(--white);
    border: 3px solid var(--ink);
    border-radius: 18px 15px 20px 14px;
    padding: 20px;
    box-shadow: 5px 5px 0 var(--ink);
}

.op-panel:before {
    content: "";
    position: absolute;
    inset: 6px;
    border: 1px solid rgba(23,23,23,.13);
    border-radius: 12px;
    pointer-events: none;
}

.op-panel.cream {
    background: #eee8dc;
}

.op-tag {
    display: inline-block;
    border: 2px solid var(--ink);
    border-radius: 999px;
    background: #eee8dc;
    padding: 5px 10px;
    font: 500 .69rem 'DM Mono', monospace;
    letter-spacing: .04em;
}

.op-rule {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 26px 0 20px;
    font: 500 .72rem 'DM Mono', monospace;
    letter-spacing: .12em;
    color: #777064;
}

.op-rule:before, .op-rule:after {
    content: "";
    flex: 1;
    height: 2px;
    background: #b5aea0;
}

.op-speech {
    position: relative;
    background: var(--white);
    border: 2px solid var(--ink);
    border-radius: 17px;
    padding: 12px 15px;
    font-weight: 800;
    box-shadow: 3px 3px 0 var(--ink);
}

.op-metric {
    background: var(--white);
    border: 2.5px solid var(--ink);
    border-radius: 14px;
    padding: 14px;
    box-shadow: 3px 3px 0 var(--ink);
    animation: entrance .45s both;
}

.op-number {
    font-size: 2rem;
    line-height: 1.2;
    font-weight: 900;
}

.op-label {
    font-size: .73rem;
    text-transform: uppercase;
    letter-spacing: .07em;
    font-weight: 900;
    color: #625c52;
}

.op-note {
    padding: 13px 15px;
    background: #eee8dc;
    border-left: 5px solid var(--ink);
    border-radius: 0 12px 12px 0;
}

.op-character {
    display: block;
    width: 100%;
    max-width: 250px;
    height: auto;
    margin: auto;
    overflow: visible;
    filter: drop-shadow(3px 4px 0 rgba(23,23,23,.13));
}

.pip-idle {
    transform-origin: 50% 80%;
    animation: bounce 3.2s ease-in-out infinite;
}

.dot-idle {
    transform-origin: 50% 80%;
    animation: bounce 3.8s ease-in-out infinite reverse;
}

.inky-idle {
    transform-origin: 50% 80%;
    animation: squish 2.6s ease-in-out infinite;
}

.waving-arm {
    transform-origin: 78px 142px;
    animation: wave 2.5s ease-in-out infinite;
}

.blink {
    transform-box: fill-box;
    transform-origin: center;
    animation: blink 5.2s infinite;
}

.twinkle {
    transform-box: fill-box;
    transform-origin: center;
    animation: twinkle 2.2s ease-in-out infinite;
}

.wiggle:hover {
    animation: wobble .4s ease-in-out;
}

.stButton > button, .stDownloadButton > button {
    background: var(--white);
    color: var(--ink);
    border: 3px solid var(--ink);
    border-radius: 12px;
    font-weight: 900;
    box-shadow: 3px 3px 0 var(--ink);
    transition: transform .15s, box-shadow .15s, background .15s;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: #eee8dc;
    color: var(--ink);
    transform: translate(-2px,-2px) rotate(-.4deg);
    box-shadow: 5px 5px 0 var(--ink);
}

.stButton > button:active, .stDownloadButton > button:active {
    transform: translate(2px,2px);
    box-shadow: 1px 1px 0 var(--ink);
}

.stTextArea textarea, .stTextInput input {
    background: var(--white) !important;
    border: 2px solid var(--ink) !important;
    border-radius: 12px !important;
    color: var(--ink) !important;
    line-height: 1.65 !important;
}

[data-testid="stFileUploader"] section {
    background: var(--white);
    border: 2px dashed var(--ink);
    border-radius: 15px;
    transition: background .2s;
}

[data-testid="stFileUploader"] section:hover {
    background: #eee8dc;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 3px solid var(--ink);
}

.stTabs [data-baseweb="tab"] {
    background: #e9e3d7;
    border: 2px solid var(--ink);
    border-bottom: 0;
    border-radius: 12px 12px 0 0;
    padding: 10px 17px;
    font-weight: 900;
}

.stTabs [aria-selected="true"] {
    background: var(--white) !important;
}

.stProgress > div > div > div > div {
    background: var(--ink);
    transition: width .8s ease;
}

[data-testid="stAlert"] {
    border: 2px solid var(--ink);
    border-radius: 12px;
}

.op-footer {
    text-align: center;
    color: #777064;
    font: 500 .69rem 'DM Mono', monospace;
    letter-spacing: .1em;
}

@keyframes bounce {
    0%,100% { transform: translateY(0) rotate(-1deg); }
    50% { transform: translateY(-7px) rotate(1deg); }
}

@keyframes squish {
    0%,100% { transform: translateY(0) scaleX(1); }
    45% { transform: translateY(-5px) scaleX(1.04); }
}

@keyframes wave {
    0%,100% { transform: rotate(0); }
    35%,60% { transform: rotate(-20deg); }
}

@keyframes blink {
    0%,44%,48%,100% { transform: scaleY(1); }
    46% { transform: scaleY(.08); }
}

@keyframes twinkle {
    0%,100% { opacity: .35; transform: scale(.8) rotate(0); }
    50% { opacity: 1; transform: scale(1.15) rotate(12deg); }
}

@keyframes wobble {
    0%,100% { transform: rotate(0); }
    25% { transform: rotate(-2deg); }
    75% { transform: rotate(2deg); }
}

@keyframes entrance {
    from { opacity: 0; transform: translateY(12px) scale(.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@media(max-width: 700px) {
    .block-container { padding: 1rem .8rem 2rem; }
    .op-panel { padding: 15px; box-shadow: 3px 3px 0 var(--ink); }
    .op-title { font-size: 2.6rem; }
}

@media(prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# ORIGINAL SVG CHARACTERS
# ============================================================

def character_svg(kind="pip", pose="happy", height=250):
    """Draw an original vintage-inspired mascot using inline SVG."""
    if kind == "pip":
        head = """
        <path d="M64 56 Q49 30 74 20 Q90 10 108 24
        Q130 9 150 23 Q177 14 188 39 Q202 59 186 78
        L181 105 Q166 137 126 137 Q84 134 68 108Z"
        fill="#171717"/>
        """
        face = """
        <path d="M77 54 Q91 37 111 42 Q135 34 153 43
        Q175 39 177 62 L170 97 Q156 121 127 122
        Q95 120 81 97Z" fill="#fff"/>
        """
        eyes = """
        <path d="M86 65 Q90 49 104 49 Q119 50 120 68
        Q120 90 104 94 Q87 91 86 65Z" fill="#171717"/>
        <path d="M132 66 Q136 49 150 50 Q166 52 165 69
        Q164 91 149 94 Q132 90 132 66Z" fill="#171717"/>
        <ellipse class="blink" cx="105" cy="69" rx="11" ry="17" fill="#fff"/>
        <ellipse class="blink" cx="150" cy="69" rx="11" ry="17" fill="#fff"/>
        <ellipse cx="109" cy="75" rx="5.5" ry="9" fill="#171717"/>
        <ellipse cx="146" cy="75" rx="5.5" ry="9" fill="#171717"/>
        <circle cx="108" cy="70" r="3" fill="#fff"/>
        <circle cx="145" cy="70" r="3" fill="#fff"/>
        """
        mouth = """
        <path d="M91 102 Q127 133 163 101 Q157 135 127 137
        Q99 135 91 102Z" fill="#171717"/>
        <path d="M100 108 Q127 119 155 107 L151 119
        Q127 127 104 119Z" fill="#fff"/>
        <path d="M119 112 L119 122 M136 112 L136 122"
        stroke="#171717" stroke-width="2"/>
        """
        accessory = """
        <path d="M146 24 L157 8 L164 26Z" fill="#171717"/>
        <circle cx="157" cy="23" r="3" fill="#fff"/>
        """
        body_color = "#171717"

    elif kind == "dot":
        head = """
        <path d="M72 37 Q52 22 65 12 Q83 3 99 28
        Q122 17 146 28 Q172 12 189 32 Q205 52 185 75
        L183 105 Q174 136 127 137 Q81 135 73 107Z"
        fill="#e5dfd3" stroke="#171717" stroke-width="5"/>
        """
        face = """
        <path d="M81 54 Q102 41 126 47 Q153 40 176 55
        L170 98 Q158 120 128 122 Q96 120 84 98Z"
        fill="#fff" stroke="#171717" stroke-width="3"/>
        """
        eyes = """
        <path d="M91 62 Q99 50 110 56 Q121 62 119 77
        Q117 91 105 93 Q92 90 91 77Z" fill="#171717"/>
        <path d="M137 62 Q145 50 156 56 Q167 62 165 77
        Q163 91 151 93 Q138 90 137 77Z" fill="#171717"/>
        <ellipse cx="107" cy="69" rx="6" ry="10" fill="#fff"/>
        <ellipse cx="153" cy="69" rx="6" ry="10" fill="#fff"/>
        <circle cx="108" cy="67" r="2.5" fill="#171717"/>
        <circle cx="154" cy="67" r="2.5" fill="#171717"/>
        """
        mouth = """
        <path d="M105 103 Q127 116 151 101 Q144 126 126 124
        Q110 121 105 103Z" fill="#171717"/>
        <path d="M113 106 L141 106 L138 113 L117 113Z" fill="#fff"/>
        """
        accessory = """
        <path d="M87 43 L105 25 L123 43Z" fill="#171717"/>
        <circle cx="105" cy="37" r="4" fill="#fff"/>
        <circle cx="177" cy="32" r="9" fill="#171717"/>
        <circle cx="177" cy="32" r="4" fill="#fff"/>
        """
        body_color = "#e5dfd3"

    else:  # Inky has a completely different, rounded ink-drop silhouette.
        head = """
        <path d="M67 94 Q57 68 80 48 Q92 35 105 41
        Q124 22 144 40 Q175 43 184 73 Q195 102 171 122
        Q151 140 119 134 Q82 135 70 114Z"
        fill="#171717"/>
        """
        face = ""
        eyes = """
        <path d="M91 65 Q101 54 112 63 Q121 73 115 89
        Q108 100 98 91 Q88 83 91 65Z" fill="#fff"/>
        <path d="M135 64 Q145 53 156 63 Q165 73 159 89
        Q152 100 142 91 Q132 82 135 64Z" fill="#fff"/>
        <ellipse cx="107" cy="78" rx="5" ry="9" fill="#171717"/>
        <ellipse cx="150" cy="78" rx="5" ry="9" fill="#171717"/>
        <circle cx="105" cy="72" r="3" fill="#fff"/>
        <circle cx="148" cy="72" r="3" fill="#fff"/>
        """
        mouth = """
        <path d="M109 105 Q128 117 149 103 Q143 125 127 124
        Q112 121 109 105Z" fill="#fff"/>
        <path d="M127 108 L127 117" stroke="#171717" stroke-width="2"/>
        """
        accessory = """
        <path d="M76 60 Q55 42 73 31 Q90 25 100 45
        Q87 49 76 60Z" fill="#171717"/>
        <circle cx="78" cy="40" r="4" fill="#fff"/>
        """
        body_color = "#171717"

    # Pose-specific brows and expressions.
    extra = ""
    if pose == "thinking":
        extra = """
        <path d="M91 46 Q103 37 114 45 M138 45 Q150 35 162 44"
        fill="none" stroke="#171717" stroke-width="4"
        stroke-linecap="round"/>
        <path d="M193 22 Q207 7 217 21 Q224 32 211 39"
        fill="none" stroke="#171717" stroke-width="3"
        stroke-linecap="round"/>
        """
    elif pose == "surprised":
        extra = """
        <path d="M90 43 Q103 31 116 42 M138 42 Q151 30 164 42"
        fill="none" stroke="#171717" stroke-width="4"
        stroke-linecap="round"/>
        <ellipse cx="127" cy="113" rx="10" ry="13" fill="#171717"/>
        """
    elif pose == "confused":
        extra = """
        <path d="M91 43 Q104 39 114 45 M138 42 Q151 34 163 40"
        fill="none" stroke="#171717" stroke-width="4"
        stroke-linecap="round"/>
        <path d="M198 27 Q210 15 219 25"
        fill="none" stroke="#171717" stroke-width="3"/>
        """

    # Limbs, gloves, torso, and oversized shoes are separately drawn.
    if kind == "inky":
        legs = """
        <path d="M104 177 Q97 196 91 207 M148 177 Q155 194 162 207"
        fill="none" stroke="#171717" stroke-width="9"
        stroke-linecap="round"/>
        """
        arms = """
        <path d="M82 147 Q54 157 42 179 M171 147 Q194 157 207 178"
        fill="none" stroke="#171717" stroke-width="8"
        stroke-linecap="round"/>
        """
    else:
        legs = """
        <path d="M105 177 Q100 197 94 208 M149 177 Q153 196 161 207"
        fill="none" stroke="#171717" stroke-width="9"
        stroke-linecap="round"/>
        """
        arms = """
        <path d="M82 146 Q53 157 42 180 M171 146 Q194 157 207 178"
        fill="none" stroke="#171717" stroke-width="9"
        stroke-linecap="round"/>
        """

    body = f"""
    <path d="M91 132 Q127 145 164 132 L171 177
    Q128 193 84 177Z" fill="{body_color}"
    stroke="#171717" stroke-width="3"/>
    <path d="M108 142 L146 142 L141 164 L111 164Z"
    fill="#fff" stroke="#171717" stroke-width="2"/>
    """

    gloves = """
    <path d="M30 181 Q24 173 31 165 L38 171 L37 159
    Q40 153 45 159 L48 170 L53 163 Q60 161 59 169
    L56 181 Q50 193 39 190Z"
    fill="#fff" stroke="#171717" stroke-width="3"/>
    <path d="M195 179 Q188 171 194 164 L201 170 L200 158
    Q203 152 208 158 L211 169 L216 162 Q223 160 222 168
    L219 180 Q213 192 202 189Z"
    fill="#fff" stroke="#171717" stroke-width="3"/>
    """

    shoes = """
    <path d="M75 207 Q92 197 104 209 Q111 222 91 226
    L67 224 Q57 219 75 207Z" fill="#171717"/>
    <path d="M147 208 Q162 197 176 208 Q186 221 167 226
    L145 224 Q136 219 147 208Z" fill="#171717"/>
    <path d="M73 217 L96 218 M150 217 L173 218"
    stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>
    """

    spark = """
    <path class="twinkle"
    d="M204 47 L209 58 L220 62 L209 68 L205 80
    L199 69 L188 66 L199 59Z" fill="#171717"/>
    """

    animation_class = {
        "pip": "pip-idle",
        "dot": "dot-idle",
        "inky": "inky-idle",
    }[kind]

    labels = {
        "pip": "Pip, cheerful cartoon host",
        "dot": "Dot, curious cartoon detective",
        "inky": "Inky, playful little ink creature",
    }

    return f"""
    <svg class="op-character {animation_class}"
         style="max-height:{height}px"
         viewBox="0 0 250 240"
         role="img"
         aria-label="{labels[kind]}"
         xmlns="http://www.w3.org/2000/svg">
      <g stroke-linecap="round" stroke-linejoin="round">
        {legs}
        {arms}
        {body}
        {head}
        {face}
        {eyes}
        {mouth}
        {accessory}
        {extra}
        {gloves}
        {shoes}
        {spark}
      </g>
    </svg>
    """


# ============================================================
# TEXT ANALYSIS ENGINE
# ============================================================

POLISHED_PHRASES = [
    "in today's fast-paced world",
    "it is important to note",
    "delve into",
    "plays a crucial role",
    "in conclusion",
    "moreover",
    "furthermore",
    "it is worth noting",
    "a testament to",
    "multifaceted",
    "navigate the complexities",
    "in the realm of",
    "at the end of the day",
]

PERSONAL_CUES = [
    "i think",
    "i believe",
    "in my experience",
    "i noticed",
    "i learned",
    "i remember",
    "for me",
    "i prefer",
    "i feel",
    "my goal",
    "i want",
    "i tried",
    "i found",
    "i realized",
    "i chose",
]

STOP_WORDS = {
    "the", "and", "that", "with", "for", "this", "are", "was",
    "but", "you", "your", "from", "have", "has", "they", "their",
    "then", "when", "what", "not", "can", "will", "would", "there",
    "been", "were", "into", "its", "our", "out", "about", "which",
}


def analyze_text(text):
    """Return transparent text statistics and simple rule-based signals."""
    words = re.findall(r"\b[\w’'-]+\b", text.lower(), flags=re.UNICODE)

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]

    word_count = len(words)
    sentence_count = len(sentences)

    unique_words = set(words)
    vocabulary_variety = (
        round(len(unique_words) / word_count * 100)
        if word_count else 0
    )

    average_sentence_length = (
        round(word_count / sentence_count, 1)
        if sentence_count else 0
    )

    counts = Counter(
        word.strip("'-’")
        for word in words
        if len(word.strip("'-’")) >= 3
    )

    repeated_words = [
        (word, count)
        for word, count in counts.most_common()
        if count > 1 and word not in STOP_WORDS
    ][:12]

    lower_text = text.lower()

    polished_found = [
        phrase for phrase in POLISHED_PHRASES
        if phrase in lower_text
    ]

    personal_found = [
        phrase for phrase in PERSONAL_CUES
        if phrase in lower_text
    ]

    # This is a simple heuristic, not an AI probability.
    score = min(
        100,
        round(
            len(polished_found) * 12
            + max(0, average_sentence_length - 22) * 1.4
            + max(0, 42 - vocabulary_variety) * 0.7
            + len(repeated_words) * 1.5
        ),
    )

    return {
        "words": word_count,
        "sentences": sentence_count,
        "average": average_sentence_length,
        "variety": vocabulary_variety,
        "polished": polished_found,
        "personal": personal_found,
        "repeated": repeated_words,
        "score": score,
    }


# ============================================================
# REUSABLE UI COMPONENTS
# ============================================================

def metric(value, label, delay=0):
    st.markdown(
        f"""
        <div class="op-metric" style="animation-delay:{delay}ms">
            <div class="op-number">{html.escape(str(value))}</div>
            <div class="op-label">{html.escape(label)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_rule(text):
    st.markdown(
        f'<div class="op-rule">{html.escape(text)}</div>',
        unsafe_allow_html=True,
    )


def make_report(result, title="ORATORPULSE TEXT REPORT"):
    repeated = (
        ", ".join(f"{word} ({count})"
                  for word, count in result["repeated"])
        or "None found"
    )

    return "\n".join([
        title,
        "=" * len(title),
        f"Word count: {result['words']}",
        f"Sentence count: {result['sentences']}",
        f"Average sentence length: {result['average']}",
        f"Vocabulary variety: {result['variety']}%",
        f"Pattern score (heuristic): {result['score']}/100",
        "",
        "Polished-sounding phrases:",
        ", ".join(result["polished"]) or "None found",
        "",
        "Personal-language cues:",
        ", ".join(result["personal"]) or "None found",
        "",
        "Repeated words:",
        repeated,
        "",
        "LIMITATION:",
        "Rule-based clues only. Not an AI detector or authorship verdict.",
    ])


def render_results(result, report_name="oratorpulse_report.txt"):
    section_rule("THE CREW'S NOTEBOOK")

    columns = st.columns(4)

    metrics = [
        (result["words"], "Word count"),
        (result["sentences"], "Sentences"),
        (result["average"], "Words / sentence"),
        (f'{result["variety"]}%', "Vocabulary variety"),
    ]

    for index, (value, label) in enumerate(metrics):
        with columns[index]:
            metric(value, label, index * 90)

    st.write("")

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            '<div class="op-panel"><h3>Pattern score</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="op-number">{result["score"]}'
            '<span style="font-size:1rem"> / 100</span></div>',
            unsafe_allow_html=True,
        )
        st.progress(result["score"])
        st.caption(
            "A small rule-based indicator. It is not a probability, "
            "a validated detector, or proof of authorship."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="op-panel cream">',
            unsafe_allow_html=True,
        )

        if result["score"] >= 35:
            st.markdown(character_svg("pip", "thinking", 150),
                        unsafe_allow_html=True)
            st.markdown("### Pip is taking a closer look")
            st.write(
                "Some patterns stood out in this checklist. "
                "Review the details and context before drawing conclusions."
            )
        else:
            st.markdown(character_svg("pip", "happy", 150),
                        unsafe_allow_html=True)
            st.markdown("### Pip has made a note")
            st.write(
                "The simple checklist found fewer signals. "
                "That does not establish who wrote the text."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            '<div class="op-panel"><h3>Polished-sounding phrases</h3>',
            unsafe_allow_html=True,
        )

        if result["polished"]:
            for phrase in result["polished"]:
                st.markdown(f"- `{phrase}`")
        else:
            st.write("No matches from the predefined phrase list.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.markdown(
            '<div class="op-panel"><h3>Repeated words</h3>',
            unsafe_allow_html=True,
        )

        if result["repeated"]:
            repeated_df = pd.DataFrame(
                result["repeated"],
                columns=["Word", "Count"],
            )
            st.dataframe(
                repeated_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("No notable repeated words were found.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="op-panel"><h3>Personal-language cues</h3>',
            unsafe_allow_html=True,
        )

        if result["personal"]:
            for phrase in result["personal"]:
                st.markdown(f"- `{phrase}`")
        else:
            st.write("No matches from the predefined cue list.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.download_button(
            "Download TXT report",
            data=make_report(result),
            file_name=report_name,
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# SESSION STATE — APPLY PENDING VALUES BEFORE CREATING WIDGETS
# ============================================================

if "draft_text" not in st.session_state:
    st.session_state.draft_text = ""

if "pending_text" in st.session_state:
    st.session_state.draft_text = st.session_state.pop("pending_text")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "detective_result" not in st.session_state:
    st.session_state.detective_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ORATORPULSE")
    st.markdown(
        '<div class="op-kicker">THE LITTLE CARTOON STUDIO</div>',
        unsafe_allow_html=True,
    )

    st.markdown(character_svg("inky", "happy", 155),
                unsafe_allow_html=True)

    st.markdown("**A curious little writing workshop.**")
    st.caption(
        "Explore language patterns, not a verdict on who wrote a text."
    )

    st.divider()

    st.markdown("### Your workbenches")
    st.markdown("**Text Lab** — inspect a passage")
    st.markdown("**Pattern Detective** — explore CSV or TXT files")
    st.markdown("**How it works** — understand the clues")

    st.divider()

    st.markdown(
        '<div class="op-footer">INK · PAPER · CURIOSITY</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HERO SCENE
# ============================================================

hero_left, hero_right = st.columns(
    [1.3, 1],
    gap="large",
    vertical_alignment="center",
)

with hero_left:
    st.markdown(
        '<div class="op-kicker">A HAND-DRAWN WRITING WORKSHOP</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="op-title">OratorPulse</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="op-subtitle">
        Step into a tiny vintage cartoon studio where curious characters
        inspect the patterns hiding in everyday writing. Bring a passage,
        meet the crew, and explore the clues for yourself.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
        <span class="op-tag">NO API KEYS</span>
        &nbsp; <span class="op-tag">RULE-BASED CLUES</span>
        &nbsp; <span class="op-tag">TRANSPARENT RESULTS</span>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        '<div class="op-panel cream" style="text-align:center">',
        unsafe_allow_html=True,
    )

    st.markdown(character_svg("pip", "happy", 300),
                unsafe_allow_html=True)

    st.markdown(
        '<div class="op-speech">'
        '“Well, hello there! Shall we investigate some words?”'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CHARACTER LINEUP
# ============================================================

section_rule("MEET YOUR STUDIO CREW")

crew = st.columns(3, gap="medium")

characters = [
    (
        "pip",
        "Pip",
        "THE CHEERFUL HOST",
        "“Every sentence has a little story.”",
        "Curious, welcoming, and always ready to help.",
    ),
    (
        "dot",
        "Dot",
        "THE PATTERN DETECTIVE",
        "“Aha! Let's look a little closer.”",
        "Clever, patient, and a fan of tiny details.",
    ),
    (
        "inky",
        "Inky",
        "THE PLAYFUL INK DROP",
        "“Boing! I found a repeat!”",
        "Silly, bouncy, and never short on enthusiasm.",
    ),
]

for col, (kind, name, role, quote, description) in zip(crew, characters):
    with col:
        st.markdown(
            '<div class="op-panel wiggle" style="text-align:center">',
            unsafe_allow_html=True,
        )

        st.markdown(character_svg(kind, "happy", 190),
                    unsafe_allow_html=True)

        st.markdown(f"### {name}")

        st.markdown(
            f'<div class="op-kicker">{role}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(f"*{quote}*")
        st.caption(description)

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# APPLICATION TABS
# ============================================================

section_rule("CHOOSE YOUR WORKBENCH")

text_tab, detective_tab, about_tab = st.tabs([
    "Text Lab",
    "Pattern Detective",
    "How it works",
])


# ============================================================
# TEXT LAB
# ============================================================

with text_tab:
    left, right = st.columns([1.35, .65], gap="large")

    with left:
        st.markdown("## The writing desk")
        st.write(
            "Paste a passage or try the example. "
            "The crew will inspect a few visible language patterns."
        )

        button_a, button_b = st.columns(2)

        with button_a:
            if st.button("Try example text", use_container_width=True):
                st.session_state.pending_text = SAMPLE_TEXT
                st.session_state.analysis_result = None
                st.rerun()

        with button_b:
            if st.button("Clear the desk", use_container_width=True):
                st.session_state.pending_text = ""
                st.session_state.analysis_result = None
                st.rerun()

        # IMPORTANT: pending_text is applied before this widget is created.
        passage = st.text_area(
            "Your passage",
            key="draft_text",
            height=250,
            placeholder=(
                "Once upon a sentence... paste your writing here."
            ),
        )

        analyze_button = st.button(
            "Inspect my text",
            type="primary",
            use_container_width=True,
        )

        if analyze_button:
            if not passage.strip():
                st.session_state.analysis_result = None
                st.warning(
                    "Pip found an empty page! Add some text first."
                )
            else:
                st.session_state.analysis_result = analyze_text(passage)
                st.success(
                    "The crew has finished its first inspection."
                )

    with right:
        st.markdown(
            '<div class="op-panel cream" style="text-align:center">',
            unsafe_allow_html=True,
        )

        st.markdown(
            character_svg(
                "dot",
                "thinking" if analyze_button else "happy",
                215,
            ),
            unsafe_allow_html=True,
        )

        st.markdown("### Dot's checklist")

        st.markdown(
            '<div class="op-speech">'
            '“Patterns are clues, not proof!”'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("")
        st.markdown("**What Dot checks**")
        st.markdown("- Sentence length")
        st.markdown("- Vocabulary variety")
        st.markdown("- Predefined phrases")
        st.markdown("- Personal-language cues")
        st.markdown("- Repeated words")

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.analysis_result:
        render_results(st.session_state.analysis_result)


# ============================================================
# PATTERN DETECTIVE — CSV AND TXT
# ============================================================

with detective_tab:
    left, right = st.columns([1.15, .85], gap="large")

    with left:
        st.markdown("## Dot's detective desk")

        st.write(
            "Upload a CSV or TXT file. CSV files can be previewed, "
            "and you can choose which text column to inspect."
        )

        uploaded = st.file_uploader(
            "Drop your CSV or TXT file here",
            type=["csv", "txt"],
            key="detective_upload",
        )

        if uploaded is not None:
            try:
                if uploaded.name.lower().endswith(".csv"):
                    dataframe = pd.read_csv(uploaded)

                    st.markdown("### Evidence preview")

                    st.dataframe(
                        dataframe.head(10),
                        use_container_width=True,
                        hide_index=True,
                    )

                    text_columns = list(
                        dataframe.select_dtypes(
                            include=["object", "string"]
                        ).columns
                    )

                    if not text_columns:
                        st.error(
                            "No text columns were found in this CSV."
                        )
                    else:
                        selected_column = st.selectbox(
                            "Choose the text column",
                            options=text_columns,
                        )

                        if st.button(
                            "Inspect selected column",
                            use_container_width=True,
                        ):
                            combined_text = "\n".join(
                                dataframe[selected_column]
                                .dropna()
                                .astype(str)
                                .tolist()
                            )

                            if not combined_text.strip():
                                st.warning(
                                    "This column contains no usable text."
                                )
                            else:
                                st.session_state.detective_result = (
                                    analyze_text(combined_text)
                                )

                                st.session_state.detective_report_text = (
                                    combined_text
                                )

                                st.success(
                                    "Dot has finished inspecting the column."
                                )

                else:
                    content = uploaded.getvalue().decode(
                        "utf-8-sig",
                        errors="replace",
                    )

                    st.markdown("### Evidence preview")

                    preview = content[:2500]

                    st.text_area(
                        "TXT preview",
                        value=preview,
                        height=180,
                        disabled=True,
                    )

                    if len(content) > 2500:
                        st.caption("Preview shortened to 2,500 characters.")

                    if st.button(
                        "Inspect TXT file",
                        use_container_width=True,
                    ):
                        if not content.strip():
                            st.warning("This file appears to be empty.")
                        else:
                            st.session_state.detective_result = (
                                analyze_text(content)
                            )

                            st.session_state.detective_report_text = content

                            st.success(
                                "Dot has finished inspecting the TXT file."
                            )

            except Exception as error:
                st.error(
                    "Dot couldn't read this file. "
                    f"Check the file format and try again. Details: {error}"
                )

    with right:
        st.markdown(
            '<div class="op-panel cream" style="text-align:center">',
            unsafe_allow_html=True,
        )

        st.markdown(
            character_svg("dot", "thinking", 235),
            unsafe_allow_html=True,
        )

        st.markdown("### Evidence, not verdicts")

        st.write(
            "Dot looks for simple textual patterns. "
            "This application uses Python rules and does not call "
            "an external AI service."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.detective_result:
        render_results(
            st.session_state.detective_result,
            report_name="oratorpulse_detective_report.txt",
        )


# ============================================================
# ABOUT — METHOD AND LIMITATIONS
# ============================================================

with about_tab:
    st.markdown("## How the studio works")

    st.write(
        "OratorPulse is a small, transparent checklist. "
        "It does not claim to identify the author of a passage."
    )

    steps = st.columns(3, gap="medium")

    step_data = [
        (
            "pip",
            "01 — Count",
            "Count words and split text into sentences using simple rules.",
        ),
        (
            "dot",
            "02 — Compare",
            "Check a predefined list of phrases, personal cues, "
            "and repeated words.",
        ),
        (
            "inky",
            "03 — Reflect",
            "Summarize a few signals with a heuristic score. "
            "Use it as a prompt to review the text.",
        ),
    ]

    for col, (kind, title, description) in zip(steps, step_data):
        with col:
            st.markdown(
                '<div class="op-panel" style="text-align:center">',
                unsafe_allow_html=True,
            )

            st.markdown(
                character_svg(kind, "happy", 160),
                unsafe_allow_html=True,
            )

            st.markdown(f"### {title}")
            st.write(description)

            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="op-panel"><h3>What this cannot tell you</h3>',
        unsafe_allow_html=True,
    )

    st.markdown("""
- **It cannot establish authorship.** Human and AI-written text can
  share the same characteristics.
- **The score is not a probability.** It is a hand-built heuristic,
  not a validated AI-detection model.
- **Context matters.** Genre, language background, topic, and editing
  can affect the patterns.
- **A missing signal proves nothing.** The predefined lists are limited.
- **Review the actual text.** Treat the results as a starting point,
  not a final judgement.
""")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.markdown(
    """
    <div class="op-footer">
        MADE OF INK, PAPER & A HEALTHY DOSE OF CURIOSITY
        <br><br>
        ORATORPULSE · VINTAGE CARTOON TEXT STUDIO
    </div>
    """,
    unsafe_allow_html=True,
)
