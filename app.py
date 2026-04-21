import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Spending Dashboard", layout="wide")

# Load data
df = pd.read_csv("student_spending_cleaned.csv")

# If these columns are missing, create them
spending_cols = [
    "housing", "food", "transportation", "books_supplies",
    "entertainment", "personal_care", "technology",
    "health_wellness", "miscellaneous"
]

if "total_spending" not in df.columns:
    df["total_spending"] = df[spending_cols].sum(axis=1)

if "spending_status" not in df.columns:
    df["spending_status"] = df.apply(
        lambda row: "Overspending" if row["total_spending"] > row["monthly_income"]
        else "Underspending",
        axis=1
    )

# Title
st.title("📊 Student Spending Dashboard")
st.markdown("### Bank Perspective: Understanding where college students spend the most to design better student deals")

# Sidebar filters
st.sidebar.header("Filters")

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["gender"].dropna().unique().tolist())
)

selected_year = st.sidebar.selectbox(
    "Select Year in School",
    ["All"] + sorted(df["year_in_school"].dropna().unique().tolist())
)

selected_payment = st.sidebar.selectbox(
    "Select Payment Method",
    ["All"] + sorted(df["preferred_payment_method"].dropna().unique().tolist())
)

# Apply filters
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year_in_school"] == selected_year]

if selected_payment != "All":
    filtered_df = filtered_df[filtered_df["preferred_payment_method"] == selected_payment]

# Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

avg_spending = filtered_df["total_spending"].mean()
avg_income = filtered_df["monthly_income"].mean()
overspending_pct = (
    (filtered_df["spending_status"] == "Overspending").mean() * 100
)

col1.metric("Average Total Spending", f"${avg_spending:,.2f}")
col2.metric("Average Monthly Income", f"${avg_income:,.2f}")
col3.metric("Overspending Rate", f"{overspending_pct:.1f}%")

# Average spending by category
st.subheader("Average Spending by Category")

category_avg = filtered_df[spending_cols].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(10, 5))
category_avg.plot(kind="bar", ax=ax1)
ax1.set_title("Average Spending by Category")
ax1.set_xlabel("Category")
ax1.set_ylabel("Average Spending")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# Overspending vs underspending
st.subheader("Student Spending Behavior")

status_pct = filtered_df["spending_status"].value_counts(normalize=True) * 100

fig2, ax2 = plt.subplots(figsize=(6, 4))
status_pct.plot(kind="bar", ax=ax2)
ax2.set_title("Overspending vs Underspending")
ax2.set_xlabel("Spending Status")
ax2.set_ylabel("Percentage (%)")
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig2)

# Distribution of total spending
st.subheader("Distribution of Total Spending")

fig3, ax3 = plt.subplots(figsize=(8, 5))
ax3.hist(filtered_df["total_spending"], bins=30)
ax3.set_title("Distribution of Total Student Spending")
ax3.set_xlabel("Total Spending")
ax3.set_ylabel("Number of Students")
plt.tight_layout()
st.pyplot(fig3)

# Group comparisons
st.subheader("Group Comparisons")

col4, col5 = st.columns(2)

with col4:
    gender_avg = filtered_df.groupby("gender")["total_spending"].mean().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    gender_avg.plot(kind="bar", ax=ax4)
    ax4.set_title("Average Spending by Gender")
    ax4.set_xlabel("Gender")
    ax4.set_ylabel("Average Total Spending")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig4)

with col5:
    year_avg = filtered_df.groupby("year_in_school")["total_spending"].mean().sort_values(ascending=False)
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    year_avg.plot(kind="bar", ax=ax5)
    ax5.set_title("Average Spending by Year")
    ax5.set_xlabel("Year in School")
    ax5.set_ylabel("Average Total Spending")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig5)

payment_avg = filtered_df.groupby("preferred_payment_method")["total_spending"].mean().sort_values(ascending=False)
fig6, ax6 = plt.subplots(figsize=(8, 4))
payment_avg.plot(kind="bar", ax=ax6)
ax6.set_title("Average Spending by Payment Method")
ax6.set_xlabel("Preferred Payment Method")
ax6.set_ylabel("Average Total Spending")
plt.xticks(rotation=20)
plt.tight_layout()
st.pyplot(fig6)

# Bank recommendations
st.subheader("Recommended Student Deals for Banks")

top_category = category_avg.index[0]

st.markdown(f"""
Based on the filtered data, **{top_category.replace('_', ' ').title()}** is the highest spending category.

### Suggested Bank Strategies
- Offer cashback or rewards in the **top spending category**
- Provide grocery/food discounts for students
- Add budgeting alerts for overspending customers
- Promote student-friendly debit/credit card deals
- Create personalized offers based on spending behavior
""")