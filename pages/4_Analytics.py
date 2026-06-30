import streamlit as st
import pandas as pd
from data.data_loader import get_cached_data
from utils.charts import plot_claims_by_state, plot_claim_amount_histogram

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.title("📈 Deep Dive Analytics")

try:
    df = get_cached_data()
    
    tab1, tab2 = st.tabs(["Geographical Analysis", "Distributions"])
    
    with tab1:
        st.subheader("Claims by State")
        st.plotly_chart(plot_claims_by_state(df), use_container_width=True)
        
    with tab2:
        st.subheader("Claim Amount Histogram")
        st.plotly_chart(plot_claim_amount_histogram(df), use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
