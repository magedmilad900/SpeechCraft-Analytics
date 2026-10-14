
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Fredoka:wght@400;500;600;700&family=Patrick+Hand&display=swap');

.stApp,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 10%, #ff9ed0 0 2px, transparent 3px),
        radial-gradient(circle at 90% 30%, #70fff3 0 3px, transparent 4px),
        #eee5ff;
    background-size: 38px 38px, 51px 51px, auto;
    color: #171326;
}

h1, h2, h3, p, button, input, textarea, label {
    font-family: 'Fredoka', cursive !important;
}

h1, h2, h3 {
    font-family: 'Bangers', cursive !important;
}

.stButton > button {
    background: #fff05a;
    color: #171326;
    border: 3px solid #171326;
    border-radius: 15px;
    box-shadow: 5px 5px 0 #171326;
    font-weight: 800;
}

[data-testid="stSidebar"] {
    background: #fff05a;
    border-right: 4px solid #171326;
}
</style>
""", unsafe_allow_html=True)
