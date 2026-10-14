from __future__ import annotations

import io
import math
import re
from collections import Counter
from html import escape
from typing import Iterable

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="OratorPulse — The Friendly Ink Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Analysis engine
# -----------------------------
POLISHED_PHRASES = [
    "in conclusion", "it is important to note", "delve into", "a testament to",
    "plays a crucial role", "at the end of the day", "leverage", "robust solution",
    "paradigm shift", "seamless experience", "unlock the potential", "furthermore",
]
PERSONAL_CUES = [
    "i think", "i believe", "in my opinion", "i feel", "my experience", "we believe",
    "our team", "for me", "i noticed", "i learned", "i remember", "we found",
]
STOPWORDS = set("a an the and or but if then than so for to of in on at by with from as is are was were be been it this that these those i you he she we they them my our your their do does did have has had not no very really just about into over under more most can could should would will also there here when where how what which who why".split())


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w’'-]+\b", text.lower())


def analyze_text(text: str) -> dict:
    clean = text.strip()
    tokens = words(clean)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", clean) if s.strip()]
    content_words = [w for w in tokens if w not in STOPWORDS and len(w) > 2]
    counts = Counter(tokens)
    repeats = [(w, n) for w, n in counts.most_common() if n > 1 and w not in STOPWORDS and len(w) > 2]
    phrase_hits = [p for p in POLISHED_PHRASES if p in clean.lower()]
    cue_hits = [p for p in PERSONAL_CUES if p in clean.lower()]
    wc = len(tokens)
    sc = len(sentences)
    avg = (wc / sc) if sc else 0
    variety = (len(set(tokens)) / wc * 100) if wc else 0
    pattern = min(100, round((len(phrase_hits) * 13) + (len(cue_hits) * 9) + max(0, avg - 16) * 1.8))
    return {
        "word_count": wc,
        "sentence_count": sc,
        "avg_sentence": avg,
        "vocabulary": variety,
        "pattern_score": pattern,
        "polished": phrase_hits,
        "personal": cue_hits,
        "repeated": repeats[:10],
        "content_words": len(content_words),
    }


def report_text(text: str, result: dict) -> str:
    lines = [
        "ORATORPULSE — INK STUDIO REPORT",
        "=" * 36,
        "This is a rule-based language sketch, not a scientific or AI-authorship verdict.",
        "",
        f"Words: {result['word_count']}",
        f"Sentences: {result['sentence_count']}",
        f"Average sentence length: {result['avg_sentence']:.1f} words",
        f"Vocabulary variety: {result['vocabulary']:.1f}%",
        f"Pattern score: {result['pattern_score']}/100",
        f"Polished-sounding phrases: {', '.join(result['polished']) or 'None spotted'}",
        f"Personal-language cues: {', '.join(result['personal']) or 'None spotted'}",
        f"Repeated words: {', '.join(f'{w} ({n})' for w, n in result['repeated']) or 'None spotted'}",
        "",
        "Keep the useful clues, question the certainty, and trust your own voice.",
    ]
    return "\n".join(lines)


