import streamlit as st
from data.preprocessing import preprocess_pipeline

@st.cache_data(show_spinner=False)
def get_cached_data():
    """
    Centralized data loader to ensure Streamlit only loads and preprocesses 
    the dataset once across all pages, drastically improving performance.
    """
    return preprocess_pipeline("HL Main.csv")
