import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from theme import apply_theme

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Visualization",
    page_icon="📊",
    layout="wide"
)
apply_theme()

st.title("📊 Data Visualization")
st.caption(
    "Explore and visualize any supported tabular dataset"
)


# ============================================================
# GET DATASET
# ============================================================

if "dataset" not in st.session_state:

    st.warning(
        "⚠️ Please upload a dataset first."
    )

    st.stop()


df = st.session_state["dataset"].copy()


# ============================================================
# DATASET PREVIEW
# ============================================================

st.subheader("📄 Dataset")

st.dataframe(
    df,
    use_container_width=True,
    height=350
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.subheader("📋 Dataset Information")

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
    "Numeric Columns",
    len(
        df.select_dtypes(
            include="number"
        ).columns
    )
)

c4.metric(
    "Categorical Columns",
    len(
        df.select_dtypes(
            exclude="number"
        ).columns
    )
)


# ============================================================
# CHART SELECTION
# ============================================================

st.divider()

st.subheader("📈 Visualization")

chart = st.selectbox(
    "Select Chart Type",
    [
        "Histogram",
        "Bar Chart",
        "Scatter Plot",
        "Line Chart",
        "Box Plot",
        "Pie Chart"
    ],
    key="visualization_chart"
)


# ============================================================
# NUMERIC AND CATEGORICAL COLUMNS
# ============================================================

numeric_columns = (
    df.select_dtypes(
        include="number"
    ).columns.tolist()
)


categorical_columns = (
    df.select_dtypes(
        exclude="number"
    ).columns.tolist()
)


# ============================================================
# HISTOGRAM
# ============================================================

if chart == "Histogram":

    if len(numeric_columns) == 0:

        st.warning(
            "⚠️ Histogram requires at least one numeric column."
        )

    else:

        column = st.selectbox(
            "Select Numeric Column",
            numeric_columns,
            key="histogram_column"
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.hist(
            df[column].dropna(),
            bins=10
        )

        ax.set_title(
            f"Histogram - {column}"
        )

        ax.set_xlabel(
            column
        )

        ax.set_ylabel(
            "Frequency"
        )

        ax.grid(
            alpha=0.25
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# BAR CHART
# ============================================================

elif chart == "Bar Chart":

    if len(categorical_columns) == 0:

        st.warning(
            "⚠️ Bar Chart requires a categorical column."
        )

    else:

        column = st.selectbox(
            "Select Categorical Column",
            categorical_columns,
            key="bar_column"
        )

        counts = (
            df[column]
            .astype(str)
            .value_counts()
            .head(20)
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.bar(
            counts.index,
            counts.values
        )

        ax.set_title(
            f"Bar Chart - {column}"
        )

        ax.set_xlabel(
            column
        )

        ax.set_ylabel(
            "Count"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        ax.grid(
            axis="y",
            alpha=0.25
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# SCATTER PLOT
# ============================================================

elif chart == "Scatter Plot":

    if len(numeric_columns) < 2:

        st.warning(
            "⚠️ Scatter Plot requires at least two numeric columns."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            x_column = st.selectbox(
                "X Axis",
                numeric_columns,
                key="scatter_x"
            )

        with col2:

            y_options = [
                column
                for column in numeric_columns
                if column != x_column
            ]

            y_column = st.selectbox(
                "Y Axis",
                y_options,
                key="scatter_y"
            )


        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        ax.scatter(
            df[x_column],
            df[y_column],
            alpha=0.7,
            s=60
        )

        ax.set_title(
            f"{x_column} vs {y_column}"
        )

        ax.set_xlabel(
            x_column
        )

        ax.set_ylabel(
            y_column
        )

        ax.grid(
            alpha=0.25
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# LINE CHART
# ============================================================

elif chart == "Line Chart":

    if len(numeric_columns) == 0:

        st.warning(
            "⚠️ Line Chart requires numeric data."
        )

    else:

        column = st.selectbox(
            "Select Numeric Column",
            numeric_columns,
            key="line_column"
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.plot(
            df[column].reset_index(drop=True)
        )

        ax.set_title(
            f"Line Chart - {column}"
        )

        ax.set_xlabel(
            "Record"
        )

        ax.set_ylabel(
            column
        )

        ax.grid(
            alpha=0.25
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# BOX PLOT
# ============================================================

elif chart == "Box Plot":

    if len(numeric_columns) == 0:

        st.warning(
            "⚠️ Box Plot requires numeric data."
        )

    else:

        selected_columns = st.multiselect(
            "Select Numeric Columns",
            numeric_columns,
            default=numeric_columns[:min(
                3,
                len(numeric_columns)
            )],
            key="box_columns"
        )

        if len(selected_columns) == 0:

            st.info(
                "Select at least one numeric column."
            )

        else:

            fig, ax = plt.subplots(
                figsize=(10, 6)
            )

            ax.boxplot(
                [
                    df[column].dropna()
                    for column in selected_columns
                ],
                labels=selected_columns
            )

            ax.set_title(
                "Box Plot"
            )

            ax.set_ylabel(
                "Values"
            )

            plt.xticks(
                rotation=30
            )

            ax.grid(
                axis="y",
                alpha=0.25
            )

            st.pyplot(fig)

            plt.close(fig)


# ============================================================
# PIE CHART
# ============================================================

elif chart == "Pie Chart":

    if len(categorical_columns) == 0:

        st.warning(
            "⚠️ Pie Chart requires a categorical column."
        )

    else:

        column = st.selectbox(
            "Select Categorical Column",
            categorical_columns,
            key="pie_column"
        )

        counts = (
            df[column]
            .astype(str)
            .value_counts()
            .head(10)
        )

        fig, ax = plt.subplots(
            figsize=(7, 7)
        )

        ax.pie(
            counts.values,
            labels=counts.index,
            autopct="%1.1f%%"
        )

        ax.set_title(
            f"Distribution - {column}"
        )

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# CORRELATION MATRIX
# ============================================================

st.divider()

st.subheader("🔗 Correlation Matrix")

if len(numeric_columns) >= 2:

    correlation = df[
        numeric_columns
    ].corr()

    st.dataframe(
        correlation.round(3),
        use_container_width=True
    )

else:

    st.info(
        "Correlation matrix requires at least two numeric columns."
    )


# ============================================================
# SUMMARY
# ============================================================

st.divider()

st.success(
    "✅ Visualization completed successfully."
)