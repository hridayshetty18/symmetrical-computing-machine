import streamlit as st
import pandas as pd
from data.data_loader import get_cached_data
from utils.network import plot_fraud_network

st.set_page_config(page_title="Hospital Lookup", page_icon="🏥", layout="wide")
st.title("🏥 Hospital Profile & Lookup")

try:
    df = get_cached_data()
    
    hospitals = sorted(df['Hospital'].unique())
    selected_hospital = st.selectbox("Search for a Hospital:", ["-- Select --"] + list(hospitals))
    
    if selected_hospital != "-- Select --":
        h_df = df[df['Hospital'] == selected_hospital]
        
        st.subheader(f"Profile: {selected_hospital}")
        
        col1, col2, col3, col4 = st.columns(4)
        total_claims = len(h_df)
        avg_claim = h_df['Claim_Amount'].mean()
        fraud_cases = len(h_df[h_df['Status'] == 'Suspected Fraud'])
        fraud_rate = (fraud_cases / total_claims) * 100 if total_claims > 0 else 0
        
        col1.metric("Total Claims", total_claims)
        col2.metric("Average Claim", f"₹{avg_claim:,.2f}")
        col3.metric("Fraud Cases", fraud_cases, f"{fraud_rate:.1f}%")
        
        risk_score = min(100, int(fraud_rate * 2)) # Simple derived risk score for hospital
        if risk_score > 50:
            col4.metric("Provider Risk Score", risk_score, "🔴 High", delta_color="inverse")
        else:
            col4.metric("Provider Risk Score", risk_score, "🟢 Normal")
            
        st.divider()
        
        col_net, col_table = st.columns([2, 1])
        
        with col_net:
            st.write("### Patient-Provider Network Graph")
            st.caption("Visualizing connections to detect fraud rings. Red nodes = Patients with fraud history.")
            fig = plot_fraud_network(df, selected_hospital)
            st.plotly_chart(fig, use_container_width=True)
            
        with col_table:
            st.write("### Recent Remarks")
            remarks_df = h_df[['Date', 'Remarks', 'Status']].sort_values('Date', ascending=False).head(10)
            st.dataframe(remarks_df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
