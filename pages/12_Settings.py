import streamlit as st
from theme import apply_theme


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

# Apply currently saved theme
apply_theme()


# ============================================================
# TITLE
# ============================================================

st.title("⚙️ Settings")
st.caption("Customize your application")


# ============================================================
# DEFAULT SETTINGS
# ============================================================

if "saved_theme" not in st.session_state:
    st.session_state["saved_theme"] = "Light"

if "saved_notifications" not in st.session_state:
    st.session_state["saved_notifications"] = True


# ============================================================
# APPEARANCE
# ============================================================

st.divider()

st.subheader("🎨 Appearance")

theme = st.selectbox(
    "Theme",
    ["Light", "Dark"],
    index=(
        0
        if st.session_state["saved_theme"] == "Light"
        else 1
    ),
    key="theme_selection"
)


# ============================================================
# NOTIFICATIONS
# ============================================================

st.divider()

st.subheader("🔔 Notifications")

notifications = st.toggle(
    "Enable Notifications",
    value=st.session_state["saved_notifications"],
    key="notification_selection"
)


# ============================================================
# SAVE SETTINGS
# ============================================================

st.divider()

if st.button(
    "💾 Save Settings",
    type="primary",
    use_container_width=True
):

    # Save theme
    st.session_state["saved_theme"] = theme

    # Save notification setting
    st.session_state["saved_notifications"] = notifications

    st.success(
        "✅ Settings saved successfully!"
    )

    # Refresh the page so the new theme is applied
    st.rerun()