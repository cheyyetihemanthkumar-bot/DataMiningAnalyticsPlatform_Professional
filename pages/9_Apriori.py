import streamlit as st
import pandas as pd
import numpy as np
from theme import apply_theme
from itertools import combinations


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Apriori",
    page_icon="🛒",
    layout="wide"
)
apply_theme()

st.title("🛒 Apriori Association Rule Mining")
st.caption(
    "Discover frequent itemsets and association rules"
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
# SELECT TRANSACTION COLUMNS
# ============================================================

st.subheader("🎯 Select Transaction Columns")

selected_columns = st.multiselect(
    "Select columns to use for association analysis",
    df.columns.tolist(),
    default=df.columns.tolist(),
    key="apriori_columns"
)


if len(selected_columns) == 0:

    st.warning(
        "⚠️ Please select at least one column."
    )

    st.stop()


# ============================================================
# SETTINGS
# ============================================================

st.subheader("⚙️ Apriori Settings")

col1, col2, col3 = st.columns(3)


with col1:

    min_support = st.slider(
        "Minimum Support",
        min_value=0.05,
        max_value=1.0,
        value=0.20,
        step=0.05,
        key="apriori_support"
    )


with col2:

    min_confidence = st.slider(
        "Minimum Confidence",
        min_value=0.05,
        max_value=1.0,
        value=0.50,
        step=0.05,
        key="apriori_confidence"
    )


with col3:

    min_lift = st.slider(
        "Minimum Lift",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        key="apriori_lift"
    )


# ============================================================
# RUN APRIORI
# ============================================================

if st.button(
    "🚀 Run Apriori",
    type="primary",
    key="run_apriori"
):

    # ========================================================
    # PREPARE DATA
    # ========================================================

    data = df[
        selected_columns
    ].copy()


    # ========================================================
    # CONVERT EACH RECORD INTO A TRANSACTION
    # ========================================================

    transactions = []

    for _, row in data.iterrows():

        transaction = []

        for column in selected_columns:

            value = row[column]

            if pd.isna(value):
                continue

            item = (
                str(column)
                + "="
                + str(value)
            )

            transaction.append(item)

        if len(transaction) > 0:

            transactions.append(
                set(transaction)
            )


    # ========================================================
    # CHECK TRANSACTIONS
    # ========================================================

    if len(transactions) == 0:

        st.error(
            "❌ No valid transactions were found."
        )

        st.stop()


    total_transactions = len(
        transactions
    )


    # ========================================================
    # SUPPORT FUNCTION
    # ========================================================

    def calculate_support(
        itemset
    ):

        count = 0

        for transaction in transactions:

            if itemset.issubset(
                transaction
            ):

                count += 1

        return (
            count
            / total_transactions
        )


    # ========================================================
    # FREQUENT 1-ITEMSETS
    # ========================================================

    all_items = set()

    for transaction in transactions:

        all_items.update(
            transaction
        )


    frequent_itemsets = {}


    current_itemsets = []


    for item in sorted(
        all_items
    ):

        itemset = frozenset(
            [item]
        )

        support = calculate_support(
            itemset
        )

        if support >= min_support:

            frequent_itemsets[
                itemset
            ] = support

            current_itemsets.append(
                itemset
            )


    # ========================================================
    # GENERATE LARGER ITEMSETS
    # ========================================================

    k = 2


    while len(current_itemsets) > 0:

        candidates = set()


        for i in range(
            len(current_itemsets)
        ):

            for j in range(
                i + 1,
                len(current_itemsets)
            ):

                union_set = (
                    current_itemsets[i]
                    | current_itemsets[j]
                )


                if len(union_set) == k:

                    candidates.add(
                        union_set
                    )


        if len(candidates) == 0:
            break


        next_itemsets = []


        for candidate in candidates:

            support = calculate_support(
                candidate
            )


            if support >= min_support:

                frequent_itemsets[
                    candidate
                ] = support

                next_itemsets.append(
                    candidate
                )


        current_itemsets = (
            next_itemsets
        )

        k += 1


    # ========================================================
    # FREQUENT ITEMSETS DISPLAY
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Frequent Itemsets"
    )


    if len(frequent_itemsets) == 0:

        st.warning(
            "⚠️ No frequent itemsets found. "
            "Try lowering Minimum Support."
        )

        st.stop()


    itemset_rows = []


    for itemset, support in (
        frequent_itemsets.items()
    ):

        itemset_rows.append({
            "Itemset": ", ".join(
                sorted(itemset)
            ),
            "Number of Items":
                len(itemset),
            "Support":
                round(support, 4),
            "Support %":
                f"{support * 100:.2f}%"
        })


    itemset_df = pd.DataFrame(
        itemset_rows
    )


    itemset_df = itemset_df.sort_values(
        "Support",
        ascending=False
    )


    st.dataframe(
        itemset_df,
        use_container_width=True
    )


    # ========================================================
    # ASSOCIATION RULES
    # ========================================================

    st.divider()

    st.subheader(
        "🔗 Association Rules"
    )


    rules = []


    for itemset, itemset_support in (
        frequent_itemsets.items()
    ):

        if len(itemset) < 2:
            continue


        items = list(itemset)


        for r in range(
            1,
            len(items)
        ):

            for antecedent_tuple in combinations(
                items,
                r
            ):

                antecedent = frozenset(
                    antecedent_tuple
                )


                consequent = (
                    itemset
                    - antecedent
                )


                if len(consequent) == 0:
                    continue


                antecedent_support = (
                    frequent_itemsets.get(
                        antecedent
                    )
                )


                if antecedent_support is None:

                    antecedent_support = (
                        calculate_support(
                            antecedent
                        )
                    )


                consequent_support = (
                    frequent_itemsets.get(
                        consequent
                    )
                )


                if consequent_support is None:

                    consequent_support = (
                        calculate_support(
                            consequent
                        )
                    )


                if antecedent_support == 0:

                    continue


                confidence = (
                    itemset_support
                    / antecedent_support
                )


                if consequent_support == 0:

                    continue


                lift = (
                    confidence
                    / consequent_support
                )


                if (
                    confidence
                    >= min_confidence
                    and
                    lift
                    >= min_lift
                ):

                    rules.append({

                        "IF":
                            ", ".join(
                                sorted(
                                    antecedent
                                )
                            ),

                        "THEN":
                            ", ".join(
                                sorted(
                                    consequent
                                )
                            ),

                        "Support":
                            round(
                                itemset_support,
                                4
                            ),

                        "Confidence":
                            round(
                                confidence,
                                4
                            ),

                        "Lift":
                            round(
                                lift,
                                4
                            )
                    })


    # ========================================================
    # RULE RESULTS
    # ========================================================

    if len(rules) > 0:

        rules_df = pd.DataFrame(
            rules
        )


        rules_df = rules_df.sort_values(
            "Lift",
            ascending=False
        )


        st.dataframe(
            rules_df,
            use_container_width=True
        )


        # ====================================================
        # BEST RULE
        # ====================================================

        best_rule = rules_df.iloc[0]


        st.success(
            "⭐ Best Association Rule: "
            + "IF "
            + str(best_rule["IF"])
            + " THEN "
            + str(best_rule["THEN"])
            + " | Confidence = "
            + str(
                best_rule["Confidence"]
            )
            + " | Lift = "
            + str(
                best_rule["Lift"]
            )
        )


    else:

        st.warning(
            "⚠️ No association rules satisfy "
            "the selected Confidence and Lift."
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Apriori Summary"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Transactions",
        total_transactions
    )


    c2.metric(
        "Frequent Itemsets",
        len(frequent_itemsets)
    )


    c3.metric(
        "Association Rules",
        len(rules)
    )


    # ========================================================
    # DOWNLOAD ITEMSETS
    # ========================================================

    st.divider()

    st.subheader(
        "⬇️ Download Results"
    )


    itemset_csv = (
        itemset_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="⬇ Download Frequent Itemsets",
        data=itemset_csv,
        file_name="frequent_itemsets.csv",
        mime="text/csv",
        key="download_itemsets"
    )


    # ========================================================
    # DOWNLOAD RULES
    # ========================================================

    if len(rules) > 0:

        rules_csv = (
            rules_df
            .to_csv(index=False)
            .encode("utf-8")
        )


        st.download_button(
            label="⬇ Download Association Rules",
            data=rules_csv,
            file_name="association_rules.csv",
            mime="text/csv",
            key="download_rules"
        )


    # ========================================================
    # COMPLETE
    # ========================================================

    st.divider()

    st.success(
        "✅ Apriori analysis completed successfully."
    )