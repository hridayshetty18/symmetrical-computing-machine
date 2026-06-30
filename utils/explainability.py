import shap
import pandas as pd
import numpy as np

def generate_shap_explanation(model, input_features, feature_names):
    """
    Generates a SHAP explanation for a given prediction.
    """
    # Create explainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_features)
    
    # Random Forest returns a list for each class. We want class 1 (Fraud)
    if isinstance(shap_values, list):
        shap_vals = shap_values[1][0]
    else:
        # Depending on version/model, it might be an array
        if len(shap_values.shape) == 3:
            shap_vals = shap_values[:, :, 1][0]
        else:
            shap_vals = shap_values[0]
            
    # Pair feature names with their SHAP values
    feature_impact = []
    for i, feature in enumerate(feature_names):
        impact = shap_vals[i]
        val = input_features.iloc[0][feature]
        if abs(impact) > 0.01: # Filter tiny impacts
            feature_impact.append({
                "feature": feature,
                "value": val,
                "impact": impact
            })
            
    # Sort by absolute impact
    feature_impact.sort(key=lambda x: abs(x["impact"]), reverse=True)
    
    # Generate human-readable reasons
    reasons = []
    for item in feature_impact[:5]: # Top 5 reasons
        f = item["feature"]
        v = item["value"]
        i = item["impact"]
        
        direction = "increased" if i > 0 else "decreased"
        
        if f == "Claim_Difference":
            reasons.append(f"Difference between claim and settlement is {v:.2f}, which {direction} risk.")
        elif f == "Settlement_Ratio":
            reasons.append(f"Settlement ratio is {v:.2f}, which {direction} risk.")
        elif f.startswith("remark_"):
            reasons.append(f"Specific investigation remarks {direction} the risk profile.")
        elif f == "Claim_Amount":
            reasons.append(f"Claim amount of {v:.2f} {direction} risk.")
        elif f == "Patient_Claim_Freq":
            reasons.append(f"Patient has filed {v} claims, which {direction} risk.")
        elif f == "Hospital_Claim_Freq":
            reasons.append(f"Hospital has filed {v} claims, which {direction} risk.")
            
    return reasons, feature_impact
