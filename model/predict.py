import os
import pickle
import pandas as pd
import numpy as np

# Resolve paths so it can be run from anywhere
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'fraud_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'tfidf_vectorizer.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'model', 'features_list.pkl')

class RiskScoreGenerator:
    def __init__(self):
        try:
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            with open(VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open(FEATURES_PATH, 'rb') as f:
                self.features_list = pickle.load(f)
        except Exception as e:
            print(f"Error loading models: {e}")
            self.model = None
            
    def predict(self, claim_data):
        """
        claim_data is a dictionary containing:
        Claim_Amount, Settled_Amount, Remarks, Patient_ID, Hospital, etc.
        """
        if self.model is None:
            return {"error": "Model not loaded."}
            
        # Convert to DataFrame
        df = pd.DataFrame([claim_data])
        
        # We need historical stats to calculate freq properly. 
        # For a true system, we'd query the DB. Here we just mock or use default.
        df['Claim_Difference'] = df['Claim_Amount'] - df.get('Settled_Amount', 0)
        df['Settlement_Ratio'] = np.where(df['Claim_Amount'] > 0, 
                                         df.get('Settled_Amount', 0) / df['Claim_Amount'], 
                                         0)
                                         
        # Mocking frequency if not passed
        df['Patient_Claim_Freq'] = df.get('Patient_Claim_Freq', 1)
        df['Hospital_Claim_Freq'] = df.get('Hospital_Claim_Freq', 5)
        
        df['Remarks'] = df.get('Remarks', "No remarks")
        
        # Apply TF-IDF
        tfidf_matrix = self.vectorizer.transform(df['Remarks'])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                                columns=[f"remark_{i}" for i in range(tfidf_matrix.shape[1])])
                                
        df_combined = pd.concat([df.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)
        
        # Ensure all features exist
        for f in self.features_list:
            if f not in df_combined.columns:
                df_combined[f] = 0
                
        X = df_combined[self.features_list]
        
        # Predict probability
        prob = self.model.predict_proba(X)[0][1] # Probability of Class 1 (Fraud)
        risk_score = int(prob * 100)
        
        # Determine level
        if risk_score > 80:
            level = "🔴 Critical"
        elif risk_score > 50:
            level = "🟠 High"
        elif risk_score > 20:
            level = "🟡 Moderate"
        else:
            level = "🟢 Low"
            
        return {
            "risk_score": risk_score,
            "probability": prob,
            "risk_level": level,
            "input_features": X # Needed for SHAP
        }