# -----------------------------
# Original SVG cast
# -----------------------------
def pip_svg(state: str = "happy", size: str = "large") -> str:
    cls = f"character pip {state} {size}"
    mouth = '<path class="smile" d="M102 151 Q145 185 188 151 Q180 196 145 198 Q110 196 102 151Z"/><path class="teeth" d="M112 164 Q145 180 178 164 L174 177 Q145 187 116 177Z"/>'
    if state == "thinking":
        mouth = '<path class="smile" d="M122 176 Q146 187 169 174"/>'
    elif state == "surprised":
        mouth = '<ellipse class="mouth" cx="145" cy="174" rx="21" ry="28"/>'
    elif state == "confused":
        mouth = '<path class="smile" d="M120 179 Q146 162 170 180"/>'
    return f'''<svg class="{cls}" viewBox="0 0 290 360" role="img" aria-label="Pip, cheerful host cartoon character">
      <g class="pip-body"><path class="hose arm left" d="M82 214 Q34 224 48 275"/><path class="hose arm right" d="M207 215 Q258 205 246 265"/>
      <path class="glove left" d="M39 268 q-16-18-27 0 l8 7-7 11 13 2-1 12 12-5 7 9 8-12 11 2-4-13 8-9z"/>
      <path class="glove right" d="M242 260 q16-19 27-2 l-7 8 8 10-13 2 1 12-12-5-7 9-8-12-11 2 4-13-8-9z"/>
      <path class="hose leg left" d="M116 273 Q93 316 77 324"/><path class="hose leg right" d="M174 273 Q198 313 218 322"/>
      <path class="shoe" d="M45 315 Q77 298 104 319 Q106 342 65 344 Q33 340 45 315Z"/><path class="shoe" d="M189 318 Q220 299 247 320 Q250 342 211 344 Q180 341 189 318Z"/>
      <path class="head" d="M70 95 Q72 36 145 34 Q218 36 220 101 L207 215 Q184 257 145 262 Q104 257 82 215Z"/>
      <path class="ear" d="M76 109 Q43 99 54 132 Q62 148 82 143"/><path class="ear" d="M214 109 Q247 99 236 132 Q228 148 208 143"/>
      <path class="cap" d="M76 83 Q105 19 164 39 Q190 23 215 80 Q170 65 76 83Z"/><path class="cap-line" d="M92 66 Q145 50 201 68"/>
      <g class="eyes"><path class="eye white" d="M91 112 Q111 91 132 112 Q128 151 103 151 Q88 143 91 112Z"/><path class="eye white" d="M158 112 Q179 91 199 112 Q202 143 187 151 Q162 151 158 112Z"/><ellipse class="pupil" cx="116" cy="124" rx="9" ry="17"/><ellipse class="pupil" cx="179" cy="124" rx="9" ry="17"/><circle class="highlight" cx="120" cy="117" r="4"/><circle class="highlight" cx="183" cy="117" r="4"/></g>
      <path class="brow" d="M94 94 Q112 82 128 91"/><path class="brow" d="M163 91 Q181 82 198 94"/>{mouth}
      <path class="bow" d="M140 220 l-25-13 9 25 16-8 16 8 9-25z"/></g></svg>'''


def dot_svg(state: str = "curious") -> str:
    mouth = '<path class="smile" d="M111 166 Q145 190 180 166"/><path class="teeth" d="M122 174 Q145 184 170 174 L166 182 Q145 188 126 182Z"/>'
    if state == "thinking":
        mouth = '<path class="smile" d="M125 181 Q147 168 168 181"/>'
    return f'''<svg class="character dot" viewBox="0 0 290 360" role="img" aria-label="Dot, curious detective cartoon character">
      <g><path class="hose arm left" d="M82 220 Q37 238 45 276"/><path class="hose arm right" d="M205 220 Q255 232 244 272"/><path class="glove left" d="M40 272 q-17-17-27 2 l9 6-7 11 13 1-1 12 12-6 8 9 7-12 11 2-4-13 8-8z"/><path class="glove right" d="M242 269 q15-19 27 0 l-8 8 8 10-13 2 2 12-13-6-7 9-8-12-11 2 4-13-8-9z"/><path class="hose leg" d="M115 274 Q98 318 78 326"/><path class="hose leg" d="M176 274 Q198 318 221 325"/><path class="shoe" d="M43 319 Q74 301 104 320 Q105 343 65 344 Q32 341 43 319Z"/><path class="shoe" d="M194 319 Q226 302 249 322 Q249 344 211 344 Q181 341 194 319Z"/>
      <path class="head dot-head" d="M74 93 Q86 40 145 37 Q205 39 218 94 L205 218 Q181 256 145 260 Q107 255 84 218Z"/><path class="hair" d="M84 85 Q94 30 110 57 Q130 22 145 58 Q163 22 176 61 Q202 32 208 86"/><g class="eyes"><path class="eye white" d="M91 119 Q111 97 134 114 Q132 149 105 152 Q88 143 91 119Z"/><path class="eye white" d="M156 114 Q179 97 199 119 Q202 143 185 152 Q158 149 156 114Z"/><ellipse class="pupil" cx="116" cy="124" rx="8" ry="16"/><ellipse class="pupil" cx="178" cy="124" rx="8" ry="16"/><circle class="highlight" cx="119" cy="118" r="4"/><circle class="highlight" cx="181" cy="118" r="4"/></g><path class="brow" d="M95 99 Q112 88 130 95"/><path class="brow" d="M162 95 Q180 88 196 99"/>{mouth}<path class="bow" d="M124 217 Q145 205 166 217 Q145 235 124 217Z"/><path class="magnify" d="M196 185 l26 25 M183 172 a22 22 0 1 0 31 31 a22 22 0 1 0-31-31"/></g></svg>'''


