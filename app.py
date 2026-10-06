import streamlit as st
from theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="CardioRisk Analytics Platform",
    page_icon="❤️",
    layout="wide"
)

# ============================================================
# APPLY GLOBAL THEME
# ============================================================

apply_theme()


# ============================================================
# MAIN TITLE
# ============================================================

st.title("❤️ CardioRisk Analytics Platform")

st.caption(
    "An Integrated Data Warehousing and Machine Learning Framework "
    "for Early Cardiovascular Disease Risk Prediction"
)