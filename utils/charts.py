import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.tree import plot_tree


def plot_confusion_matrix(cm, class_names):
    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
    )

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")

    return fig


def plot_decision_tree(model, feature_names, class_names):
    fig, ax = plt.subplots(figsize=(18, 10))

    plot_tree(
        model,
        feature_names=feature_names,
        class_names=[str(i) for i in class_names],
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax,
    )

    return fig


def plot_feature_importance(model, feature_names):
    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        importance["Feature"],
        importance["Importance"]
    )

    ax.set_title("Feature Importance")
    ax.invert_yaxis()

    return fig, importance


def plot_roc_curve(fpr, tpr, auc_score):
    fig, ax = plt.subplots(figsize=(6, 5))

    ax.plot(
        fpr,
        tpr,
        label=f"AUC = {auc_score:.3f}"
    )

    ax.plot([0, 1], [0, 1], "--")

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()

    return fig