import streamlit as st
import pandas as pd

from theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Data Mining Analytics")
st.sidebar.markdown("---")

st.sidebar.success("🏠 Dashboard")

st.sidebar.markdown("### 🚀 Available Modules")

st.sidebar.write("📂 Dataset")
st.sidebar.write("🧹 Preprocessing")
st.sidebar.write("🌳 J48")
st.sidebar.write("🌲 ID3")
st.sidebar.write("📊 Naive Bayes")
st.sidebar.write("🎯 IBk (KNN)")
st.sidebar.write("🔵 Simple K-Means")
st.sidebar.write("🛒 Apriori")
st.sidebar.write("📈 Visualization")
st.sidebar.write("📄 Reports")


# ============================================================
# TITLE
# ============================================================

st.title("📊 Data Mining Analytics Platform")

st.caption(
    "A Professional Data Mining Application Inspired by WEKA"
)

st.markdown("---")


# ============================================================
# DATASET STATUS
# ============================================================

if "dataset" in st.session_state:

    df = st.session_state["dataset"]

    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isnull().sum().sum())
    duplicate = int(df.duplicated().sum())

    status = "Loaded ✅"

else:

    rows = 0
    cols = 0
    missing = 0
    duplicate = 0

    status = "Not Loaded ❌"


# ============================================================
# DASHBOARD CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Rows", rows)
c2.metric("Columns", cols)
c3.metric("Missing", missing)
c4.metric("Duplicates", duplicate)
c5.metric("Status", status)


st.markdown("---")


# ============================================================
# AVAILABLE ALGORITHMS
# ============================================================

st.subheader("🧠 Available Algorithms")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("🌳 J48 Decision Tree")
    st.success("🌲 ID3 Decision Tree")

with col2:

    st.success("📊 Naive Bayes")
    st.success("🎯 IBk (K-Nearest Neighbour)")

with col3:

    st.success("🔵 Simple K-Means")
    st.success("🛒 Apriori Association Rules")


st.markdown("---")


# ============================================================
# PROJECT WORKFLOW
# ============================================================

st.subheader("🚀 Project Workflow")

workflow = [
    "1️⃣ Upload Dataset",
    "2️⃣ Preprocess Dataset",
    "3️⃣ Select Algorithm",
    "4️⃣ Run Algorithm",
    "5️⃣ View Results",
    "6️⃣ Download Report"
]

with st.container(border=True):

    for step in workflow:

        st.write(step)


# ============================================================
# DATASET PREVIEW
# ============================================================

st.subheader("📄 Dataset Preview")

if "dataset" in st.session_state:

    st.dataframe(
        st.session_state["dataset"].head(10),
        use_container_width=True
    )

else:

    st.warning(
        "⚠️ No dataset uploaded."
    )


st.markdown("---")


# ============================================================
# ABOUT PROJECT
# ============================================================

st.subheader("ℹ️ About Project")

st.write(
    """
This application provides a professional interface
for performing Data Mining operations.

### Supported Algorithms

- 🌳 J48 Decision Tree
- 🌲 ID3 Decision Tree
- 📊 Naive Bayes
- 🎯 IBk (KNN)
- 🔵 Simple K-Means
- 🛒 Apriori

### Supported Dataset Formats

- CSV
- Excel (.xlsx)
- ARFF (WEKA)

### Features

- Dataset Upload
- Data Preprocessing
- Classification
- Clustering
- Association Rule Mining
- Visualization
- Reports
- Download Results
"""
)


st.markdown("---")


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Developed using Streamlit • Data Mining Analytics Platform"
)