def inky_svg(state: str = "happy") -> str:
    mouth = '<path class="smile" d="M109 155 Q145 182 181 155 Q174 191 145 192 Q116 191 109 155Z"/><path class="teeth" d="M120 165 Q145 177 171 165 L167 175 Q145 181 123 175Z"/>'
    return f'''<svg class="character inky {state}" viewBox="0 0 290 360" role="img" aria-label="Inky, playful little ink creature">
      <g><path class="ink-body" d="M71 217 Q46 190 62 151 Q54 102 94 81 Q124 43 163 70 Q208 62 222 105 Q248 143 224 180 Q241 218 206 242 Q186 274 145 258 Q106 275 84 245 Q62 243 71 217Z"/><path class="hose arm left" d="M78 205 Q34 220 46 260"/><path class="hose arm right" d="M212 201 Q255 216 244 257"/><path class="glove left" d="M40 256 q-16-17-27 1 l8 8-7 11 13 1-1 12 12-6 8 9 7-12 11 2-4-13 8-8z"/><path class="glove right" d="M242 254 q15-19 27 0 l-8 8 8 10-13 2 2 12-13-6-7 9-8-12-11 2 4-13-8-9z"/><path class="ink-leg" d="M112 246 Q104 294 80 315"/><path class="ink-leg" d="M179 245 Q189 294 215 315"/><path class="shoe" d="M48 307 Q79 291 107 313 Q105 337 68 338 Q38 336 48 307Z"/><path class="shoe" d="M184 313 Q215 291 244 311 Q250 337 212 339 Q181 338 184 313Z"/><g class="eyes"><path class="eye white" d="M91 125 Q109 101 133 119 Q132 147 107 151 Q88 143 91 125Z"/><path class="eye white" d="M157 119 Q181 101 199 125 Q202 143 183 151 Q158 147 157 119Z"/><ellipse class="pupil" cx="115" cy="128" rx="8" ry="14"/><ellipse class="pupil" cx="177" cy="128" rx="8" ry="14"/><circle class="highlight" cx="118" cy="123" r="4"/><circle class="highlight" cx="180" cy="123" r="4"/></g>{mouth}<path class="ink-spark" d="M62 112 l-15-13 M220 102 l15-15 M59 183 l-20 3"/></g></svg>'''


