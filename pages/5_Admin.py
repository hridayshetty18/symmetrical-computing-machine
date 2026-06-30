import streamlit as st
import pandas as pd
from data.preprocessing import preprocess_pipeline

st.set_page_config(page_title="Admin Panel", page_icon="🔒", layout="wide")
st.title("🔒 Admin Dashboard")

# Simple mock login
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

if not st.session_state['admin_logged_in']:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state['admin_logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.success("Logged in as Administrator")
    if st.button("Logout"):
        st.session_state['admin_logged_in'] = False
        st.rerun()
        
    st.divider()
    
    st.subheader("Audit Logs & Batch Export")
    
    from data.data_loader import get_cached_data
        
    try:
        df = get_cached_data()
        
        # Filtering for export
        status_filter = st.selectbox("Filter by Status", ["All", "Suspected Fraud", "Clean"])
        if status_filter != "All":
            export_df = df[df['Status'] == status_filter]
        else:
            export_df = df
            
        st.dataframe(export_df.head(50), use_container_width=True)
        
        csv = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name='fraud_audit_log.csv',
            mime='text/csv',
        )
        
    except Exception as e:
        st.error(f"Error: {e}")
