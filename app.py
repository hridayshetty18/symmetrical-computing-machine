import streamlit as st

st.set_page_config(
    page_title="AI Health Fraud Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark mode aesthetic
st.markdown("""
<style>
    /* Global Styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e2e8f0;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }
    
    /* Success / Error colors override for aesthetics */
    .stAlert {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI-Powered Health Insurance Fraud Detection Platform")
st.write("Welcome to the next-generation fraud detection system.")
st.write("Please select a module from the sidebar to begin.")

# Quick stats overview on main page
col1, col2, col3 = st.columns(3)
col1.metric("Today's Claims Assessed", "142", "12")
col2.metric("High Risk Claims Detected", "18", "4", delta_color="inverse")
col3.metric("System Accuracy (F1-Score)", "96.2%", "0.5%")

st.info("💡 **Tip:** Use the Claim Predictor to manually assess a claim using the Random Forest model and SHAP explainability.")