# -----------------------------
# Interface styling and components
# -----------------------------
CSS = r'''<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=DM+Mono:wght@400;500&family=Rye&display=swap');
:root{--ink:#171717;--paper:#f7f3e9;--white:#fffef8;--gray:#e4e0d7;--red:#b84b3e;--blue:#4c7180;}
.stApp{background:var(--paper);color:var(--ink);font-family:'Baloo 2',system-ui,sans-serif;background-image:radial-gradient(ellipse at 15% 8%,rgba(23,23,23,.045) 0 1px,transparent 2px),radial-gradient(ellipse at 80% 76%,rgba(23,23,23,.035) 0 1px,transparent 2px);background-size:37px 41px,53px 47px}
.block-container{max-width:1240px;padding:2rem 2.5rem 4rem}
h1,h2,h3{font-family:'Rye','Georgia',serif;letter-spacing:.02em;color:var(--ink)}
h1{font-size:clamp(3rem,7vw,6.8rem);line-height:.93;margin:.1rem 0 .8rem;text-shadow:4px 4px 0 var(--gray)}
h2{font-size:clamp(1.6rem,3vw,2.6rem)}
p,.stMarkdown{font-size:1.05rem;line-height:1.5}
.hero{position:relative;overflow:hidden;min-height:450px;padding:3.2rem 3.8rem 2.5rem;border:4px solid var(--ink);border-radius:34px 22px 40px 24px;background:var(--white);box-shadow:11px 12px 0 var(--ink);isolation:isolate}
.hero:before{content:'';position:absolute;inset:13px;border:2px solid var(--ink);border-radius:26px 16px 31px 19px;pointer-events:none}
.hero-copy{position:relative;z-index:2;max-width:62%}.kicker{font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.14em;font-size:.78rem}.tagline{font-size:1.35rem;max-width:520px}.hero-art{position:absolute;right:2%;bottom:-34px;width:38%;min-width:260px;z-index:1}.cameo{position:absolute;width:90px;opacity:.9}.cameo.dot{right:27%;top:7%;transform:rotate(-8deg)}.cameo.inky{right:7%;top:19%;transform:rotate(8deg)}
.star{position:absolute;font-size:2rem;animation:twinkle 2.7s ease-in-out infinite}.star.s1{right:42%;top:17%}.star.s2{right:8%;bottom:13%;animation-delay:.9s}.star.s3{left:47%;bottom:10%;animation-delay:1.4s}.ink-line{height:14px;margin:2.2rem 0;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='14' viewBox='0 0 300 14'%3E%3Cpath d='M0 7 Q35 1 70 7 T140 7 T210 7 T300 7' fill='none' stroke='%23171717' stroke-width='3'/%3E%3C/svg%3E") center/100% 100% no-repeat}
.stButton>button{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:1.05rem;color:var(--white);background:var(--ink);border:3px solid var(--ink);border-radius:12px 18px 10px 15px;padding:.55rem 1.25rem;box-shadow:4px 5px 0 var(--red);transition:transform .16s,box-shadow .16s}.stButton>button:hover{transform:translate(-2px,-2px) rotate(-1deg);box-shadow:6px 7px 0 var(--red);color:var(--white)}.stButton>button:active{transform:translate(3px,3px);box-shadow:1px 2px 0 var(--red)}
.panel{background:var(--white);border:3px solid var(--ink);border-radius:18px 27px 20px 13px;padding:1.35rem 1.5rem;box-shadow:6px 7px 0 var(--gray);height:100%;transition:transform .2s,box-shadow .2s}.panel:hover{transform:translateY(-4px) rotate(-.4deg);box-shadow:8px 10px 0 var(--gray)}.panel h3{font-family:'Rye','Georgia',serif;font-size:1.25rem;margin:.2rem 0 .5rem}.dialogue{font-style:italic;border-left:4px solid var(--red);padding-left:.8rem}.character{width:100%;height:auto;overflow:visible}.cast-card{min-height:370px}.cast-card .character{height:245px}.cast-card.pip-card{background:#f8f5ed}.cast-card.dot-card{background:#edf1ec}.cast-card.inky-card{background:#e9e8e3}
svg .head,svg .dot-head{fill:var(--white);stroke:var(--ink);stroke-width:7;stroke-linejoin:round}svg .ink-body{fill:var(--ink);stroke:var(--ink);stroke-width:7}svg .ear,svg .cap,svg .hair,svg .shoe,svg .bow{fill:var(--ink);stroke:var(--ink);stroke-width:6;stroke-linejoin:round}svg .cap-line,svg .brow,svg .smile{fill:none;stroke:var(--white);stroke-width:6;stroke-linecap:round}svg .brow,svg .smile{stroke:var(--ink)}svg .eye.white{fill:var(--white);stroke:var(--ink);stroke-width:5}svg .pupil{fill:var(--ink)}svg .highlight{fill:var(--white)}svg .teeth{fill:var(--white);stroke:var(--ink);stroke-width:3}svg .mouth{fill:var(--ink);stroke:var(--ink);stroke-width:4}svg .hose,svg .ink-leg{fill:none;stroke:var(--ink);stroke-width:12;stroke-linecap:round}svg .glove{fill:var(--white);stroke:var(--ink);stroke-width:5;stroke-linejoin:round}svg .magnify{fill:none;stroke:var(--red);stroke-width:7;stroke-linecap:round}svg .ink-spark{fill:none;stroke:var(--white);stroke-width:4;stroke-linecap:round}
.pip{animation:breathe 4s ease-in-out infinite}.dot{animation:breathe 4.7s ease-in-out infinite .4s}.inky{animation:breathe 3.6s ease-in-out infinite .8s}.character:hover{animation:wobble .65s ease-in-out both}.pip .arm.right,.dot .arm.right,.inky .arm.right{transform-origin:205px 220px;animation:wave 3.8s ease-in-out infinite}.pip .eyes,.dot .eyes,.inky .eyes{animation:blink 5.4s infinite}.thinking .smile{animation:thinking 1.5s ease-in-out infinite}.celebrating{animation:celebrate .7s ease-in-out infinite alternate}
.metric{border-top:3px solid var(--ink);padding:.7rem .2rem}.metric-value{font-family:'DM Mono',monospace;font-size:2rem;font-weight:700}.metric-label{text-transform:uppercase;letter-spacing:.08em;font-size:.75rem}.meter{height:16px;background:var(--gray);border:2px solid var(--ink);border-radius:20px;overflow:hidden}.meter>div{height:100%;background:var(--red);animation:fill .9s ease-out both;transform-origin:left}.eyebrow{font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;color:var(--red);font-weight:700}.note{background:#f0ece1;border:2px dashed var(--ink);padding:1rem;border-radius:15px}.upload-wrap{border:3px dashed var(--ink);padding:1.5rem;border-radius:22px;background:rgba(255,254,248,.75)}.footer{font-family:'DM Mono',monospace;font-size:.72rem;text-align:center;margin-top:3rem;opacity:.7}
@keyframes breathe{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-6px) rotate(1deg)}}@keyframes wave{0%,65%,100%{transform:rotate(0)}72%{transform:rotate(-13deg)}79%{transform:rotate(8deg)}86%{transform:rotate(-8deg)}}@keyframes blink{0%,43%,47%,100%{transform:scaleY(1)}45%{transform:scaleY(.1)}}@keyframes twinkle{0%,100%{transform:scale(.8) rotate(0);opacity:.5}50%{transform:scale(1.25) rotate(15deg);opacity:1}}@keyframes wobble{0%,100%{transform:rotate(0)}25%{transform:rotate(-3deg) translateY(-3px)}75%{transform:rotate(3deg) translateY(-3px)}}@keyframes celebrate{from{transform:translateY(0) rotate(-2deg)}to{transform:translateY(-8px) rotate(2deg)}}@keyframes fill{from{transform:scaleX(0)}to{transform:scaleX(1)}}@keyframes thinking{0%,100%{opacity:.65}50%{opacity:1}}
@media(max-width:760px){.block-container{padding:1rem 1rem 3rem}.hero{padding:2rem 1.4rem;min-height:640px}.hero-copy{max-width:100%}.hero-art{width:75%;right:8%;bottom:-10px}.cameo{width:65px}.hero h1{font-size:3.5rem}.tagline{font-size:1.1rem}.stButton>button{width:100%}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}}
</style>'''
st.markdown(CSS, unsafe_allow_html=True)


