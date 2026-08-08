import streamlit as st
import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    MinMaxScaler,
    StandardScaler
)


from theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Preprocessing",
    page_icon="🧹",
    layout="wide"
)

apply_theme()


# ============================================================
# TITLE
# ============================================================

st.title("🧹 Data Preprocessing")

st.caption(
    "Clean and transform your dataset before running algorithms"
)

st.divider()


# ============================================================
# CHECK DATASET
# ============================================================

if "dataset" not in st.session_state:

    st.warning(
        "⚠️ Please upload a dataset first."
    )

    st.stop()


# Always start from the uploaded dataset
df = st.session_state["dataset"].copy()


# ============================================================
# DATASET SUMMARY
# ============================================================

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
    "Missing",
    int(
        df.isnull()
        .sum()
        .sum()
    )
)

c4.metric(
    "Duplicates",
    int(
        df.duplicated()
        .sum()
    )
)


st.divider()


# ============================================================
# DATASET PREVIEW
# ============================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)


st.divider()


# ============================================================
# REMOVE COLUMNS
# ============================================================

st.subheader("🗑 Remove Columns")

remove_cols = st.multiselect(
    "Select Columns to Remove",
    options=list(df.columns),
    key="preprocessing_remove_columns"
)


st.divider()


# ============================================================
# RENAME COLUMN
# ============================================================

st.subheader("✏️ Rename Column")

rename_col = st.selectbox(
    "Choose Column",
    ["None"] + list(df.columns),
    key="preprocessing_rename_column"
)


new_name = ""

if rename_col != "None":

    new_name = st.text_input(
        "New Column Name",
        key="preprocessing_new_column_name"
    )


st.divider()


# ============================================================
# MISSING VALUES
# ============================================================

st.subheader("❓ Handle Missing Values")

missing_option = st.selectbox(
    "Choose Method",
    [
        "Do Nothing",
        "Drop Missing Rows",
        "Fill Numeric Mean",
        "Fill Numeric Median",
        "Fill Categorical Mode"
    ],
    key="preprocessing_missing_method"
)


st.divider()


# ============================================================
# REMOVE DUPLICATES
# ============================================================

st.subheader("🔁 Duplicate Rows")

remove_duplicate = st.checkbox(
    "Remove Duplicate Rows",
    key="preprocessing_remove_duplicates"
)


st.divider()


# ============================================================
# LABEL ENCODING
# ============================================================

st.subheader("🏷️ Label Encoding")

categorical = list(
    df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns
)


encode_columns = st.multiselect(
    "Select Columns for Label Encoding",
    options=categorical,
    key="preprocessing_encode_columns"
)


if categorical:

    st.caption(
        "Categorical columns available for encoding: "
        + ", ".join(categorical)
    )

else:

    st.info(
        "ℹ️ No categorical columns available for encoding."
    )


st.divider()


# ============================================================
# SCALING
# ============================================================

st.subheader(
    "📈 Normalization / Standardization"
)


numeric_columns = list(
    df.select_dtypes(
        include="number"
    ).columns
)


scale_columns = st.multiselect(
    "Select Numeric Columns",
    options=numeric_columns,
    default=numeric_columns,
    key="preprocessing_scale_columns"
)


scale_method = st.radio(
    "Method",
    [
        "None",
        "Min-Max Scaling",
        "Standardization"
    ],
    key="preprocessing_scale_method"
)


st.divider()


# ============================================================
# APPLY PREPROCESSING
# ============================================================

