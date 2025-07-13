import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------
# Utility Functions
# -------------------

def get_default_categories():
    return {
        "Housing": 0,
        "Utilities": 0,
        "Groceries": 0,
        "Transportation": 0,
        "Healthcare": 0,
        "Insurance": 0,
        "Debt Payments": 0,
        "Entertainment": 0,
        "Savings": 0,
        "Education": 0,
    }

def calculate_50_30_20(income, expenses):
    limits = {
        "Needs": income * 0.50,
        "Wants": income * 0.30,
        "Savings": income * 0.20,
    }

    categorized = {"Needs": 0, "Wants": 0, "Savings": 0}
    for category, amount in expenses.items():
        if category in ["Housing", "Utilities", "Groceries", "Transportation", "Healthcare", "Insurance", "Debt Payments"]:
            categorized["Needs"] += amount
        elif category in ["Entertainment"]:
            categorized["Wants"] += amount
        elif category in ["Savings", "Education"]:
            categorized["Savings"] += amount
        else:
            categorized["Wants"] += amount  # Default fallback

    return categorized, limits

def plot_expense_breakdown(categorized, limits):
    categories = list(categorized.keys())
    actuals = [categorized[k] for k in categories]
    colors = []

for k in categories:
    limit = limits[k]
    if limit == 0:
        colors.append("grey")  # No budget set, neutral color
        continue
    ratio = categorized[k] / limit
    if ratio <= 1.0:
        colors.append("green")
    elif ratio <= 1.2:
        colors.append("yellow")
    else:
        colors.append("red")

    fig, ax = plt.subplots()
    ax.bar(categories, actuals, color=colors)
    ax.set_title("50/30/20 Rule Analysis")
    ax.set_ylabel("Amount ($)")
    st.pyplot(fig)

def dime_calculator(debt, income, years, mortgage, edu_cost, num_children):
    return debt + (income * years) + mortgage + (edu_cost * num_children)

# -------------------
# Streamlit App
# -------------------

st.set_page_config(page_title="Personal Budget Analyzer", layout="wide")
st.title("📊 Personal Budget & Insurance Planner")

# Monthly Income
monthly_income = st.number_input("Enter your **Monthly Income ($)**", min_value=0.0, step=100.0)

# Family Info
st.subheader("👨‍👩‍👧‍👦 Family Members")
adults = st.number_input("Number of Adults", min_value=1, step=1, value=1)
children = st.number_input("Number of Children", min_value=0, step=1, value=0)

# Expense Input
st.subheader("💸 Monthly Expenses")
expenses = get_default_categories()

# Predefined Categories
for category in expenses.keys():
    expenses[category] = st.number_input(f"{category}", min_value=0.0, step=50.0)

# Custom Categories
st.markdown("**Add Custom Expense Categories**")
custom_expenses = {}
with st.expander("➕ Add Custom Categories"):
    num_custom = st.number_input("Number of Custom Categories", min_value=0, max_value=10, step=1)
    for i in range(num_custom):
        cat = st.text_input(f"Custom Category {i+1} Name")
        val = st.number_input(f"{cat} Amount", min_value=0.0, step=50.0, key=f"custom_{i}")
        if cat:
            custom_expenses[cat] = val

expenses.update(custom_expenses)

# -----------------------
# 50/30/20 Rule Analysis
# -----------------------
st.subheader("📐 50/30/20 Budget Rule Analysis")
categorized, limits = calculate_50_30_20(monthly_income, expenses)
plot_expense_breakdown(categorized, limits)

# Summary Recommendations
st.markdown("### 💡 Spending Suggestions")
for category, amount in categorized.items():
    ratio = amount / limits[category]
    if ratio > 1.2:
        st.error(f"⚠️ You are overspending in **{category}**. Consider reducing your spending.")
    elif ratio > 1.0:
        st.warning(f"🔶 You are slightly over the limit in **{category}**. Caution is advised.")
    else:
        st.success(f"✅ Good job staying within the **{category}** budget.")

# Suggested Categories for Family
st.subheader("📌 Suggested Categories Based on Family Size")
if children > 0:
    st.info("🧒 Consider allocating budget for: Childcare, School Supplies, Pediatric Care, and Activities")
if adults > 1:
    st.info("👫 Consider budget sharing on: Joint Insurance, Dual Transportation, Shared Groceries")

# -----------------------
# DIME Life Insurance
# -----------------------
st.subheader("🛡️ DIME Life Insurance Calculator")

with st.expander("ℹ️ Learn about the DIME Method"):
    st.markdown("""
    **DIME** stands for:
    - **D**ebt: All outstanding debts
    - **I**ncome: Annual income × number of years to provide
    - **M**ortgage: Remaining balance
    - **E**ducation: Future education costs per child
    """)

col1, col2 = st.columns(2)
with col1:
    debt = st.number_input("Total Outstanding Debt ($)", min_value=0.0, step=100.0)
    income = st.number_input("Annual Income ($)", min_value=0.0, step=1000.0)
    income_years = st.number_input("Years to Support Family", min_value=1, step=1, value=10)
with col2:
    mortgage = st.number_input("Remaining Mortgage ($)", min_value=0.0, step=1000.0)
    edu_cost = st.number_input("Estimated Education Cost per Child ($)", min_value=0.0, step=1000.0)

insurance_needed = dime_calculator(debt, income, income_years, mortgage, edu_cost, children)
st.success(f"✅ Recommended Life Insurance Coverage: **${insurance_needed:,.2f}**")
