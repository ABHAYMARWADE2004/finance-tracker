import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Page Settings ----
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰", layout="wide")

# ---- Load Data ----
df = pd.read_csv('transactions.csv')
df['date'] = pd.to_datetime(df['date'])

# ---- Sidebar Filters ----
st.sidebar.title("🔍 Filters")
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

category_options = sorted(df['category'].unique())
selected_categories = st.sidebar.multiselect("Categories", category_options, default=category_options)

mask = (
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['category'].isin(selected_categories))
)
df = df[mask]

# ---- Header ----
st.title("💰 Personal Finance Tracker")
st.caption("A simple dashboard to track income, expenses and spending patterns")
st.divider()

# ---- KPI Metrics ----
income = df[df['type'] == 'Credit']['amount'].sum()
expense = df[df['type'] == 'Debit']['amount'].sum()
savings = income - expense
savings_rate = (savings / income * 100) if income > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Income", f"₹{income:,.0f}")
col2.metric("Total Expense", f"₹{expense:,.0f}")
col3.metric("Net Savings", f"₹{savings:,.0f}")
col4.metric("Savings Rate", f"{savings_rate:.1f}%")

st.divider()

# ---- Charts Row ----
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Expense by Category")
    expense_df = df[df['type'] == 'Debit']
    fig1 = px.pie(expense_df, values='amount', names='category', hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.subheader("📈 Monthly Income vs Expense")
    df['month'] = df['date'].dt.to_period('M').astype(str)
    monthly = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    fig2 = px.bar(monthly, x='month', y='amount', color='type', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

# ---- Trend Line ----
st.subheader("📉 Daily Spending Trend")
daily_expense = df[df['type'] == 'Debit'].groupby('date')['amount'].sum().reset_index()
fig3 = px.line(daily_expense, x='date', y='amount', markers=True)
st.plotly_chart(fig3, use_container_width=True)

# ---- Raw Data ----
with st.expander("📄 View Raw Transaction Data"):
    st.dataframe(df.drop(columns=['month']), use_container_width=True)

st.caption("Built with Python, Pandas, Plotly and Streamlit")