import streamlit as st
import pandas as pd
from model.predict import RiskScoreGenerator
from utils.explainability import generate_shap_explanation
from utils.ocr import extract_text_from_image, verify_claim_with_ocr
from utils.reports import generate_pdf_report

st.set_page_config(page_title="Claim Predictor", page_icon="🤖", layout="wide")
st.title("🤖 AI Claim Predictor & Verification")

@st.cache_resource
def load_predictor():
    return RiskScoreGenerator()

predictor = load_predictor()

col_form, col_results = st.columns([1, 1])

with col_form:
    st.subheader("Enter Claim Details")
    with st.form("claim_form"):
        patient_id = st.text_input("Patient ID", value="PAT1234")
        hospital = st.text_input("Hospital Name", value="Hospital A")
        claim_amount = st.number_input("Claim Amount (₹)", value=50000.0)
        settled_amount = st.number_input("Settled Amount (₹)", value=15000.0)
        remarks = st.text_area("Investigation Remarks", value="Duplicate Bill Detected")
        
        st.write("### Document OCR (Optional)")
        uploaded_file = st.file_uploader("Upload Bill / Discharge Summary (Image)", type=['png', 'jpg', 'jpeg'])
        
        submit_btn = st.form_submit_button("Run AI Assessment")

with col_results:
    if submit_btn:
        with st.spinner("Analyzing claim using Random Forest..."):
            claim_data = {
                "Patient_ID": patient_id,
                "Hospital": hospital,
                "Claim_Amount": claim_amount,
                "Settled_Amount": settled_amount,
                "Remarks": remarks
            }
            
            result = predictor.predict(claim_data)
            
            if "error" in result:
                st.error(result["error"])
            else:
                score = result["risk_score"]
                level = result["risk_level"]
                
                st.subheader("Fraud Risk Assessment")
                st.markdown(f"### Risk Score: **{score} / 100**")
                st.markdown(f"### Risk Level: **{level}**")
                
                # SHAP Explainability
                st.write("### Why did the model make this decision?")
                try:
                    reasons, _ = generate_shap_explanation(
                        predictor.model, 
                        result["input_features"], 
                        predictor.features_list
                    )
                    for r in reasons:
                        st.write(f"- {r}")
                except Exception as e:
                    st.warning(f"Could not generate SHAP explanation: {e}")
                    reasons = ["Model reasoning not available."]
                    
                # OCR Verification
                if uploaded_file is not None:
                    st.divider()
                    st.write("### OCR Document Verification")
                    with st.spinner("Extracting text via EasyOCR..."):
                        bytes_data = uploaded_file.getvalue()
                        text = extract_text_from_image(bytes_data)
                        ocr_result = verify_claim_with_ocr(text, claim_amount, patient_id)
                        
                        if ocr_result["amount_match"]:
                            st.success(f"✅ Claim Amount (₹{claim_amount}) found in document.")
                        else:
                            st.error(f"❌ Claim Amount (₹{claim_amount}) NOT found in document. Possible forgery.")
                            reasons.append("Claim amount missing from submitted documents.")
                            
                # PDF Generation
                st.divider()
                st.write("### Actions")
                pdf_bytes = generate_pdf_report(claim_data, score, reasons)
                st.download_button(
                    label="📄 Download Investigation Report",
                    data=pdf_bytes,
                    file_name=f"Fraud_Report_{patient_id}.pdf",
                    mime="application/pdf"
                )
