import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from theme import apply_theme
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Simple K-Means",
    page_icon="🔵",
    layout="wide"
)
apply_theme()

st.title("🔵 Simple K-Means Clustering")
st.caption(
    "Professional K-Means clustering for numeric and categorical datasets"
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
    use_container_width=True
)


# ============================================================
# SELECT FEATURES
# ============================================================

st.subheader("🎯 Clustering Features")

feature_columns = st.multiselect(
    "Select columns to use for clustering",
    df.columns.tolist(),
    default=df.columns.tolist(),
    key="kmeans_features"
)


if len(feature_columns) == 0:

    st.warning(
        "⚠️ Please select at least one feature."
    )

    st.stop()


# ============================================================
# K VALUE
# ============================================================

st.subheader("⚙️ K-Means Settings")

col1, col2 = st.columns(2)


with col1:

    k = st.number_input(
        "Number of Clusters (K)",
        min_value=2,
        max_value=15,
        value=3,
        step=1,
        key="kmeans_k"
    )


with col2:

    random_state = st.number_input(
        "Random State",
        min_value=0,
        max_value=999,
        value=42,
        step=1,
        key="kmeans_random"
    )


# ============================================================
# PREPARE DATA
# ============================================================

data = df[
    feature_columns
].copy()


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

for column in data.columns:

    if pd.api.types.is_numeric_dtype(
        data[column]
    ):

        if data[column].isnull().any():

            data[column] = data[column].fillna(
                data[column].median()
            )

    else:

        data[column] = data[column].fillna(
            "Missing"
        )


# ============================================================
# IDENTIFY NUMERIC / CATEGORICAL
# ============================================================

numeric_columns = [
    column
    for column in data.columns
    if pd.api.types.is_numeric_dtype(
        data[column]
    )
]


categorical_columns = [
    column
    for column in data.columns
    if column not in numeric_columns
]


# ============================================================
# PREPROCESSING
# ============================================================

transformers = []


if len(numeric_columns) > 0:

    transformers.append(
        (
            "numeric",
            StandardScaler(),
            numeric_columns
        )
    )


if len(categorical_columns) > 0:

    transformers.append(
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_columns
        )
    )


preprocessor = ColumnTransformer(
    transformers=transformers,
    remainder="drop"
)


processed_data = preprocessor.fit_transform(
    data
)


# ============================================================
# RUN K-MEANS
# ============================================================