def section_heading(eyebrow: str, title: str, copy: str = "") -> None:
    st.markdown(f'<div class="eyebrow">{eyebrow}</div><h2>{title}</h2>{f"<p>{copy}</p>" if copy else ""}', unsafe_allow_html=True)


def metric_card(label: str, value: str, accent: str = "") -> str:
    return f'<div class="metric"><div class="metric-value" style="color:{accent or "var(--ink)"}">{value}</div><div class="metric-label">{label}</div></div>'


# -----------------------------
# Session state and navigation
# -----------------------------
if "text_value" not in st.session_state:
    st.session_state.text_value = ""
if "pending_text" not in st.session_state:
    st.session_state.pending_text = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if st.session_state.pending_text is not None:
    st.session_state.text_value = st.session_state.pending_text
    st.session_state.pending_text = None

# Hero
st.markdown(f'''<section class="hero"><div class="hero-copy"><div class="kicker">✦ The friendly ink studio · issue no. 01</div><h1>OratorPulse</h1><p class="tagline">A cheerful little language workshop for finding the rhythm, personality, and patterns in your words.</p><div class="ink-line"></div></div><div class="hero-art">{pip_svg('happy')}</div><div class="cameo dot">{dot_svg('curious')}</div><div class="cameo inky">{inky_svg('happy')}</div><div class="star s1">✦</div><div class="star s2">✧</div><div class="star s3">✦</div></section>''', unsafe_allow_html=True)

st.write("")
hero_cols = st.columns([1, 1, 1, 1])
with hero_cols[0]:
    if st.button("Open the Text Lab", key="hero_lab"):
        st.session_state.pending_text = st.session_state.get("text_value", "")
        st.rerun()
with hero_cols[1]:
    st.markdown('<div class="note">Pip says: <b>Every sentence has a little wiggle.</b></div>', unsafe_allow_html=True)

