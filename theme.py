import streamlit as st
import base64
from pathlib import Path


def apply_theme():

    # ============================================================
    # CRICKET BACKGROUND IMAGE
    # ============================================================

    image_path = (
        Path(__file__).parent
        / "assets"
        / "cricket_background.png"
    )

    if image_path.exists():

        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(
                image_file.read()
            ).decode()

        background_css = f"""
        background-image:
            linear-gradient(
                rgba(0, 0, 0, 0.42),
                rgba(0, 0, 0, 0.42)
            ),
            url("data:image/png;base64,{encoded_image}");

        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        """

    else:

        background_css = """
        background-color: #0E1117;
        """

    # ============================================================
    # APPLY GLOBAL THEME
    # ============================================================

    st.markdown(
        f"""
        <style>

        /* ========================================================
           REMOVE STREAMLIT WHITE BACKGROUND
        ======================================================== */

        html,
        body {{
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;
        }}

        /* ========================================================
           MAIN APPLICATION BACKGROUND
        ======================================================== */

        .stApp {{
            {background_css}
            color: #FFFFFF !important;
        }}

        .main {{
            background: transparent !important;
        }}

        .main .block-container {{
            background: transparent !important;
            padding-top: 2rem;
        }}

        /* ========================================================
           STREAMLIT TOP HEADER
        ======================================================== */

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stToolbar"] {{
            background: transparent !important;
        }}

        /* ========================================================
           TOP DECORATION
        ======================================================== */

        [data-testid="stDecoration"] {{
            background: transparent !important;
        }}

        /* ========================================================
           ALL HEADINGS
        ======================================================== */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            color: #FFFFFF !important;

            text-shadow:
                2px 2px 5px rgba(0, 0, 0, 0.90) !important;
        }}

        /* ========================================================
           NORMAL TEXT
        ======================================================== */

        p,
        label,
        span,
        small,
        li {{
            color: #FFFFFF !important;
        }}

        .stMarkdown {{
            color: #FFFFFF !important;
        }}

        .stCaption {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           SIDEBAR
        ======================================================== */

        section[data-testid="stSidebar"] {{
            background:
                rgba(5, 15, 30, 0.94) !important;

            backdrop-filter: blur(12px);
        }}

        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           SIDEBAR HEADINGS
        ======================================================== */

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6 {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           NORMAL BUTTONS
        ======================================================== */

        .stButton > button {{
            background:
                linear-gradient(
                    135deg,
                    #1976D2,
                    #0D47A1
                ) !important;

            color: #FFFFFF !important;

            border:
                1px solid
                rgba(255,255,255,0.45) !important;

            border-radius: 10px !important;

            padding:
                0.55rem 1.2rem !important;

            font-weight: 600 !important;

            box-shadow:
                0 4px 10px
                rgba(0,0,0,0.30) !important;

            transition:
                all 0.2s ease !important;
        }}

        .stButton > button:hover {{
            background:
                linear-gradient(
                    135deg,
                    #2196F3,
                    #1565C0
                ) !important;

            border-color: #FFFFFF !important;

            transform: translateY(-1px);
        }}

        .stButton > button p {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           DOWNLOAD BUTTONS
        ======================================================== */

        .stDownloadButton > button {{
            background:
                linear-gradient(
                    135deg,
                    #1976D2,
                    #0D47A1
                ) !important;

            color: #FFFFFF !important;

            border:
                1px solid
                rgba(255,255,255,0.45) !important;

            border-radius: 10px !important;

            padding:
                0.55rem 1.2rem !important;

            font-weight: 600 !important;

            box-shadow:
                0 4px 10px
                rgba(0,0,0,0.30) !important;
        }}

        .stDownloadButton > button:hover {{
            background:
                linear-gradient(
                    135deg,
                    #2196F3,
                    #1565C0
                ) !important;

            border-color: #FFFFFF !important;

            transform: translateY(-1px);
        }}

        .stDownloadButton > button p {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           FILE UPLOADER
        ======================================================== */

        [data-testid="stFileUploader"] {{
            background:
                rgba(10, 20, 35, 0.92) !important;

            border-radius: 12px;
            padding: 12px;
        }}

        [data-testid="stFileUploader"] button {{
            background: #1976D2 !important;
            color: #FFFFFF !important;

            border:
                1px solid
                rgba(255,255,255,0.45) !important;
        }}

        [data-testid="stFileUploader"] button span {{
            color: #FFFFFF !important;
        }}

        [data-testid="stFileUploader"] small {{
            color: #FFFFFF !important;
            opacity: 1 !important;
        }}

        [data-testid="stFileUploader"] p {{
            color: #FFFFFF !important;
        }}

        [data-testid="stFileUploader"] span {{
            color: #FFFFFF !important;
        }}

        [data-testid="stFileUploader"] label {{
            color: #FFFFFF !important;
        }}

        [data-testid="stFileUploaderDropzone"] {{
            background:
                rgba(10, 20, 35, 0.92) !important;

            border:
                1px solid
                rgba(255,255,255,0.40) !important;
        }}

        /* ========================================================
           SELECT BOX
        ======================================================== */

        div[data-baseweb="select"] {{
            background:
                rgba(10, 20, 35, 0.90) !important;
        }}

        div[data-baseweb="select"] * {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           TEXT INPUT
        ======================================================== */

        input,
        textarea {{
            color: #FFFFFF !important;

            background:
                rgba(10, 20, 35, 0.90) !important;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: #DDDDDD !important;
            opacity: 1 !important;
        }}

        /* ========================================================
           NUMBER INPUT
        ======================================================== */

        div[data-testid="stNumberInput"] input {{
            color: #FFFFFF !important;

            background:
                rgba(10, 20, 35, 0.90) !important;
        }}

        /* ========================================================
           MULTISELECT
        ======================================================== */

        div[data-testid="stMultiSelect"] {{
            background:
                rgba(10, 20, 35, 0.90) !important;
        }}

        div[data-testid="stMultiSelect"] * {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           RADIO BUTTONS
        ======================================================== */

        div[data-testid="stRadio"] label {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           CHECKBOX
        ======================================================== */

        div[data-testid="stCheckbox"] label {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           TOGGLE
        ======================================================== */

        div[data-testid="stToggle"] label {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           METRIC CARDS
        ======================================================== */

        div[data-testid="stMetric"] {{
            background:
                rgba(10, 20, 35, 0.90) !important;

            border-radius: 14px;

            padding: 15px;

            border:
                1px solid
                rgba(255,255,255,0.20);

            box-shadow:
                0 4px 15px
                rgba(0,0,0,0.35);
        }}

        div[data-testid="stMetric"] * {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           DATAFRAME
        ======================================================== */

        [data-testid="stDataFrame"] {{
            background:
                rgba(10, 20, 35, 0.92) !important;

            border-radius: 10px;
        }}

        /* ========================================================
           ALERTS
        ======================================================== */

        [data-testid="stAlert"] {{
            border-radius: 10px;
        }}

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           EXPANDERS
        ======================================================== */

        [data-testid="stExpander"] {{
            background:
                rgba(10, 20, 35, 0.88) !important;

            border-radius: 10px;
        }}

        [data-testid="stExpander"] * {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           TABS
        ======================================================== */

        button[data-baseweb="tab"] {{
            color: #FFFFFF !important;
        }}

        button[data-baseweb="tab"] p {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           DIVIDERS
        ======================================================== */

        hr {{
            border-color:
                rgba(255,255,255,0.35) !important;
        }}

        /* ========================================================
           LINKS
        ======================================================== */

        a {{
            color: #FFFFFF !important;
        }}

        /* ========================================================
           NOTIFICATIONS
        ======================================================== */

        [data-testid="stNotification"] * {{
            color: #FFFFFF !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )