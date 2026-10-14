from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OratorPulse — Cartoon Speech Studio", page_icon="🎙️", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Fredoka:wght@400;600;700&family=Patrick+Hand&display=swap');

html, body, [data-testid="stAppViewContainer"], button, input, textarea, label {
    font-family: 'Fredoka', 'Comic Sans MS', cursive !important;
}

.stApp {
    background: #fff8e8;
    color: #191919;
}

/* خلفية منقطة كارتونية */
[data-testid="stAppViewContainer"]:before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.22;
    background-image: radial-gradient(#f28c8c 2px, transparent 2px), radial-gradient(#8fd3ff 2px, transparent 2px);
    background-size: 40px 40px;
    background-position: 0 0, 20px 20px;
}

[data-testid="stSidebar"] {
    background: #ffe9c7;
    border-right: 3px solid #191919;
    box-shadow: 6px 0 0 #191919;
}

h1, h2, h3 {
    font-family: 'Bangers', cursive !important;
    letter-spacing: 0.03em;
    color: #191919;
}

.hero-card {
    border: 3px solid #191919;
    border-radius: 24px;
    background: #8fd3ff;
    padding: 2rem;
    box-shadow: 6px 7px 0 #191919;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-card h1 {
    font-size: 3rem;
    margin: 0 0 0.5rem 0;
    color: #191919;
}

.hero-card p {
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.25rem;
    color: #191919;
    margin: 0;
}

.fun-box {
    border: 3px solid #191919;
    border-radius: 20px;
    background: #ffffff;
    padding: 1.5rem;
    box-shadow: 5px 6px 0 #191919;
    margin-bottom: 1.5rem;
    transition: transform 0.2s ease;
}

.fun-box:hover {
    transform: translate(-3px, -3px);
    box-shadow: 8px 9px 0 #191919;
}

.badge-ideal {
    background: #bbf7d0;
    border: 2px solid #191919;
    padding: 0.3rem 0.8rem;
    border-radius: 12px;
    font-weight: 700;
    color: #166534;
    display: inline-block;
}

.badge-flawed {
    background: #fecaca;
    border: 2px solid #191919;
    padding: 0.3rem 0.8rem;
    border-radius: 12px;
    font-weight: 700;
    color: #991b1b;
    display: inline-block;
}

.stButton > button {
    border: 3px solid #191919;
    border-radius: 16px;
    background: #ffcf56;
    color: #191919;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 0.6rem 1.2rem;
    box-shadow: 4px 5px 0 #191919;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button:hover {
    background: #f28c8c;
    color: #191919;
    transform: translate(-2px, -2px);
    box-shadow: 6px 7px 0 #191919;
}

[data-testid="stMetric"] {
    border: 3px solid #191919;
    border-radius: 18px;
    background: #ffffff;
    padding: 1rem;
    box-shadow: 4px 5px 0 #191919;
}

[data-testid="stChatMessage"] {
    border: 3px solid #191919;
    border-radius: 18px;
    background: #fffef8;
    box-shadow: 4px 5px 0 #191919;
}
</style>
""",
    unsafe_allow_html=True,
)

# القائمة الجانبية الكارتونية
with st.sidebar:
    st.markdown("### 🎙️ OratorPulse Studio")
    st.caption("Track C · Contrastive Speech Magic")
    if st.button("✨ New Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("<b>🎨 Cartoon Themes</b>", unsafe_allow_html=True)
    theme_choice = st.radio("Choose Vibe:", ["Sunny Yellow", "Bubblegum Blue", "Minty Fresh"], label_visibility="collapsed")
    st.divider()
    st.file_uploader("📂 Drop Audio / Speech File", type=["wav", "mp3", "csv"])

# واجهة الهيرو الكارتونية المبهجة
st.markdown(
    """
<div class="hero-card">
    <h1>🎙️ ORATOR PULSE 🚀</h1>
    <p>Compare ideal vs. flawed speeches, smash temporal glitches, and score your voice with cartoon power!</p>