st.markdown('<div class="ink-line"></div>', unsafe_allow_html=True)

# Cast
section_heading("Meet the studio crew", "Three original ink-side companions", "They are here to encourage curiosity—not to make definitive judgments about who wrote a text.")
cast = st.columns(3)
with cast[0]:
    st.markdown(f'<div class="panel cast-card pip-card">{pip_svg("happy")}<h3>Pip · the cheerful host</h3><p class="dialogue">“Let’s give those words a little spotlight!”</p><small>Welcoming, bouncy, and always ready with a magnifying grin.</small></div>', unsafe_allow_html=True)
with cast[1]:
    st.markdown(f'<div class="panel cast-card dot-card">{dot_svg("curious")}<h3>Dot · the curious detective</h3><p class="dialogue">“Hmm… a clue may be hiding in the rhythm.”</p><small>Thoughtful, observant, and fond of tidy little patterns.</small></div>', unsafe_allow_html=True)
with cast[2]:
    st.markdown(f'<div class="panel cast-card inky-card">{inky_svg("happy")}<h3>Inky · the playful scribble</h3><p class="dialogue">“Boing! Let’s make a friendly discovery.”</p><small>Silly, expressive, and never scary—just a happy blob of ink.</small></div>', unsafe_allow_html=True)

st.markdown('<div class="ink-line"></div>', unsafe_allow_html=True)

# Navigation
section_heading("Choose a desk", "The studio floor", "Each station keeps the practical tools close at hand, with a little characterful motion around the edges.")
tab_lab, tab_detective, tab_about = st.tabs(["✦ Text Lab", "⌕ Pattern Detective", "◎ How it works"])

