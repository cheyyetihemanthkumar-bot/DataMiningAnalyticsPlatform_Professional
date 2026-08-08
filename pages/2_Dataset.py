import streamlit as st
import pandas as pd
import arff
import os
import io

from theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dataset",
    page_icon="📂",
    layout="wide"
)

apply_theme()


# ============================================================
# TITLE
# ============================================================

st.title("📂 Dataset Management")
st.caption("Upload, Preview and Manage Datasets")

st.divider()


# ============================================================
# UPLOAD DATASET
# ============================================================

st.subheader("📤 Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose Dataset",
    type=["csv", "xlsx", "arff"],
    key="dataset_uploader"
)


# ============================================================
# PROCESS UPLOADED DATASET
# ============================================================

if uploaded_file is not None:

    extension = os.path.splitext(
        uploaded_file.name
    )[1].lower()

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    if extension == ".csv":

        try:

            df = pd.read_csv(
                uploaded_file
            )

        except Exception as e:

            st.error(
                f"❌ Error reading CSV file: {e}"
            )

            st.stop()


    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    elif extension == ".xlsx":

        try:

            df = pd.read_excel(
                uploaded_file
            )

        except Exception as e:

            st.error(
                f"❌ Error reading Excel file: {e}"
            )

            st.stop()


    # --------------------------------------------------------
    # ARFF
    # --------------------------------------------------------

    elif extension == ".arff":

        try:

            text_data = io.StringIO(
                uploaded_file
                .getvalue()
                .decode("utf-8")
            )

            dataset = arff.load(
                text_data
            )

            df = pd.DataFrame(
                dataset["data"]
            )

            df.columns = [
                attr[0]
                for attr in dataset["attributes"]
            ]

        except Exception as e:

            st.error(
                f"❌ Error reading ARFF file: {e}"
            )

            st.stop()


    # --------------------------------------------------------
    # INVALID FORMAT
    # --------------------------------------------------------

    else:

        st.error(
            "❌ Unsupported file format."
        )

        st.stop()


    # ========================================================
    # CLEAN COLUMN NAMES
    # ========================================================

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]


    # ========================================================
    # SAVE DATASET
    # ========================================================

    st.session_state["dataset"] = df.copy()

    st.session_state[
        "dataset_filename"
    ] = uploaded_file.name


    st.success(
        "✅ Dataset Uploaded Successfully!"
    )


# ============================================================
# GET SAVED DATASET
# ============================================================

if "dataset" in st.session_state:

    df = st.session_state[
        "dataset"
    ].copy()


    # ========================================================
    # DATASET SUMMARY
    # ========================================================

    st.divider()

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
        int(
            df.isnull()
            .sum()
            .sum()
        )
    )

    c4.metric(
        "Duplicate Rows",
        int(
            df.duplicated()
            .sum()
        )
    )


    # ========================================================
    # DATASET PREVIEW
    # ========================================================

    st.divider()

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    st.divider()

    st.subheader("📋 Column Information")

    column_info = pd.DataFrame({

        "Column Name":
            df.columns.tolist(),

        "Data Type":
            df.dtypes.astype(
                str
            ).tolist(),

        "Missing Values":
            df.isnull()
            .sum()
            .tolist(),

        "Unique Values":
            df.nunique()
            .tolist()

    })

    st.dataframe(
        column_info,
        use_container_width=True
    )


    # ========================================================
    # DATASET STATISTICS
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Dataset Statistics"
    )

    try:

        statistics = df.describe(
            include="all"
        ).transpose()

        st.dataframe(
            statistics,
            use_container_width=True
        )

    except Exception:

        st.warning(
            "⚠️ Statistics cannot be generated "
            "for this dataset."
        )


    # ========================================================
    # SEARCH RECORDS
    # ========================================================

    st.divider()

    st.subheader(
        "🔍 Search Records"
    )

    search = st.text_input(
        "Enter keyword",
        key="dataset_search"
    )

    if search:

        filtered = df[
            df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

        st.write(
            f"🔎 Found {len(filtered)} matching records."
        )

        st.dataframe(
            filtered,
            use_container_width=True
        )


    # ========================================================
    # DOWNLOAD DATASET
    # ========================================================

    st.divider()

    st.subheader(
        "⬇️ Download Dataset"
    )

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Dataset",
        data=csv_data,
        file_name="dataset.csv",
        mime="text/csv",
        key="download_dataset"
    )


# ============================================================
# NO DATASET
# ============================================================

else:

    st.info(
        "📂 Please upload a CSV, Excel or ARFF dataset."
    )