if st.button(
    "🚀 Run K-Means",
    type="primary",
    key="run_kmeans"
):

    # ========================================================
    # K-MEANS MODEL
    # ========================================================

    model = KMeans(
        n_clusters=int(k),
        random_state=int(random_state),
        n_init=10
    )


    # ========================================================
    # FIT MODEL
    # ========================================================

    clusters = model.fit_predict(
        processed_data
    )


    # ========================================================
    # ADD CLUSTERS
    # ========================================================

    result = df.copy()

    result["Cluster"] = (
        clusters + 1
    )


    # ========================================================
    # HEADER
    # ========================================================

    st.divider()

    st.subheader(
        "🎯 Clustering Results"
    )


    # ========================================================
    # CLUSTER COUNTS
    # ========================================================

    cluster_counts = (
        pd.Series(clusters + 1)
        .value_counts()
        .sort_index()
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Number of Clusters",
        int(k)
    )


    c2.metric(
        "Total Records",
        len(data)
    )


    c3.metric(
        "WCSS / Inertia",
        f"{model.inertia_:.3f}"
    )


    # ========================================================
    # CLUSTER DISTRIBUTION
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Cluster Distribution"
    )


    distribution_df = pd.DataFrame({
        "Cluster": [
            f"Cluster {x}"
            for x in cluster_counts.index
        ],
        "Records": cluster_counts.values,
        "Percentage": [
            f"{(x / len(data)) * 100:.1f}%"
            for x in cluster_counts.values
        ]
    })


    st.dataframe(
        distribution_df,
        use_container_width=True
    )


    # ========================================================
    # PCA
    # ========================================================

    st.divider()

    st.subheader(
        "🧭 PCA Cluster Map"
    )


    # PCA requires at least 2 dimensions
    if processed_data.shape[1] >= 2:

        pca = PCA(
            n_components=2
        )


        pca_data = pca.fit_transform(
            processed_data
        )


        # ----------------------------------------------------
        # Transform cluster centers
        # ----------------------------------------------------

        center_2d = pca.transform(
            model.cluster_centers_
        )


        # ----------------------------------------------------
        # Plot
        # ----------------------------------------------------

        fig, ax = plt.subplots(
            figsize=(11, 7)
        )


        colors = [
            "#2563EB",
            "#16A34A",
            "#DC2626",
            "#9333EA",
            "#EA580C",
            "#0891B2",
            "#DB2777",
            "#65A30D"
        ]


        for cluster_number in range(
            int(k)
        ):

            mask = (
                clusters
                == cluster_number
            )


            ax.scatter(
                pca_data[
                    mask,
                    0
                ],
                pca_data[
                    mask,
                    1
                ],
                s=90,
                alpha=0.75,
                color=colors[
                    cluster_number
                    % len(colors)
                ],
                label=(
                    f"Cluster "
                    f"{cluster_number + 1}"
                    f" ({mask.sum()} records)"
                )
            )


            # ------------------------------------------------
            # Cluster center
            # ------------------------------------------------

            ax.scatter(
                center_2d[
                    cluster_number,
                    0
                ],
                center_2d[
                    cluster_number,
                    1
                ],
                marker="*",
                s=400,
                color="black",
                edgecolors="white",
                linewidths=1.5
            )


            ax.annotate(
                f"C{cluster_number + 1}",
                (
                    center_2d[
                        cluster_number,
                        0
                    ],
                    center_2d[
                        cluster_number,
                        1
                    ]
                ),
                fontsize=12,
                fontweight="bold",
                xytext=(8, 8),
                textcoords="offset points"
            )


        # ----------------------------------------------------
        # Labels
        # ----------------------------------------------------

        explained_1 = (
            pca.explained_variance_ratio_[0]
            * 100
        )


        explained_2 = (
            pca.explained_variance_ratio_[1]
            * 100
        )


        ax.set_xlabel(
            f"Principal Component 1 "
            f"({explained_1:.1f}% variance)"
        )


        ax.set_ylabel(
            f"Principal Component 2 "
            f"({explained_2:.1f}% variance)"
        )


        ax.set_title(
            "K-Means Cluster Visualization"
        )


        ax.legend(
            loc="best"
        )


        ax.grid(
            alpha=0.25
        )


        st.pyplot(
            fig,
            use_container_width=True
        )


        plt.close(fig)


        st.info(
            "⭐ Stars represent the center of each cluster. "
            "PCA converts multiple dataset features into "
            "two dimensions only for visualization."
        )


    else:

        st.info(
            "PCA visualization requires at least "
            "two processed dimensions."
        )


    # ========================================================
    # SILHOUETTE SCORE
    # ========================================================

    st.divider()

    st.subheader(
        "📐 Clustering Quality"
    )


    if len(set(clusters)) > 1:

        silhouette = silhouette_score(
            processed_data,
            clusters
        )


        c1, c2 = st.columns(2)


        c1.metric(
            "Silhouette Score",
            f"{silhouette:.4f}"
        )


        if silhouette >= 0.7:

            quality = "Excellent"

        elif silhouette >= 0.5:

            quality = "Good"

        elif silhouette >= 0.25:

            quality = "Moderate"

        else:

            quality = "Weak"


        c2.metric(
            "Cluster Quality",
            quality
        )


    # ========================================================
    # ELBOW METHOD
    # ========================================================

    st.divider()

    st.subheader(
        "📉 Elbow Method"
    )


    max_k = min(
        10,
        len(data) - 1
    )


    if max_k >= 2:

        inertia_values = []

        k_values = range(
            2,
            max_k + 1
        )


        for current_k in k_values:

            temp_model = KMeans(
                n_clusters=current_k,
                random_state=int(random_state),
                n_init=10
            )


            temp_model.fit(
                processed_data
            )


            inertia_values.append(
                temp_model.inertia_
            )


        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )


        ax2.plot(
            list(k_values),
            inertia_values,
            marker="o",
            linewidth=2
        )


        # Highlight selected K
        if int(k) >= 2 and int(k) <= max_k:

            selected_index = (
                int(k) - 2
            )


            ax2.scatter(
                int(k),
                inertia_values[
                    selected_index
                ],
                s=180,
                marker="*",
                color="red",
                zorder=5,
                label=f"Selected K = {k}"
            )


            ax2.legend()


        ax2.set_xlabel(
            "Number of Clusters (K)"
        )


        ax2.set_ylabel(
            "WCSS / Inertia"
        )


        ax2.set_title(
            "Elbow Method for Choosing K"
        )


        ax2.grid(
            alpha=0.25
        )


        st.pyplot(
            fig2,
            use_container_width=True
        )


        plt.close(fig2)


        st.info(
            "💡 The elbow point is where the decrease "
            "in WCSS starts becoming smaller."
        )


    # ========================================================
    # CLUSTERED DATASET
    # ========================================================

    st.divider()

    st.subheader(
        "📄 Clustered Dataset"
    )


    st.dataframe(
        result,
        use_container_width=True,
        height=400
    )


    # ========================================================
    # CLUSTER SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Cluster Summary"
    )


    # Numeric summary
    if len(numeric_columns) > 0:

        numeric_summary = (
            result
            .groupby("Cluster")[
                numeric_columns
            ]
            .mean()
            .round(3)
        )


        st.markdown(
            "### 🔢 Numeric Feature Averages"
        )


        st.dataframe(
            numeric_summary,
            use_container_width=True
        )


    # Categorical summary
    if len(categorical_columns) > 0:

        categorical_summary = []


        for cluster_number in sorted(
            result["Cluster"].unique()
        ):

            cluster_data = result[
                result["Cluster"]
                == cluster_number
            ]


            row = {
                "Cluster":
                    f"Cluster {cluster_number}"
            }


            for column in categorical_columns:

                mode_values = (
                    cluster_data[column]
                    .mode()
                )


                if len(mode_values) > 0:

                    row[column] = (
                        mode_values.iloc[0]
                    )

                else:

                    row[column] = "N/A"


            categorical_summary.append(
                row
            )


        categorical_summary_df = (
            pd.DataFrame(
                categorical_summary
            )
        )


        st.markdown(
            "### 🏷️ Dominant Categorical Values"
        )


        st.dataframe(
            categorical_summary_df,
            use_container_width=True
        )


    # ========================================================
    # FEATURE INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "🔍 Features Used"
    )


    feature_info = pd.DataFrame({
        "Feature": feature_columns,
        "Type": [
            "Numeric"
            if column in numeric_columns
            else "Categorical"
            for column in feature_columns
        ]
    })


    st.dataframe(
        feature_info,
        use_container_width=True
    )

    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.divider()

    st.subheader(
        "⬇️ Download Results"
    )

    csv = result.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download Clustered Dataset",
        data=csv,
        file_name="kmeans_clustered_dataset.csv",
        mime="text/csv",
        key="download_kmeans"
    )

    # ========================================================
    # COMPLETE
    # ========================================================

    st.divider()

    st.success(
        "✅ K-Means clustering completed successfully."
    )