with tab_lab:
    left, right = st.columns([1.55, .85], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">Desk 01 · write & listen</div><h3>Your story, center stage</h3><p>Paste a passage or write something new. The studio uses transparent, simple rules to surface patterns.</p>', unsafe_allow_html=True)
        st.text_area("Text for the studio", key="text_value", height=250, placeholder="Once upon a sentence…", label_visibility="collapsed")
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Analyze", key="analyze"):
                if st.session_state.text_value.strip():
                    st.session_state.analysis = analyze_text(st.session_state.text_value)
                    st.toast("Pip is listening! Your report is ready.")
                else:
                    st.session_state.analysis = None
                    st.warning("Pip is peeking into an empty notebook. Add a few words first!")
        with b2:
            if st.button("Example text", key="example"):
                st.session_state.pending_text = ("I believe a good story is a small door into another mind. "
                    "In my experience, the details matter, and a curious reader notices the rhythm. "
                    "At the end of the day, every voice deserves room to grow.")
                st.rerun()
        with b3:
            if st.button("Clear page", key="clear"):
                st.session_state.pending_text = ""
                st.session_state.analysis = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        mood = "thinking" if st.session_state.text_value.strip() and not st.session_state.analysis else "happy"
        st.markdown(f'<div class="panel" style="text-align:center"><div class="eyebrow">Pip’s desk-side note</div>{pip_svg(mood)}<h3>{"Pip is thinking…" if mood == "thinking" else "A blank page is a beginning"}</h3><p>{"The little wheels are turning. Results are clues, not a verdict." if mood == "thinking" else "Try the example button, or give the page a sentence of your own."}</p></div>', unsafe_allow_html=True)

    if st.session_state.analysis:
        r = st.session_state.analysis
        st.markdown('<div class="ink-line"></div>', unsafe_allow_html=True)
        section_heading("The report room", "A few friendly clues", "These indicators describe surface patterns in the text. They do not identify an author or prove how a passage was created.")
        m1, m2, m3, m4, m5 = st.columns(5)
        for col, html in zip([m1, m2, m3, m4, m5], [metric_card("words", str(r['word_count'])), metric_card("sentences", str(r['sentence_count'])), metric_card("avg. sentence", f"{r['avg_sentence']:.1f}"), metric_card("vocabulary variety", f"{r['vocabulary']:.0f}%", "var(--blue)"), metric_card("pattern score", f"{r['pattern_score']}", "var(--red)")]):
            with col: st.markdown(f'<div class="panel">{html}</div>', unsafe_allow_html=True)
        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            polished = ", ".join(r["polished"]) if r["polished"] else "No listed phrases spotted"
            st.markdown(f'<div class="panel"><div class="eyebrow">Phrase parade</div><h3>Polished-sounding phrases</h3><p>{escape(polished)}</p><div class="meter"><div style="width:{min(100, len(r["polished"])*18)}%"></div></div></div>', unsafe_allow_html=True)
        with c2:
            personal = ", ".join(r["personal"]) if r["personal"] else "No listed cues spotted"
            st.markdown(f'<div class="panel"><div class="eyebrow">Voice clues</div><h3>Personal-language cues</h3><p>{escape(personal)}</p><div class="meter"><div style="width:{min(100, len(r["personal"])*18)}%;background:var(--blue)"></div></div></div>', unsafe_allow_html=True)
        st.write("")
        repeated = ", ".join(f"{w} ({n})" for w, n in r["repeated"]) or "No notable repeats"
        st.markdown(f'<div class="panel"><div class="eyebrow">Dot’s notebook</div><h3>Repeated words</h3><p>{escape(repeated)}</p><small>Frequent words can be intentional emphasis, a topic signal, or simply part of natural writing.</small></div>', unsafe_allow_html=True)
        st.download_button("Download TXT report", report_text(st.session_state.text_value, r), file_name="oratorpulse-report.txt", mime="text/plain")

with tab_detective:
    dleft, dright = st.columns([1.2, .8], gap="large")
    with dleft:
        st.markdown('<div class="panel"><div class="eyebrow">Desk 02 · inspect a batch</div><h3>Dot’s pattern desk</h3><p>Upload a CSV or TXT file. For CSVs, choose the column containing the text you want to inspect.</p>', unsafe_allow_html=True)
        upload = st.file_uploader("Upload CSV or TXT", type=["csv", "txt"], label_visibility="visible")
        if upload is not None:
            try:
                if upload.name.lower().endswith(".csv"):
                    df = pd.read_csv(upload)
                    st.success(f"Dot found {len(df):,} rows in {upload.name}.")
                    text_col = st.selectbox("Text column", list(df.columns))
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
                    batch_text = "\n".join(df[text_col].dropna().astype(str).tolist())
                else:
                    batch_text = upload.getvalue().decode("utf-8", errors="replace")
                    st.success(f"Dot opened {upload.name}.")
                    st.text_area("Text preview", batch_text[:4000], height=180, disabled=True)
                if st.button("Inspect uploaded text", key="inspect_upload"):
                    st.session_state.analysis = analyze_text(batch_text)
                    st.session_state.pending_text = batch_text
                    st.rerun()
            except Exception as exc:
                st.error(f"Dot got a little tangled: {exc}")
        st.markdown('</div>', unsafe_allow_html=True)
    with dright:
        st.markdown(f'<div class="panel" style="text-align:center"><div class="eyebrow">Magnifying glass ready</div>{dot_svg("curious")}<h3>Clue, not conclusion</h3><p>Batch inspection is useful for exploring patterns across notes, drafts, or examples. It is not a scientific authorship test.</p></div>', unsafe_allow_html=True)

with tab_about:
    a, b = st.columns([1.2, .8], gap="large")
    with a:
        st.markdown('<div class="panel"><div class="eyebrow">The studio method</div><h3>How the little workshop works</h3><p><b>1 · Count.</b> Words and sentences are measured with lightweight punctuation and word rules.</p><p><b>2 · Notice.</b> A small, visible list of phrases and personal-language cues is checked.</p><p><b>3 · Compare.</b> Repeats and vocabulary variety add context to the sketch.</p><p><b>4 · Reflect.</b> The pattern score is an illustrative signal, never a certainty about a person or a text’s origin.</p><div class="note"><b>Limitations:</b> language is messy, creative, and culturally varied. Short passages can be especially noisy. Use these results as prompts for revision or discussion, not as evidence.</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="panel" style="text-align:center"><div class="eyebrow">A note from the cast</div>{inky_svg("happy")}<h3>Keep your own voice</h3><p>OratorPulse helps you notice what is on the page. You remain the best judge of what you meant.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="footer">ORATORPULSE · MADE IN THE FRIENDLY INK STUDIO · ALL CLUES ARE TRANSPARENT AND RULE-BASED</div>', unsafe_allow_html=True)
