import streamlit as st
from theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Data Mining Analytics Platform",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# APPLY GLOBAL THEME
# ============================================================

apply_theme()


# ============================================================
# MAIN TITLE
# ============================================================

st.title("📊 Data Mining Analytics Platform")

st.caption(
    "A Professional Data Mining Application Inspired by WEKA"
)