</div>
""",
    unsafe_allow_html=True,
)

# مؤشرات سريعة كارتونية
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏆 Rubric Score", "94 / 100", "🔥 Top Performance")
with col2:
    st.metric("⏱️ Temporal Grounding", "0.2s Gap", "⚡ Super Fast")
with col3:
    st.metric("🎯 Filler Words", "0 Detected", "✨ Clean Speech")

st.markdown("<br>", unsafe_allow_html=True)

# استبدال الجداول بكروت تفاعلية مبهجة (Cards Grid) بدون جداول نهائياً!
st.subheader("🌟 Speech Sample Cards (Contrastive Inspector)")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        """
    <div class="fun-box" style="background: #e0f2fe;">
        <span class="badge-ideal">IDEAL SAMPLE #1</span>
        <h3 style="margin: 0.5rem 0;">💡 Technical Pitch Master</h3>
        <p><b>Pace:</b> 145 WPM | <b>Jitter:</b> 1.25 | <b>Gap:</b> 0.2s</p>
        <p style="font-family: 'Patrick Hand', cursive; font-size: 1.1rem; color: #0369a1;">
        "Optimal pace and tone with zero filler words. Crystal clear delivery!"
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
    <div class="fun-box" style="background: #fdf4ff;">
        <span class="badge-ideal">IDEAL SAMPLE #2</span>
        <h3 style="margin: 0.5rem 0;">🚀 Product Launch</h3>
        <p><b>Pace:</b> 140 WPM | <b>Jitter:</b> 1.10 | <b>Gap:</b> 0.3s</p>
        <p style="font-family: 'Patrick Hand', cursive; font-size: 1.1rem; color: #86198f;">
        "Engaging rhythm, stable pitch, and high audience retention."
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
    <div class="fun-box" style="background: #fff1f2;">
        <span class="badge-flawed">FLAWED SAMPLE #1</span>
        <h3 style="margin: 0.5rem 0;">⚠️ Rushed Pitch</h3>
        <p><b>Pace:</b> 190 WPM | <b>Jitter:</b> 2.10 | <b>Gap:</b> 1.8s</p>
        <p style="font-family: 'Patrick Hand', cursive; font-size: 1.1rem; color: #9f1239;">
        "Excessive speed, frequent pauses, and stuttering on key terms."
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="fun-box" style="background: #fffbeb;">
        <span class="badge-flawed">FLAWED SAMPLE #2</span>
        <h3 style="margin: 0.5rem 0;">⚠️ Nervous Review</h3>
        <p><b>Pace:</b> 110 WPM | <b>Jitter:</b> 3.40 | <b>Gap:</b> 2.5s</p>
        <p style="font-family: 'Patrick Hand', cursive; font-size: 1.1rem; color: #92400e;">
        "Heavy hesitation, awkward silence spikes, and low confidence tone."
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.divider()

# قسم الشات التفاعلي الكارتوني
st.subheader("💬 AI Speech Coach Chat")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey there! 👋 I'm your cartoon speech coach. Ask me how to fix temporal gaps or boost your rubric score!"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_chat = st.chat_input("Ask about speech flaws, pacing, or rubric scores...")
if user_chat:
    st.session_state.messages.append({"role": "user", "content": user_chat})
    response = f"🎯 Great question! Regarding '{user_chat}', our contrastive model flags temporal gaps above 1.5s as primary flaws. Keep your pace around 140 WPM for maximum impact!"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

<ElicitationsGroup message="Explore more cartoon features:">
  <Elicitation label="Add interactive voice recording widget" query="How can I add an interactive live voice recording button in this cartoon style?"/>
  <Elicitation label="Create a cartoon score breakdown radar chart" query="How can I add a fun cartoon score breakdown chart to this app?"/>
</ElicitationsGroup>
