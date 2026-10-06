import streamlit as st
import base64
from pathlib import Path


def apply_theme():

    # ============================================================
    # CARDIOVASCULAR HEALTHCARE BACKGROUND IMAGE
    # ============================================================

    image_path = (
        Path(__file__).parent
        / "assets"
        / "image.jpg"
    )

    if image_path.exists():

        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(
                image_file.read()
            ).decode()

        background_css = f"""
        background-image:
            linear-gradient(
                rgba(0, 20, 40, 0.48),
                rgba(0, 15, 35, 0.48)
            ),
            url("data:image/png;base64,{encoded_image}");

        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        """

    else:

        background_css = """
        background-color: #071A2B;
        """

    # ============================================================
    # GLOBAL STREAMLIT THEME
    # ============================================================

    st.markdown(
        f"""
        <style>

        /* ========================================================
           REMOVE DEFAULT STREAMLIT BACKGROUND
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

        .stApp {{
            {background_css}
            color: #FFFFFF !important;
            min-height: 100vh;
        }}

        .main {{
            background: transparent !important;
        }}

        .main .block-container {{
            background: transparent !important;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}


        /* ========================================================
           STREAMLIT HEADER
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

        [data-testid="stDecoration"] {{
            background: transparent !important;
        }}


        /* ========================================================
           HEADINGS
        ======================================================== */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            text-shadow:
                2px 2px 5px rgba(0, 0, 0, 0.90) !important;
        }}

        h1 {{
            font-size: 2.4rem !important;
        }}

        h2 {{
            font-size: 1.8rem !important;
        }}

        h3 {{
            font-size: 1.4rem !important;
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
            color: #E0E0E0 !important;
        }}


        /* ========================================================
           SIDEBAR
        ======================================================== */

        section[data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    rgba(3, 20, 35, 0.97),
                    rgba(4, 25, 45, 0.97)
                ) !important;

            backdrop-filter: blur(15px);
            border-right:
                1px solid rgba(255, 255, 255, 0.12);
        }}

        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6 {{
            color: #FFFFFF !important;
        }}


        /* ========================================================
           BUTTONS
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
                rgba(255, 255, 255, 0.40) !important;

            border-radius: 10px !important;

            padding:
                0.55rem 1.2rem !important;

            font-weight: 600 !important;

            box-shadow:
                0 4px 12px
                rgba(0, 0, 0, 0.35) !important;

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

            transform: translateY(-2px);

            box-shadow:
                0 6px 16px
                rgba(0, 0, 0, 0.45) !important;
        }}

        .stButton > button p {{
            color: #FFFFFF !important;
        }}


        /* ========================================================
           DOWNLOAD BUTTON
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
                rgba(255, 255, 255, 0.40) !important;

            border-radius: 10px !important;

            padding:
                0.55rem 1.2rem !important;

            font-weight: 600 !important;

            box-shadow:
                0 4px 12px
                rgba(0, 0, 0, 0.35) !important;
        }}

        .stDownloadButton > button:hover {{
            background:
                linear-gradient(
                    135deg,
                    #2196F3,
                    #1565C0
                ) !important;

            border-color: #FFFFFF !important;

            transform: translateY(-2px);
        }}

        .stDownloadButton > button p {{
            color: #FFFFFF !important;
        }}


        /* ========================================================
           METRIC CARDS
        ======================================================== */

        div[data-testid="stMetric"] {{
            background:
                linear-gradient(
                    135deg,
                    rgba(5, 30, 55, 0.94),
                    rgba(10, 45, 75, 0.90)
                ) !important;

            border-radius: 14px !important;

            padding: 18px !important;

            border:
                1px solid
                rgba(100, 200, 255, 0.25) !important;

            box-shadow:
                0 5px 18px
                rgba(0, 0, 0, 0.40) !important;

            backdrop-filter: blur(8px);
        }}

        div[data-testid="stMetric"] * {{
            color: #FFFFFF !important;
        }}

        div[data-testid="stMetricLabel"] {{
            color: #B9E7FF !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}


        /* ========================================================
           FILE UPLOADER
        ======================================================== */

        [data-testid="stFileUploader"] {{
            background:
                rgba(5, 25, 45, 0.94) !important;

            border-radius: 12px !important;

            padding: 12px !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.20) !important;
        }}

        [data-testid="stFileUploader"] button {{
            background: #1976D2 !important;

            color: #FFFFFF !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.40) !important;
        }}

        [data-testid="stFileUploader"] button span {{
            color: #FFFFFF !important;
        }}

        [data-testid="stFileUploader"] small {{
            color: #FFFFFF !important;
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
                rgba(5, 25, 45, 0.92) !important;

            border:
                1px solid
                rgba(100, 200, 255, 0.30) !important;
        }}


        /* ========================================================
           SELECT BOX
        ======================================================== */

        div[data-baseweb="select"] {{
            background:
                rgba(5, 25, 45, 0.95) !important;

            border-radius: 8px !important;
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
                rgba(5, 25, 45, 0.95) !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.20) !important;

            border-radius: 8px !important;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: #D0D0D0 !important;
            opacity: 1 !important;
        }}


        /* ========================================================
           NUMBER INPUT
        ======================================================== */

        div[data-testid="stNumberInput"] input {{
            color: #FFFFFF !important;

            background:
                rgba(5, 25, 45, 0.95) !important;
        }}


        /* ========================================================
           MULTISELECT
        ======================================================== */

        div[data-testid="stMultiSelect"] {{
            background:
                rgba(5, 25, 45, 0.95) !important;
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
           DATAFRAME
        ======================================================== */

        [data-testid="stDataFrame"] {{
            background:
                rgba(5, 25, 45, 0.94) !important;

            border-radius: 10px !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.18) !important;
        }}


        /* ========================================================
           ALERTS
        ======================================================== */

        [data-testid="stAlert"] {{
            border-radius: 10px !important;
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
                rgba(5, 25, 45, 0.90) !important;

            border-radius: 10px !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.15) !important;

            backdrop-filter: blur(8px);
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
           LINKS
        ======================================================== */

        a {{
            color: #8ED8FF !important;
            font-weight: 500;
        }}

        a:hover {{
            color: #FFFFFF !important;
        }}


        /* ========================================================
           DIVIDERS
        ======================================================== */

        hr {{
            border-color:
                rgba(255, 255, 255, 0.25) !important;
        }}


        /* ========================================================
           COLUMNS / CARDS
        ======================================================== */

        div[data-testid="column"] {{
            color: #FFFFFF !important;
        }}


        /* ========================================================
           SCROLLBAR
        ======================================================== */

        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: #061522;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #1976D2;
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #2196F3;
        }}


        /* ========================================================
           CARD STYLE FOR CUSTOM HTML
        ======================================================== */

        .health-card {{
            background:
                linear-gradient(
                    135deg,
                    rgba(5, 30, 55, 0.94),
                    rgba(10, 45, 75, 0.88)
                );

            border:
                1px solid
                rgba(100, 200, 255, 0.25);

            border-radius: 16px;

            padding: 20px;

            margin-bottom: 18px;

            box-shadow:
                0 6px 20px
                rgba(0, 0, 0, 0.35);

            backdrop-filter: blur(10px);
        }}

        .health-card h3 {{
            color: #FFFFFF !important;
            margin-bottom: 8px;
        }}

        .health-card p {{
            color: #DDEEFF !important;
        }}


        /* ========================================================
           CVD TITLE
        ======================================================== */

        .cvd-title {{
            text-align: center;

            font-size: 2.4rem;

            font-weight: 800;

            color: #FFFFFF;

            text-shadow:
                2px 2px 8px rgba(0, 0, 0, 0.90);

            margin-bottom: 5px;
        }}

        .cvd-subtitle {{
            text-align: center;

            font-size: 1.05rem;

            color: #D7F3FF !important;

            text-shadow:
                1px 1px 4px rgba(0, 0, 0, 0.80);

            margin-bottom: 25px;
        }}


        /* ========================================================
           FOOTER
        ======================================================== */

        footer {{
            visibility: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )