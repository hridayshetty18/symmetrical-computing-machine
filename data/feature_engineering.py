import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def create_features(df):
    """Generates numerical and categorical features."""
    # Claim Difference
    df['Claim_Difference'] = df['Claim_Amount'] - df['Settled_Amount']
    df['Settlement_Ratio'] = np.where(df['Claim_Amount'] > 0, 
                                     df['Settled_Amount'] / df['Claim_Amount'], 
                                     0)
    
    # Patient Claim Frequency
    patient_freq = df.groupby('Patient_ID').size().to_dict()
    df['Patient_Claim_Freq'] = df['Patient_ID'].map(patient_freq)
    
    # Hospital Claim Frequency
    hospital_freq = df.groupby('Hospital').size().to_dict()
    df['Hospital_Claim_Freq'] = df['Hospital'].map(hospital_freq)
    
    # Target encoding (1 for Fraud, 0 for Clean)
    if 'Status' in df.columns:
        df['Is_Fraud'] = (df['Status'] == 'Suspected Fraud').astype(int)
        
    return df

def extract_text_features(df, vectorizer=None, fit=False):
    """Applies TF-IDF to the Remarks column."""
    if fit or vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['Remarks'])
    else:
        tfidf_matrix = vectorizer.transform(df['Remarks'])
        
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                            columns=[f"remark_{i}" for i in range(tfidf_matrix.shape[1])])
    
    # Concatenate features
    df_combined = pd.concat([df.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)
    return df_combined, vectorizer
