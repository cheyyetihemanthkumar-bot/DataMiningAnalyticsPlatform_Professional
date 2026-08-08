import streamlit as st
import pandas as pd
import numpy as np
import math

from theme import apply_theme

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    cohen_kappa_score,
    classification_report,
    roc_curve,
    auc
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="J48 Decision Tree",
    page_icon="🌳",
    layout="wide"
)
apply_theme()

st.title("🌳 J48 Decision Tree")
st.caption(
    "C4.5 / J48 using Entropy, Information Gain and Gain Ratio"
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
# SELECT CLASS ATTRIBUTE
# ============================================================

st.subheader("🎯 Class Attribute")

target_column = st.selectbox(
    "Select Class / Target Column",
    df.columns.tolist(),
    index=len(df.columns) - 1,
    key="j48_target"
)


# ============================================================
# J48 SETTINGS
# ============================================================

st.subheader("⚙️ J48 Settings")

col1, col2 = st.columns(2)

with col1:

    max_depth = st.number_input(
        "Maximum Depth",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
        key="j48_depth"
    )

with col2:

    test_size_percent = st.slider(
        "Test Size (%)",
        min_value=10,
        max_value=40,
        value=20,
        step=5,
        key="j48_test"
    )

test_size = test_size_percent / 100


# ============================================================
# ENTROPY
# ============================================================

def entropy(values):

    if len(values) == 0:
        return 0.0

    counts = pd.Series(values).value_counts()

    total = len(values)

    result = 0.0

    for count in counts:

        probability = count / total

        if probability > 0:

            result -= (
                probability
                * math.log2(probability)
            )

    return result


# ============================================================
# INFORMATION GAIN
# ============================================================

def information_gain(
    parent_values,
    groups
):

    parent_entropy = entropy(
        parent_values
    )

    total = len(parent_values)

    weighted_entropy = 0.0

    for group in groups:

        if len(group) == 0:
            continue

        weighted_entropy += (
            len(group) / total
        ) * entropy(group)

    return (
        parent_entropy
        - weighted_entropy
    )


# ============================================================
# SPLIT INFORMATION
# ============================================================

def split_information(
    groups,
    total
):

    if total == 0:
        return 0.0

    result = 0.0

    for group in groups:

        if len(group) == 0:
            continue

        probability = len(group) / total

        result -= (
            probability
            * math.log2(probability)
        )

    return result


# ============================================================
# GAIN RATIO
# ============================================================

def calculate_gain_ratio(
    gain,
    split_info
):

    if split_info == 0:
        return 0.0

    return gain / split_info


# ============================================================
# FIND BEST NUMERIC SPLIT
# ============================================================

def best_numeric_split(
    data,
    target,
    attribute
):

    values = sorted(
        data[attribute]
        .dropna()
        .unique()
    )

    if len(values) < 2:

        return (
            None,
            -1,
            0,
            -1
        )

    best_threshold = None
    best_gain = -1
    best_split = 0
    best_ratio = -1

    parent = data[target].values

    for i in range(
        len(values) - 1
    ):

        threshold = (
            values[i]
            + values[i + 1]
        ) / 2

        left = data[
            data[attribute] <= threshold
        ]

        right = data[
            data[attribute] > threshold
        ]

        if (
            len(left) == 0
            or len(right) == 0
        ):
            continue

        groups = [
            left[target].values,
            right[target].values
        ]

        gain = information_gain(
            parent,
            groups
        )

        split_info = split_information(
            groups,
            len(data)
        )

        ratio = calculate_gain_ratio(
            gain,
            split_info
        )

        if ratio > best_ratio:

            best_threshold = threshold
            best_gain = gain
            best_split = split_info
            best_ratio = ratio

    return (
        best_threshold,
        best_gain,
        best_split,
        best_ratio
    )


# ============================================================
# ATTRIBUTE EVALUATION
# ============================================================

def evaluate_attributes(
    data,
    target,
    attributes
):

    rows = []

    parent = data[target].values

    parent_entropy = entropy(
        parent
    )

    for attribute in attributes:

        column = data[attribute]

        # ----------------------------------------------------
        # NUMERIC ATTRIBUTE
        # ----------------------------------------------------

        if pd.api.types.is_numeric_dtype(
            column
        ):

            (
                threshold,
                gain,
                split_info,
                ratio
            ) = best_numeric_split(
                data,
                target,
                attribute
            )

            if threshold is None:
                continue

            rows.append({
                "Attribute": attribute,
                "Entropy": parent_entropy,
                "Information Gain": gain,
                "Split Information": split_info,
                "Gain Ratio": ratio,
                "Split": f"<= {threshold:.3f} / > {threshold:.3f}"
            })

        # ----------------------------------------------------
        # CATEGORICAL ATTRIBUTE
        # ----------------------------------------------------

        else:

            values = data[
                attribute
            ].dropna().unique()

            if len(values) < 2:
                continue

            groups = []

            for value in values:

                subset = data[
                    data[attribute] == value
                ]

                groups.append(
                    subset[target].values
                )

            gain = information_gain(
                parent,
                groups
            )

            split_info = split_information(
                groups,
                len(data)
            )

            ratio = calculate_gain_ratio(
                gain,
                split_info
            )

            rows.append({
                "Attribute": attribute,
                "Entropy": parent_entropy,
                "Information Gain": gain,
                "Split Information": split_info,
                "Gain Ratio": ratio,
                "Split": "Categorical"
            })

    if len(rows) == 0:

        return pd.DataFrame()

    return pd.DataFrame(rows)


# ============================================================
# TREE NODE
# ============================================================

class TreeNode:

    def __init__(
        self,
        attribute=None,
        prediction=None,
        gain=0.0,
        split_info=0.0,
        gain_ratio=0.0,
        threshold=None,
        samples=0,
        class_counts=None
    ):

        self.attribute = attribute

        self.prediction = prediction

        self.gain = gain

        self.split_info = split_info

        self.gain_ratio = gain_ratio

        self.threshold = threshold

        self.samples = samples

        self.class_counts = (
            class_counts
            if class_counts is not None
            else {}
        )

        self.children = {}


# ============================================================
# BUILD TREE
# ============================================================

def build_tree(
    data,
    target,
    attributes,
    depth,
    max_depth
):

    majority_class = (
        data[target]
        .value_counts()
        .idxmax()
    )

    samples = len(data)

    class_counts = (
        data[target]
        .value_counts()
        .to_dict()
    )

    # --------------------------------------------------------
    # PURE NODE
    # --------------------------------------------------------

    if data[target].nunique() == 1:

        return TreeNode(
            prediction=data[target].iloc[0],
            samples=samples,
            class_counts=class_counts
        )

    # --------------------------------------------------------
    # MAX DEPTH
    # --------------------------------------------------------

    if depth >= max_depth:

        return TreeNode(
            prediction=majority_class,
            samples=samples,
            class_counts=class_counts
        )

    # --------------------------------------------------------
    # NO ATTRIBUTES
    # --------------------------------------------------------

    if len(attributes) == 0:

        return TreeNode(
            prediction=majority_class,
            samples=samples,
            class_counts=class_counts
        )

    # --------------------------------------------------------
    # EVALUATE ATTRIBUTES
    # --------------------------------------------------------

    scores = evaluate_attributes(
        data,
        target,
        attributes
    )

    if scores.empty:

        return TreeNode(
            prediction=majority_class,
            samples=samples,
            class_counts=class_counts
        )

    # Highest Gain Ratio
    scores = scores.sort_values(
        "Gain Ratio",
        ascending=False
    )

    best = scores.iloc[0]

    best_attribute = best[
        "Attribute"
    ]

    best_gain = best[
        "Information Gain"
    ]

    best_split = best[
        "Split Information"
    ]

    best_ratio = best[
        "Gain Ratio"
    ]

    # --------------------------------------------------------
    # CREATE DECISION NODE
    # --------------------------------------------------------

    node = TreeNode(
        attribute=best_attribute,
        prediction=majority_class,
        gain=best_gain,
        split_info=best_split,
        gain_ratio=best_ratio,
        samples=samples,
        class_counts=class_counts
    )

    remaining_attributes = [
        attribute
        for attribute in attributes
        if attribute != best_attribute
    ]

    # --------------------------------------------------------
    # CATEGORICAL ATTRIBUTE
    # --------------------------------------------------------

    if not pd.api.types.is_numeric_dtype(
        data[best_attribute]
    ):

        values = (
            data[best_attribute]
            .dropna()
            .unique()
        )

        for value in values:

            subset = data[
                data[best_attribute] == value
            ]

            if len(subset) == 0:
                continue

            child = build_tree(
                subset,
                target,
                remaining_attributes,
                depth + 1,
                max_depth
            )

            node.children[
                str(value)
            ] = child

    # --------------------------------------------------------
    # NUMERIC ATTRIBUTE
    # --------------------------------------------------------

    else:

        (
            threshold,
            gain,
            split_info,
            ratio
        ) = best_numeric_split(
            data,
            target,
            best_attribute
        )

        node.threshold = threshold

        if threshold is not None:

            left = data[
                data[best_attribute]
                <= threshold
            ]

            right = data[
                data[best_attribute]
                > threshold
            ]

            if len(left) > 0:

                node.children[
                    f"<= {threshold:.3f}"
                ] = build_tree(
                    left,
                    target,
                    remaining_attributes,
                    depth + 1,
                    max_depth
                )

            if len(right) > 0:

                node.children[
                    f"> {threshold:.3f}"
                ] = build_tree(
                    right,
                    target,
                    remaining_attributes,
                    depth + 1,
                    max_depth
                )

    return node


# ============================================================
# PREDICTION
# ============================================================

def predict_one(
    node,
    row
):

    # Leaf
    if node.attribute is None:

        return node.prediction

    value = row[
        node.attribute
    ]

    # --------------------------------------------------------
    # NUMERIC
    # --------------------------------------------------------

    if node.threshold is not None:

        if value <= node.threshold:

            branch = (
                f"<= {node.threshold:.3f}"
            )

        else:

            branch = (
                f"> {node.threshold:.3f}"
            )

        if branch in node.children:

            return predict_one(
                node.children[branch],
                row
            )

        return node.prediction

    # --------------------------------------------------------
    # CATEGORICAL
    # --------------------------------------------------------

    branch = str(value)

    if branch in node.children:

        return predict_one(
            node.children[branch],
            row
        )

    return node.prediction


def predict(
    node,
    X
):

    predictions = []

    for _, row in X.iterrows():

        predictions.append(
            predict_one(
                node,
                row
            )
        )

    return np.array(
        predictions
    )


# ============================================================
# START J48
# ============================================================

if st.button(
    "🚀 Run J48",
    type="primary",
    key="run_j48"
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

                data[column] = (
                    data[column]
                    .fillna(
                        data[column].median()
                    )
                )

        else:

            data[column] = (
                data[column]
                .fillna("Missing")
            )


    # ========================================================
    # REMOVE MISSING TARGET
    # ========================================================

    data = data.dropna(
        subset=[target_column]
    )


    # ========================================================
    # ATTRIBUTES
    # ========================================================

    attributes = [
        column
        for column in data.columns
        if column != target_column
    ]


    # ========================================================
    # TRAIN TEST SPLIT
    # ========================================================

    try:

        train_data, test_data = (
            train_test_split(
                data,
                test_size=test_size,
                random_state=42,
                stratify=data[
                    target_column
                ]
            )
        )

    except ValueError:

        train_data, test_data = (
            train_test_split(
                data,
                test_size=test_size,
                random_state=42,
                stratify=None
            )
        )


    # ========================================================
    # ROOT ATTRIBUTE EVALUATION
    # ========================================================

    root_scores = evaluate_attributes(
        train_data,
        target_column,
        attributes
    )


    if root_scores.empty:

        st.error(
            "❌ No suitable attributes were found."
        )

        st.stop()


    root_scores = root_scores.sort_values(
        "Gain Ratio",
        ascending=False
    )


    # ========================================================
    # ATTRIBUTE TABLE
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Attribute Evaluation"
    )

    st.dataframe(
        root_scores,
        use_container_width=True
    )


    # ========================================================
    # ROOT
    # ========================================================

    root_attribute = root_scores.iloc[0][
        "Attribute"
    ]

    root_gain_ratio = root_scores.iloc[0][
        "Gain Ratio"
    ]

    st.success(
        f"🌳 Root Attribute: "
        f"**{root_attribute}**  |  "
        f"Highest Gain Ratio: "
        f"**{root_gain_ratio:.4f}**"
    )


    # ========================================================
    # BUILD TREE
    # ========================================================

    root = build_tree(
        train_data,
        target_column,
        attributes,
        depth=0,
        max_depth=max_depth
    )


    # ========================================================
    # TREE VISUALIZATION
    # ========================================================

    st.divider()

    st.subheader(
        "🌳 J48 Decision Tree"
    )


    # --------------------------------------------------------
    # Class colors
    # --------------------------------------------------------

    class_values = list(
        train_data[
            target_column
        ]
        .astype(str)
        .unique()
    )


    colors = [
        "#90EE90",
        "#FF9999",
        "#87CEFA",
        "#FFD580",
        "#D8B4FE",
        "#F9A8D4",
        "#A7F3D0",
        "#FDBA74"
    ]


    class_colors = {}

    for i, value in enumerate(
        class_values
    ):

        class_colors[value] = (
            colors[
                i % len(colors)
            ]
        )


    # --------------------------------------------------------
    # Escape Graphviz text
    # --------------------------------------------------------

    def escape_text(text):

        return (
            str(text)
            .replace(
                "&",
                "&amp;"
            )
            .replace(
                "<",
                "&lt;"
            )
            .replace(
                ">",
                "&gt;"
            )
            .replace(
                '"',
                "&quot;"
            )
        )


    # --------------------------------------------------------
    # Graph containers
    # --------------------------------------------------------

    graph_nodes = []

    graph_edges = []

    counter = [0]


    # --------------------------------------------------------
    # Create Graphviz tree
    # --------------------------------------------------------

    def create_graph(
        node,
        parent=None,
        branch=""
    ):

        current_id = (
            f"node{counter[0]}"
        )

        counter[0] += 1


        # Class distribution
        value_text = ", ".join(
            [
                f"{k}: {v}"
                for k, v
                in node.class_counts.items()
            ]
        )


        # ----------------------------------------------------
        # LEAF
        # ----------------------------------------------------

        if node.attribute is None:

            prediction = str(
                node.prediction
            )

            fill_color = (
                class_colors.get(
                    prediction,
                    "#E5E7EB"
                )
            )

            label = (
                f'<<TABLE '
                f'BORDER="0" '
                f'CELLBORDER="1" '
                f'CELLSPACING="0" '
                f'CELLPADDING="7">'

                f'<TR>'
                f'<TD '
                f'BGCOLOR="{fill_color}">'
                f'<B>Class = '
                f'{escape_text(prediction)}'
                f'</B>'
                f'</TD>'
                f'</TR>'

                f'<TR>'
                f'<TD>'
                f'Samples = '
                f'{node.samples}'
                f'</TD>'
                f'</TR>'

                f'<TR>'
                f'<TD>'
                f'Value = '
                f'{escape_text(value_text)}'
                f'</TD>'
                f'</TR>'

                f'</TABLE>>'
            )

            graph_nodes.append(
                (
                    current_id,
                    label,
                    fill_color
                )
            )


        # ----------------------------------------------------
        # DECISION NODE
        # ----------------------------------------------------

        else:

            label = (
                f'<<TABLE '
                f'BORDER="0" '
                f'CELLBORDER="1" '
                f'CELLSPACING="0" '
                f'CELLPADDING="7">'

                f'<TR>'
                f'<TD '
                f'BGCOLOR="#B7D7F0">'
                f'<B>'
                f'{escape_text(node.attribute)}'
                f'</B>'
                f'</TD>'
                f'</TR>'

                f'<TR>'
                f'<TD>'
                f'Gain Ratio = '
                f'{node.gain_ratio:.4f}'
                f'</TD>'
                f'</TR>'

                f'<TR>'
                f'<TD>'
                f'Samples = '
                f'{node.samples}'
                f'</TD>'
                f'</TR>'

                f'<TR>'
                f'<TD>'
                f'Value = '
                f'{escape_text(value_text)}'
                f'</TD>'
                f'</TR>'

                f'</TABLE>>'
            )

            graph_nodes.append(
                (
                    current_id,
                    label,
                    "#B7D7F0"
                )
            )


        # Parent connection
        if parent is not None:

            graph_edges.append(
                (
                    parent,
                    current_id,
                    branch
                )
            )


        # Children
        for branch_name, child in (
            node.children.items()
        ):

            create_graph(
                child,
                current_id,
                branch_name
            )


    create_graph(root)


    # --------------------------------------------------------
    # DOT GRAPH
    # --------------------------------------------------------

    dot = """
    digraph J48Tree {

        graph [
            rankdir=TB,
            bgcolor="white",
            nodesep=0.50,
            ranksep=0.70,
            margin=0.20
        ];

        node [
            shape=box,
            style="rounded,filled",
            fontname="Arial",
            fontsize=10,
            color="#555555"
        ];

        edge [
            color="#555555",
            fontname="Arial",
            fontsize=9
        ];
    """


    # Nodes
    for node_id, label, color in (
        graph_nodes
    ):

        dot += (
            f'{node_id} '
            f'[label={label}, '
            f'fillcolor="{color}"];'
        )


    # Edges
    for parent, child, branch in (
        graph_edges
    ):

        dot += (
            f'{parent} -> {child} '
            f'[label="{escape_text(branch)}"];'
        )


    dot += "}"


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    st.graphviz_chart(
        dot,
        use_container_width=True
    )


    # ========================================================
    # PREDICTION
    # ========================================================

    X_test = test_data.drop(
        columns=[target_column]
    )

    y_test = test_data[
        target_column
    ]


    y_pred = predict(
        root,
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
    # OVERALL PERFORMANCE
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
        len(test_data)
    )


    # ========================================================
    # ONE CONFUSION MATRIX
    # ========================================================

    st.divider()

    st.subheader(
        "🔲 Confusion Matrix"
    )


    labels = sorted(
        data[
            target_column
        ]
        .astype(str)
        .unique()
    )


    y_test_str = (
        y_test.astype(str)
    )

    y_pred_str = (
        pd.Series(y_pred)
        .astype(str)
    )


    cm = confusion_matrix(
        y_test_str,
        y_pred_str,
        labels=labels
    )


    cm_df = pd.DataFrame(
        cm,
        index=[
            "Actual " + label
            for label in labels
        ],
        columns=[
            "Predicted " + label
            for label in labels
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
        y_test_str,
        y_pred_str,
        labels=labels,
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

    import matplotlib.pyplot as plt

    # ========================================================
    # BINARY DATASET
    # ========================================================

    if len(labels) == 2:

        positive_class = labels[1]

        y_actual = (
            y_test_str == positive_class
        ).astype(int)

        y_prediction = (
            y_pred_str == positive_class
        ).astype(int)

        fpr, tpr, _ = roc_curve(
            y_actual,
            y_prediction
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
            linestyle="--"
        )

        ax.set_xlabel(
            "False Positive Rate"
        )

        ax.set_ylabel(
            "True Positive Rate"
        )

        ax.set_title(
            "ROC Curve - J48"
        )

        ax.legend(
            loc="lower right"
        )

        st.pyplot(fig)

        plt.close(fig)

        st.success(
            f"ROC AUC = {roc_auc:.4f}"
        )

    # ========================================================
    # MULTICLASS - WEKA STYLE
    # ========================================================

    else:

        roc_class = st.selectbox(
            "Select Class for ROC Curve",
            labels,
            key="j48_roc_class"
        )

        st.caption(
            f"ROC Curve: {roc_class} vs Rest"
        )

        y_actual = (
            y_test_str == roc_class
        ).astype(int)

        y_prediction = (
            y_pred_str == roc_class
        ).astype(int)

        try:

            fpr, tpr, _ = roc_curve(
                y_actual,
                y_prediction
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
                    f"{roc_class} vs Rest "
                    f"(AUC = {roc_auc:.3f})"
                )
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
                "ROC Curve - J48"
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
                f"ROC AUC ({roc_class}) = "
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

        if node.attribute is None:

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
                + str(node.prediction)
            )


            return rules


        # ----------------------------------------------------
        # CHILDREN
        # ----------------------------------------------------

        for branch, child in (
            node.children.items()
        ):

            new_conditions = (
                conditions
                + [
                    f"{node.attribute} = {branch}"
                ]
            )


            rules.extend(
                generate_rules(
                    child,
                    new_conditions
                )
            )


        return rules


    rules = generate_rules(
        root
    )


    # --------------------------------------------------------
    # DISPLAY RULES
    # --------------------------------------------------------

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
        "✅ Complete J48 analysis finished."
    )