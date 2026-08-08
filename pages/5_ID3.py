import streamlit as st
import pandas as pd
import numpy as np
from theme import apply_theme

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    cohen_kappa_score,
    classification_report,
    roc_curve,
    auc
)

import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ID3 Decision Tree",
    page_icon="🌳",
    layout="wide"
)
apply_theme()

st.title("🌳 ID3 Decision Tree")
st.caption(
    "ID3 Classification using Entropy and Information Gain"
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
# DATASET
# ============================================================

st.subheader("📄 Dataset")

st.dataframe(
    df,
    use_container_width=True
)


# ============================================================
# TARGET
# ============================================================

st.subheader("🎯 Class Attribute")

target_column = st.selectbox(
    "Select Class / Target Column",
    df.columns.tolist(),
    index=len(df.columns) - 1,
    key="id3_target"
)


# ============================================================
# SETTINGS
# ============================================================

st.subheader("⚙️ ID3 Settings")

col1, col2 = st.columns(2)


with col1:

    max_depth = st.number_input(
        "Maximum Depth",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
        key="id3_depth"
    )


with col2:

    test_size_percent = st.slider(
        "Test Size (%)",
        min_value=10,
        max_value=40,
        value=20,
        step=5,
        key="id3_test"
    )


test_size = test_size_percent / 100


# ============================================================
# RUN ID3
# ============================================================

if st.button(
    "🚀 Run ID3",
    type="primary",
    key="run_id3"
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
    # X AND Y
    # ========================================================

    X = data.drop(
        columns=[target_column]
    )

    y = data[target_column]


    # ========================================================
    # ENCODE CATEGORICAL INPUT COLUMNS
    # ========================================================

    encoders = {}

    for column in X.columns:

        if not pd.api.types.is_numeric_dtype(
            X[column]
        ):

            encoder = LabelEncoder()

            X[column] = encoder.fit_transform(
                X[column].astype(str)
            )

            encoders[column] = encoder


    # ========================================================
    # ENCODE TARGET
    # ========================================================

    target_encoder = LabelEncoder()

    y_encoded = target_encoder.fit_transform(
        y.astype(str)
    )


    # ========================================================
    # TRAIN / TEST SPLIT
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
    # ID3 MODEL
    # ========================================================

    model = DecisionTreeClassifier(
        criterion="entropy",
        max_depth=max_depth,
        random_state=42
    )


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
    # CONFUSION MATRIX
    # ========================================================

    st.divider()

    st.subheader(
        "🔲 Confusion Matrix"
    )


    labels = list(
        range(
            len(
                target_encoder.classes_
            )
        )
    )


    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=labels
    )


    class_names = (
        target_encoder.classes_
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
    # DECISION TREE
    # ========================================================

    st.divider()

    st.subheader(
        "🌳 ID3 Decision Tree"
    )


    from sklearn.tree import export_graphviz


    dot_data = export_graphviz(
        model,
        out_file=None,
        feature_names=X.columns,
        class_names=[
            str(x)
            for x in class_names
        ],
        filled=True,
        rounded=True,
        special_characters=True
    )


    st.graphviz_chart(
        dot_data,
        use_container_width=True
    )


    # ========================================================
    # FEATURE INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Feature Information"
    )


    feature_info = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    })


    feature_info = feature_info.sort_values(
        "Importance",
        ascending=False
    )


    st.dataframe(
        feature_info,
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

        positive_class_index = 1

        probabilities = model.predict_proba(
            X_test
        )[:, positive_class_index]

        fpr, tpr, _ = roc_curve(
            y_test,
            probabilities,
            pos_label=positive_class_index
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
            "ROC Curve - ID3"
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
            key="id3_roc_class"
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
                "ROC Curve - ID3"
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
    # IF - THEN RULES
    # ========================================================

    st.divider()

    st.subheader(
        "📜 IF–THEN Rules"
    )


    tree = model.tree_


    feature_names = X.columns


    def generate_rules(
        node,
        conditions=None
    ):

        if conditions is None:

            conditions = []


        rules = []


        # ----------------------------------------------------
        # LEAF
        # ----------------------------------------------------

        if (
            tree.children_left[node]
            == tree.children_right[node]
        ):

            class_index = np.argmax(
                tree.value[node][0]
            )


            class_name = (
                class_names[class_index]
            )


            condition_text = (
                " AND ".join(
                    conditions
                )
            )


            rules.append(
                "IF "
                + condition_text
                + " THEN "
                + target_column
                + " = "
                + str(class_name)
            )


            return rules


        # ----------------------------------------------------
        # FEATURE
        # ----------------------------------------------------

        feature_index = (
            tree.feature[node]
        )


        feature_name = (
            feature_names[
                feature_index
            ]
        )


        threshold = (
            tree.threshold[node]
        )


        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        left_condition = (
            f"{feature_name} <= "
            f"{threshold:.4f}"
        )


        rules.extend(
            generate_rules(
                tree.children_left[node],
                conditions
                + [left_condition]
            )
        )


        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        right_condition = (
            f"{feature_name} > "
            f"{threshold:.4f}"
        )


        rules.extend(
            generate_rules(
                tree.children_right[node],
                conditions
                + [right_condition]
            )
        )


        return rules


    rules = generate_rules(
        0
    )


    for i, rule in enumerate(
        rules,
        start=1
    ):

        st.markdown(
            f"**Rule {i}:** `{rule}`"
        )


    # ========================================================
    # COMPLETE
    # ========================================================

    st.divider()

    st.success(
        "✅ ID3 analysis completed successfully."
    )