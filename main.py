import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Simple Finance App", layout="wide", page_icon="💰")
st.title("📄 Upload Your CIBC Bank Statement (CSV)")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# ---------- CATEGORY SETUP ----------
if "categories" not in st.session_state:
    if os.path.exists("categories.json"):
        with open("categories.json", "r") as f:
            st.session_state.categories = json.load(f)
    else:
        st.session_state.categories = {"Uncategorized": []}

# Track edited DataFrame
edited_expenses_df = None

# ---------- FILE PROCESSING ----------
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip() for col in df.columns]

        # Clean Debit and Credit columns
        df["Debit"] = df["Debit"].astype(str).str.replace("[$,]", "", regex=True).replace("nan", "")
        df["Credit"] = df["Credit"].astype(str).str.replace("[$,]", "", regex=True).replace("nan", "")

        # Create unified Amount column
        def get_amount(row):
            if row["Debit"]:
                return float(row["Debit"])
            elif row["Credit"]:
                return float(row["Credit"])
            else:
                return 0.0

        df["Amount"] = df.apply(get_amount, axis=1)

        # Add DebitCredit column
        def label_type(row):
            if row["Debit"]:
                return "Debit"
            elif row["Credit"]:
                return "Credit"
            else:
                return "Unknown"

        df["DebitCredit"] = df.apply(label_type, axis=1)

        # Split into Debits & Credits
        debits_df = df[df["DebitCredit"] == "Debit"].copy()
        credits_df = df[df["DebitCredit"] == "Credit"].copy()

        # Ensure 'Category' column exists
        if "Category" not in debits_df.columns:
            debits_df["Category"] = "Uncategorized"

        # 🔥 Auto-categorize based on keyword matches
        for idx, row in debits_df.iterrows():
            detail = row["Details"].strip().lower()
            for cat, keywords in st.session_state.categories.items():
                for kw in keywords:
                    if kw.lower() in detail:
                        debits_df.at[idx, "Category"] = cat
                        break

        # ---------- DISPLAY TABS ----------
        tab1, tab2, tab3 = st.tabs(["💸 Expenses", "💰 Payments", "📊 Summary"])

        with tab1:
            st.subheader("Your Expenses")

            edited_expenses_df = st.data_editor(
                debits_df[["Date", "Details", "Amount", "Category"]],
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Category": st.column_config.SelectboxColumn(
                        "Category",
                        options=list(st.session_state.categories.keys()),
                    )
                }
            )

        with tab2:
            st.subheader("Your Payments")
            st.dataframe(credits_df[["Date", "Details", "Amount"]])

        with tab3:
            st.subheader("📊 Summary by Category")

            summary_df = (
                debits_df.groupby("Category")["Amount"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )

            st.dataframe(summary_df, use_container_width=True)

            # Plot pie chart
            import plotly.express as px
            fig = px.pie(
                summary_df,
                names="Category",
                values="Amount",
                title="Expenses by Category",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")

# ---------- CATEGORY MANAGEMENT ----------
st.header("🗂️ Manage Your Categories")

new_category = st.text_input("New Category Name")
if st.button("➕ Add Category") and new_category:
    if new_category not in st.session_state.categories:
        st.session_state.categories[new_category] = []
        st.success(f"Category '{new_category}' added!")
    else:
        st.warning("That category already exists.")

# ---------- SAVE ASSIGNED CATEGORIES ----------
if uploaded_file is not None and edited_expenses_df is not None:
    save_button = st.button("💾 Apply & Save Category Changes")

    if save_button:
        try:
            for _, row in edited_expenses_df.iterrows():
                category = row.get("Category", "").strip()
                keyword = row.get("Details", "").strip().lower()

                if not category or not keyword:
                    continue

                if category not in st.session_state.categories:
                    st.session_state.categories[category] = []

                if keyword not in [kw.lower() for kw in st.session_state.categories[category]]:
                    st.session_state.categories[category].append(keyword)

            with open("categories.json", "w") as f:
                json.dump(st.session_state.categories, f, indent=2)

            st.success("✅ Categories saved to categories.json!")

        except Exception as e:
            st.error(f"❌ Failed to save categories: {e}")