import pandas as pd
import numpy as np

def load_data(filepath="HL Main.csv"):
    """Loads the main dataset."""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Handles missing values and formats types."""
    # Drop rows without Claim_ID or Patient_ID
    df = df.dropna(subset=['Claim_ID', 'Patient_ID'])
    
    # Fill missing values
    df['Remarks'] = df['Remarks'].fillna("No Remarks")
    df['Status'] = df['Status'].fillna("Clean")
    
    # Convert dates
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Convert numerical columns
    df['Claim_Amount'] = pd.to_numeric(df['Claim_Amount'], errors='coerce').fillna(0)
    df['Settled_Amount'] = pd.to_numeric(df['Settled_Amount'], errors='coerce').fillna(0)
    
    return df

def preprocess_pipeline(filepath="HL Main.csv"):
    """Full preprocessing pipeline."""
    df = load_data(filepath)
    df = clean_data(df)
    return df
