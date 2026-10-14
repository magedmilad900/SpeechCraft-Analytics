
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Fredoka:wght@400;500;600;700&family=Patrick+Hand&display=swap');

:root {
    --ink: #171326;
    --purple: #9b5cff;
    --pink: #ff5ca8;
    --yellow: #fff05a;
    --cyan: #42f5ed;
    --lime: #b8ff5c;
    --paper: #fffdf5;
}

html, body, [data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] *,
[data-testid="stSidebar"] *,
button, input, textarea, label {
    font-family: 'Fredoka', 'Comic Sans MS', cursive !important;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 10%, #ff9ed0 0 2px, transparent 3px),
        radial-gradient(circle at 90% 30%, #70fff3 0 3px, transparent 4px),
        radial-gradient(circle at 30% 90%, #d6ff76 0 2px, transparent 3px),
        #eee5ff;
    background-size: 38px 38px, 51px 51px, 43px 43px, auto;
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1180px;
    padding: 2.2rem 2rem 4rem;
}

h1, h2, h3, h4,
[data-testid="stMetricValue"] {
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

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: var(--yellow);
    border-right: 4px solid var(--ink);
    box-shadow: 6px 0 0 var(--ink);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Bangers', cursive !important;
}

/* HERO */

.hero {
    position: relative;
    overflow: hidden;
    background: var(--purple);
    color: white;
    border: 4px solid var(--ink);
    border-radius: 30px;
    padding: 34px;
    box-shadow: 9px 9px 0 var(--ink);
    margin-bottom: 32px;
    transform: rotate(-0.4deg);
}

.hero::after {
    content: "★  ✦  ●";
    position: absolute;
    right: 22px;
    top: 16px;
    color: var(--yellow);
    font-family: 'Bangers', cursive;
    font-size: 2rem;
    transform: rotate(12deg);
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
    background: var(--yellow);
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

/* CARTOON CARDS */

.card {
    background: var(--paper);
    color: var(--ink);
    border: 3px solid var(--ink);
    border-radius: 24px;
    padding: 23px;
    box-shadow: 6px 6px 0 var(--ink);
    margin: 12px 0 22px;
    transition: transform .16s ease, box-shadow .16s ease;
}

.card:hover {
    transform: translate(-2px, -3px) rotate(-0.3deg);
    box-shadow: 9px 9px 0 var(--ink);
}

.card-yellow { background: var(--yellow); }
.card-pink { background: var(--pink); }
.card-blue { background: var(--cyan); }

.small-label {
    font-family: 'Bangers', cursive !important;
    font-size: 1.05rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.big-number {
    font-family: 'Bangers', cursive !important;
    font-size: 3rem;
    line-height: 1.2;
    text-shadow: 2px 2px 0 white;
}

/* BUTTONS */

.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: var(--yellow);
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
    transform: translate(-3px, -3px) rotate(-1deg);
    box-shadow: 8px 8px 0 var(--ink);
    border-color: var(--ink);
}

.stButton > button:active {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0 var(--ink);
}

/* INPUTS */

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

.stSelectbox > div > div,
[data-testid="stFileUploader"] section {
    border: 3px solid var(--ink);
    border-radius: 17px;
    background: white;
}

/* METRICS */

[data-testid="stMetric"] {
    background: var(--yellow);
    border: 3px solid var(--ink);
    border-radius: 19px;
    padding: 15px;
    box-shadow: 5px 5px 0 var(--ink);
}

[data-testid="stMetricLabel"] {
    font-family: 'Bangers', cursive !important;
    font-size: 1.05rem !important;
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
}

/* CHAT BUBBLES */

[data-testid="stChatMessage"] {
    background: white;
    border: 3px solid var(--ink);
    border-radius: 20px;
    box-shadow: 4px 4px 0 var(--ink);
    padding: 12px;
    margin-bottom: 16px;
}

[data-testid="stChatMessage"]:nth-of-type(even) {
    background: #e1fffb;
}

/* TABS */

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
    background: var(--yellow) !important;
    color: var(--ink) !important;
}

/* EXPANDERS AND ALERTS */

[data-testid="stExpander"] {
    background: white;
    border: 3px solid var(--ink);
    border-radius: 18px;
    box-shadow: 4px 4px 0 var(--ink);
}

[data-testid="stAlert"] {
    border: 3px solid var(--ink);
    border-radius: 17px;
    box-shadow: 4px 4px 0 var(--ink);
}

/* PROGRESS BAR */

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

/* PILLS AND FINDINGS */

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

.finding {
    background: #fff2a8;
    border: 3px solid var(--ink);
    border-radius: 14px;
    padding: 14px;
    box-shadow: 4px 4px 0 var(--ink);
    margin: 12px 0;
}

hr {
    border: none;
    border-top: 3px dashed #9b82d6;
    margin: 26px 0;
}

footer {
    visibility: hidden;
}

@media (max-width: 700px) {
    .block-container { padding: 1rem; }
    .hero { padding: 24px; }
    .hero h1 { font-size: 2.7rem !important; }
    .card { padding: 17px; }
}
