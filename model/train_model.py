import os
import sys

# Ensure imports work from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from data.preprocessing import preprocess_pipeline
from data.feature_engineering import create_features, extract_text_features

def train_and_save_model():
    print("Loading and preprocessing data...")
    df = preprocess_pipeline("HL Main.xlsx")
    
    print("Engineering features...")
    df = create_features(df)
    df, vectorizer = extract_text_features(df, fit=True)
    
    # Define features
    numerical_features = ['Claim_Amount', 'Settled_Amount', 'Claim_Difference', 
                          'Settlement_Ratio', 'Patient_Claim_Freq', 'Hospital_Claim_Freq']
    tfidf_features = [c for c in df.columns if c.startswith('remark_')]
    features = numerical_features + tfidf_features
    
    X = df[features]
    y = df['Is_Fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    
    # Save model, vectorizer, and feature names
    print("Saving artifacts...")
    os.makedirs('model', exist_ok=True)
    with open('model/fraud_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('model/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    with open('model/features_list.pkl', 'wb') as f:
        pickle.dump(features, f)
        
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    train_and_save_model()