if st.button(
    "🚀 Apply Preprocessing",
    type="primary",
    use_container_width=True,
    key="apply_preprocessing"
):

    try:

        # ====================================================
        # 1. REMOVE COLUMNS
        # ====================================================

        if remove_cols:

            df = df.drop(
                columns=remove_cols,
                errors="ignore"
            )


        # ====================================================
        # 2. RENAME COLUMN
        # ====================================================

        if (
            rename_col != "None"
            and new_name.strip() != ""
            and rename_col in df.columns
        ):

            new_name = new_name.strip()

            # Prevent duplicate column names
            if (
                new_name != rename_col
                and new_name in df.columns
            ):

                st.error(
                    f"❌ Column '{new_name}' already exists."
                )

                st.stop()


            df = df.rename(
                columns={
                    rename_col: new_name
                }
            )


        # ====================================================
        # 3. HANDLE MISSING VALUES
        # ====================================================

        if missing_option == "Drop Missing Rows":

            df = df.dropna()


        elif missing_option == "Fill Numeric Mean":

            numeric_cols = list(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            if numeric_cols:

                for col in numeric_cols:

                    mean_value = df[col].mean()

                    if pd.notna(mean_value):

                        df[col] = df[col].fillna(
                            mean_value
                        )


        elif missing_option == "Fill Numeric Median":

            numeric_cols = list(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            if numeric_cols:

                for col in numeric_cols:

                    median_value = df[col].median()

                    if pd.notna(median_value):

                        df[col] = df[col].fillna(
                            median_value
                        )


        elif missing_option == "Fill Categorical Mode":

            categorical_cols = list(
                df.select_dtypes(
                    exclude="number"
                ).columns
            )

            for col in categorical_cols:

                mode_values = df[col].mode()

                if not mode_values.empty:

                    df[col] = df[col].fillna(
                        mode_values.iloc[0]
                    )


        # ====================================================
        # 4. REMOVE DUPLICATES
        # ====================================================

        if remove_duplicate:

            df = df.drop_duplicates()


        # ====================================================
        # 5. LABEL ENCODING
        # ====================================================

        # Only encode columns that still exist
        valid_encode_columns = [
            col
            for col in encode_columns
            if col in df.columns
        ]


        for col in valid_encode_columns:

            encoder = LabelEncoder()

            df[col] = encoder.fit_transform(
                df[col].astype(str)
            )


        # ====================================================
        # 6. SCALING
        # ====================================================

        # Only use columns that still exist
        valid_scale_columns = [
            col
            for col in scale_columns
            if col in df.columns
        ]


        if (
            scale_method != "None"
            and len(valid_scale_columns) > 0
        ):

            # -----------------------------------------------
            # MIN-MAX SCALING
            # -----------------------------------------------

            if scale_method == "Min-Max Scaling":

                scaler = MinMaxScaler()

                df[valid_scale_columns] = (
                    scaler.fit_transform(
                        df[
                            valid_scale_columns
                        ]
                    )
                )


            # -----------------------------------------------
            # STANDARDIZATION
            # -----------------------------------------------

            elif scale_method == "Standardization":

                scaler = StandardScaler()

                df[valid_scale_columns] = (
                    scaler.fit_transform(
                        df[
                            valid_scale_columns
                        ]
                    )
                )


        elif scale_method != "None":

            st.info(
                "ℹ️ No valid numeric columns selected "
                "for scaling. Scaling was skipped."
            )


        # ====================================================
        # 7. SAVE PROCESSED DATASET
        # ====================================================

        st.session_state[
            "processed_dataset"
        ] = df.copy()


        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

        st.success(
            "✅ Preprocessing Completed Successfully!"
        )


        # ====================================================
        # PROCESSED DATASET SUMMARY
        # ====================================================

        st.divider()

        st.subheader(
            "📊 Processed Dataset Summary"
        )

        p1, p2, p3, p4 = st.columns(4)

        p1.metric(
            "Rows",
            df.shape[0]
        )

        p2.metric(
            "Columns",
            df.shape[1]
        )

        p3.metric(
            "Missing Values",
            int(
                df.isnull()
                .sum()
                .sum()
            )
        )

        p4.metric(
            "Duplicate Rows",
            int(
                df.duplicated()
                .sum()
            )
        )


        # ====================================================
        # PROCESSED DATASET
        # ====================================================

        st.divider()

        st.subheader(
            "📄 Processed Dataset"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=450
        )


        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.divider()

        st.subheader(
            "⬇️ Download Processed Dataset"
        )

        csv_data = (
            df
            .to_csv(index=False)
            .encode("utf-8")
        )


        st.download_button(
            label="⬇️ Download Processed Dataset",
            data=csv_data,
            file_name="processed_dataset.csv",
            mime="text/csv",
            key="download_processed_dataset"
        )


    except Exception as e:

        st.error(
            f"❌ Preprocessing failed: {e}"
        )


# ============================================================
# SHOW PREVIOUS PROCESSED DATASET
# ============================================================

if (
    "processed_dataset"
    in st.session_state
    and st.button(
        "👁️ View Last Processed Dataset",
        key="view_processed_dataset"
    )
):

    st.divider()

    st.subheader(
        "📄 Last Processed Dataset"
    )

    st.dataframe(
        st.session_state[
            "processed_dataset"
        ],
        use_container_width=True
    )


# ============================================================
# RESET DATASET
# ============================================================

st.divider()

if st.button(
    "♻️ Reset Dataset",
    key="reset_dataset"
):

    st.session_state[
        "processed_dataset"
    ] = st.session_state[
        "dataset"
    ].copy()

    st.success(
        "✅ Dataset Reset Successfully!"
    )

    st.rerun()