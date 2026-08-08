import streamlit as st
import pandas as pd
import io
from theme import apply_theme
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Reports",
    page_icon="📑",
    layout="wide"
)
apply_theme()


# ============================================================
# TITLE
# ============================================================

st.title("📑 Data Mining Reports")
st.caption(
    "Generate and download a professional report from the dataset"
)


# ============================================================
# CHECK DATASET
# ============================================================

if "dataset" not in st.session_state:

    st.warning(
        "⚠️ Please upload a dataset first."
    )

    st.stop()


df = st.session_state["dataset"].copy()


# ============================================================
# DATASET SUMMARY
# ============================================================

st.subheader("📊 Dataset Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Rows",
    df.shape[0]
)

c2.metric(
    "Columns",
    df.shape[1]
)

c3.metric(
    "Missing Values",
    int(df.isnull().sum().sum())
)

c4.metric(
    "Duplicate Rows",
    int(df.duplicated().sum())
)


# ============================================================
# DATASET PREVIEW
# ============================================================

st.divider()

st.subheader("📄 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True,
    height=350
)


# ============================================================
# COLUMN INFORMATION
# ============================================================

st.divider()

st.subheader("📋 Column Information")

column_info = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": [
        str(df[column].dtype)
        for column in df.columns
    ],
    "Missing Values": [
        int(df[column].isnull().sum())
        for column in df.columns
    ],
    "Unique Values": [
        int(df[column].nunique())
        for column in df.columns
    ]
})

st.dataframe(
    column_info,
    use_container_width=True
)


# ============================================================
# REPORT OPTIONS
# ============================================================

st.divider()

st.subheader("⚙️ Report Options")

include_preview = st.checkbox(
    "Include Dataset Preview",
    value=True,
    key="report_preview"
)

include_columns = st.checkbox(
    "Include Column Information",
    value=True,
    key="report_columns"
)

include_statistics = st.checkbox(
    "Include Dataset Statistics",
    value=True,
    key="report_statistics"
)


# ============================================================
# GENERATE REPORT
# ============================================================

if st.button(
    "📄 Generate Report",
    type="primary",
    key="generate_report"
):

    # ========================================================
    # CREATE MEMORY BUFFER
    # ========================================================

    report = io.BytesIO()


    # ========================================================
    # PDF DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(
        report,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=15
    )


    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=12,
        spaceAfter=8
    )


    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14
    )


    # ========================================================
    # STORY
    # ========================================================

    story = []


    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "Data Mining Analytics Report",
            title_style
        )
    )


    story.append(
        Paragraph(
            f"Generated on: "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            normal_style
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    story.append(
        Paragraph(
            "1. Dataset Overview",
            heading_style
        )
    )


    overview_data = [
        ["Property", "Value"],
        ["Rows", str(df.shape[0])],
        ["Columns", str(df.shape[1])],
        [
            "Missing Values",
            str(int(df.isnull().sum().sum()))
        ],
        [
            "Duplicate Rows",
            str(int(df.duplicated().sum()))
        ]
    ]


    overview_table = Table(
        overview_data,
        colWidths=[220, 220]
    )


    overview_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#2563EB")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )


    story.append(
        overview_table
    )


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    if include_columns:

        story.append(
            Paragraph(
                "2. Column Information",
                heading_style
            )
        )


        column_table_data = [
            [
                "Column",
                "Data Type",
                "Missing",
                "Unique"
            ]
        ]


        for column in df.columns:

            column_table_data.append([
                str(column),
                str(df[column].dtype),
                str(
                    int(
                        df[column]
                        .isnull()
                        .sum()
                    )
                ),
                str(
                    int(
                        df[column]
                        .nunique()
                    )
                )
            ])


        column_table = Table(
            column_table_data,
            repeatRows=1,
            colWidths=[
                150,
                100,
                80,
                80
            ]
        )


        column_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563EB")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )


        story.append(
            column_table
        )


    # ========================================================
    # DATASET STATISTICS
    # ========================================================

    if include_statistics:

        story.append(
            Paragraph(
                "3. Dataset Statistics",
                heading_style
            )
        )


        numeric_df = df.select_dtypes(
            include="number"
        )


        if not numeric_df.empty:

            statistics = (
                numeric_df
                .describe()
                .round(3)
                .reset_index()
            )


            statistics_data = [
                [
                    str(column)
                    for column
                    in statistics.columns
                ]
            ]


            for _, row in statistics.iterrows():

                statistics_data.append([
                    str(value)
                    for value in row
                ])


            statistics_table = Table(
                statistics_data,
                repeatRows=1
            )


            statistics_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#2563EB")
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    )
                ])
            )


            story.append(
                statistics_table
            )


        else:

            story.append(
                Paragraph(
                    "No numeric columns are available "
                    "for statistical analysis.",
                    normal_style
                )
            )


    # ========================================================
    # DATASET PREVIEW
    # ========================================================

    if include_preview:

        story.append(
            PageBreak()
        )


        story.append(
            Paragraph(
                "4. Dataset Preview",
                heading_style
            )
        )


        preview = df.head(10).copy()


        preview_data = [
            [
                str(column)
                for column in preview.columns
            ]
        ]


        for _, row in preview.iterrows():

            preview_data.append([
                str(value)
                for value in row
            ])


        # Limit columns for PDF readability
        if len(preview.columns) > 8:

            preview = preview.iloc[:, :8]

            preview_data = [
                [
                    str(column)
                    for column
                    in preview.columns
                ]
            ]


            for _, row in preview.iterrows():

                preview_data.append([
                    str(value)
                    for value in row
                ])


        preview_table = Table(
            preview_data,
            repeatRows=1
        )


        preview_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563EB")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    4
                )
            ])
        )


        story.append(
            preview_table
        )


    # ========================================================
    # CONCLUSION
    # ========================================================

    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "5. Conclusion",
            heading_style
        )
    )


    conclusion = (
        "The dataset was successfully analyzed using the "
        "Data Mining Analytics Platform. The report provides "
        "an overview of the dataset, column information, "
        "statistical information and a sample of the "
        "available records."
    )


    story.append(
        Paragraph(
            conclusion,
            normal_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )


    # ========================================================
    # IMPORTANT:
    # GET BYTES BEFORE ANY CLOSE OPERATION
    # ========================================================

    report_data = report.getvalue()


    # ========================================================
    # SAVE IN SESSION STATE
    # ========================================================

    st.session_state[
        "generated_report"
    ] = report_data


    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        "✅ Report generated successfully!"
    )


# ============================================================
# DOWNLOAD REPORT
# ============================================================

if "generated_report" in st.session_state:

    st.divider()

    st.subheader(
        "⬇️ Download Report"
    )


    st.download_button(
        label="⬇️ Download PDF Report",
        data=st.session_state[
            "generated_report"
        ],
        file_name="Data_Mining_Analytics_Report.pdf",
        mime="application/pdf",
        key="download_pdf_report"
    )