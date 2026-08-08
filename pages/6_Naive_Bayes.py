import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from theme import apply_theme

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    cohen_kappa_score,
    classification_report,
    roc_curve,
    auc
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Naive Bayes",
    page_icon="🧠",
    layout="wide"
)

apply_theme()

st.title(
    "🧠 Naive Bayes Classification"
)

st.caption(
    "Naive Bayes classification for categorical and numeric datasets"
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

st.subheader(
    "📄 Dataset"
)

st.dataframe(
    df,
    use_container_width=True
)
# ============================================================
# TARGET COLUMN
# ============================================================

st.subheader(
    "🎯 Class Attribute"
)

target_column = st.selectbox(
    "Select Class / Target Column",
    df.columns.tolist(),
    index=len(df.columns) - 1,
    key="nb_target"
)
# ============================================================
# SETTINGS
# ============================================================

st.subheader(
    "⚙️ Naive Bayes Settings"
)

col1, col2 = st.columns(2)


with col1:

    test_size_percent = st.slider(
        "Test Size (%)",
        min_value=10,
        max_value=40,
        value=20,
        step=5,
        key="nb_test_size"
    )


with col2:

    st.info(
        "Gaussian Naive Bayes is used for numeric data "
        "after automatic categorical encoding."
    )


test_size = test_size_percent / 100
# ============================================================
# RUN NAIVE BAYES
# ============================================================

if st.button(
    "🚀 Run Naive Bayes",
    type="primary",
    key="run_naive_bayes"
):

    # ========================================================
    # COPY DATA
    # ========================================================

    data = df.copy()
        # ========================================================
    # HANDLE MISSING VALUES
    # ========================================================

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


    # ========================================================
    # REMOVE MISSING TARGET
    # ========================================================

    data = data.dropna(
        subset=[target_column]
    )
        # ========================================================
    # X AND Y
    # ========================================================

    X = data.drop(
        columns=[target_column]
    )

    y = data[target_column]
        # ========================================================
    # ENCODE CATEGORICAL FEATURES
    # ========================================================

    feature_encoders = {}

    for column in X.columns:

        if not pd.api.types.is_numeric_dtype(
            X[column]
        ):

            encoder = LabelEncoder()

            X[column] = encoder.fit_transform(
                X[column].astype(str)
            )

            feature_encoders[column] = encoder
                # ========================================================
    # ENCODE TARGET
    # ========================================================

    target_encoder = LabelEncoder()

    y_encoded = target_encoder.fit_transform(
        y.astype(str)
    )
        # ========================================================
    # TRAIN TEST SPLIT
    # ========================================================

    try:

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y_encoded,
                test_size=test_size,
                random_state=42,
                stratify=y_encoded
            )
        )

    except ValueError:

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y_encoded,
                test_size=test_size,
                random_state=42,
                stratify=None
            )
        )
            # ========================================================
    # MODEL
    # ========================================================

    model = GaussianNB()


    # ========================================================
    # TRAIN
    # ========================================================

    model.fit(
        X_train,
        y_train
    )


    # ========================================================
    # PREDICTION
    # ========================================================

    y_pred = model.predict(
        X_test
    )
        # ========================================================
    # ACCURACY
    # ========================================================

    accuracy = accuracy_score(
        y_test,
        y_pred
    )


    # ========================================================
    # KAPPA
    # ========================================================

    kappa = cohen_kappa_score(
        y_test,
        y_pred
    )


    # ========================================================
    # PERFORMANCE
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Overall Model Performance"
    )

    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Accuracy",
        f"{accuracy * 100:.2f}%"
    )


    c2.metric(
        "Kappa Statistic",
        f"{kappa:.4f}"
    )


    c3.metric(
        "Test Instances",
        len(y_test)
    )
        # ========================================================
    # PREDICTIONS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Predictions"
    )

    prediction_df = X_test.copy()

    prediction_df["Actual"] = (
        target_encoder.inverse_transform(
            y_test
        )
    )

    prediction_df["Predicted"] = (
        target_encoder.inverse_transform(
            y_pred
        )
    )

    prediction_df["Correct"] = (
        prediction_df["Actual"]
        ==
        prediction_df["Predicted"]
    )

    st.dataframe(
        prediction_df,
        use_container_width=True
    )
        # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    st.divider()

    st.subheader(
        "🔲 Confusion Matrix"
    )

    class_names = (
        target_encoder.classes_
    )

    labels = list(
        range(
            len(class_names)
        )
    )

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=labels
    )

    cm_df = pd.DataFrame(
        cm,
        index=[
            "Actual " + str(x)
            for x in class_names
        ],
        columns=[
            "Predicted " + str(x)
            for x in class_names
        ]
    )

    st.dataframe(
        cm_df,
        use_container_width=True
    )
        # ========================================================
    # CLASSIFICATION REPORT
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Classification Report"
    )

    report = classification_report(
        y_test,
        y_pred,
        labels=labels,
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )

    st.dataframe(
        pd.DataFrame(
            report
        ).transpose(),
        use_container_width=True
    )
        # ========================================================
    # WEKA-STYLE ROC CURVE
    # ========================================================

    st.divider()

    st.subheader(
        "📈 ROC Curve"
    )


    # ========================================================
    # BINARY DATASET
    # ========================================================

    if len(class_names) == 2:

        probabilities = model.predict_proba(
            X_test
        )[:, 1]

        fpr, tpr, _ = roc_curve(
            y_test,
            probabilities
        )

        roc_auc = auc(
            fpr,
            tpr
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.plot(
            fpr,
            tpr,
            linewidth=2,
            label=f"AUC = {roc_auc:.3f}"
        )

        ax.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            label="Random Classifier"
        )

        ax.set_xlabel(
            "False Positive Rate"
        )

        ax.set_ylabel(
            "True Positive Rate"
        )

        ax.set_title(
            "ROC Curve - Naive Bayes"
        )

        ax.legend(
            loc="lower right"
        )

        ax.grid(
            alpha=0.25
        )

        st.pyplot(fig)

        plt.close(fig)

        st.success(
            f"🎯 ROC AUC = {roc_auc:.4f}"
        )


    # ========================================================
    # MULTICLASS DATASET
    # WEKA-STYLE CLASS SELECTION
    # ========================================================

    else:

        roc_class_name = st.selectbox(
            "Select Class for ROC Curve",
            list(class_names),
            key="nb_roc_class"
        )

        st.caption(
            f"ROC Curve: {roc_class_name} vs Rest"
        )

        roc_class_index = list(
            class_names
        ).index(
            roc_class_name
        )

        probabilities = model.predict_proba(
            X_test
        )[:, roc_class_index]

        y_binary = (
            y_test == roc_class_index
        ).astype(int)

        try:

            fpr, tpr, _ = roc_curve(
                y_binary,
                probabilities
            )

            roc_auc = auc(
                fpr,
                tpr
            )

            fig, ax = plt.subplots(
                figsize=(7, 5)
            )

            ax.plot(
                fpr,
                tpr,
                linewidth=2,
                label=(
                    f"{roc_class_name} vs Rest "
                    f"(AUC = {roc_auc:.3f})"
                )
            )

            ax.plot(
                [0, 1],
                [0, 1],
                linestyle="--",
                label="Random Classifier"
            )

            ax.set_xlim(
                0,
                1
            )

            ax.set_ylim(
                0,
                1.05
            )

            ax.set_xlabel(
                "False Positive Rate"
            )

            ax.set_ylabel(
                "True Positive Rate"
            )

            ax.set_title(
                "ROC Curve - Naive Bayes"
            )

            ax.legend(
                loc="lower right"
            )

            ax.grid(
                alpha=0.25
            )

            st.pyplot(fig)

            plt.close(fig)

            st.success(
                f"🎯 ROC AUC ({roc_class_name}) = "
                f"{roc_auc:.4f}"
            )

        except ValueError:

            st.warning(
                "⚠️ ROC curve cannot be calculated "
                "for the selected class."
            )
                # ========================================================
    # FEATURE INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Dataset Features Used"
    )

    feature_info = pd.DataFrame({
        "Column": X.columns,
        "Data Type": [
            str(df[column].dtype)
            for column in X.columns
        ]
    })

    st.dataframe(
        feature_info,
        use_container_width=True
    )
        # ========================================================
    # COMPLETE
    # ========================================================

    st.divider()

    st.success(
        "✅ Naive Bayes analysis completed successfully."
    )