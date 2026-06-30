import sys
import os

# Ensure paths
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    print("Testing data pipeline...")
    from data.preprocessing import preprocess_pipeline
    from data.feature_engineering import create_features
    df = preprocess_pipeline("HL Main.xlsx")
    df = create_features(df)
    assert len(df) > 0
    print("✅ Data pipeline OK.")
    
    print("Testing model prediction...")
    from model.predict import RiskScoreGenerator
    predictor = RiskScoreGenerator()
    claim_data = {
        "Patient_ID": "PAT123",
        "Hospital": "Hospital A",
        "Claim_Amount": 50000,
        "Settled_Amount": 10000,
        "Remarks": "Duplicate bill"
    }
    result = predictor.predict(claim_data)
    assert "risk_score" in result
    assert "input_features" in result
    print("✅ Model prediction OK.")
    
    print("Testing SHAP...")
    from utils.explainability import generate_shap_explanation
    reasons, impact = generate_shap_explanation(predictor.model, result["input_features"], predictor.features_list)
    assert len(reasons) > 0
    print("✅ SHAP OK.")
    
    print("Testing Network Graph...")
    from utils.network import plot_fraud_network
    fig = plot_fraud_network(df)
    assert fig is not None
    print("✅ Network graph OK.")
    
    print("Testing PDF Generation...")
    from utils.reports import generate_pdf_report
    pdf_bytes = generate_pdf_report(claim_data, result["risk_score"], reasons)
    assert len(pdf_bytes) > 0
    print("✅ PDF Generation OK.")
    
    print("All backend components passed!")

if __name__ == "__main__":
    run_tests()
