import streamlit as st
import pandas as pd
from data.data_loader import get_cached_data
from utils.charts import plot_monthly_trend, plot_fraud_distribution

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Platform Dashboard")

try:
    df = get_cached_data()
    
    col1, col2, col3, col4 = st.columns(4)
    total_claims = len(df)
    fraud_claims = len(df[df['Status'] == 'Suspected Fraud'])
    fraud_rate = (fraud_claims / total_claims) * 100
    total_amount = df['Claim_Amount'].sum()
    
    col1.metric("Total Claims", f"{total_claims:,}")
    col2.metric("Suspected Fraud", f"{fraud_claims:,}", f"{fraud_rate:.1f}%")
    col3.metric("Total Amount Claimed", f"₹{total_amount:,.2f}")
    
    recovered = df[df['Status'] == 'Suspected Fraud']['Claim_Amount'].sum() - df[df['Status'] == 'Suspected Fraud']['Settled_Amount'].sum()
    col4.metric("Potential Fraud Savings", f"₹{recovered:,.2f}")
    
    st.divider()
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.plotly_chart(plot_monthly_trend(df), use_container_width=True)
    with row1_col2:
        st.plotly_chart(plot_fraud_distribution(df), use_container_width=True)
        
    st.subheader("Recent High-Risk Claims")
    high_risk = df[df['Status'] == 'Suspected Fraud'].sort_values('Date', ascending=False).head(5)
    st.dataframe(high_risk[['Claim_ID', 'Date', 'Hospital', 'Claim_Amount', 'Settled_Amount', 'Remarks']], use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
