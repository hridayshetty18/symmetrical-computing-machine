import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=5000):
    np.random.seed(42)
    random.seed(42)

    states = ['Maharashtra', 'Delhi', 'Tamil Nadu', 'Karnataka', 'Gujarat', 'Uttar Pradesh', 'West Bengal']
    hospitals = [f"Hospital {chr(65+i)}{chr(65+j)}" for i in range(26) for j in range(26)][:200]
    provider_types = ['Multispeciality', 'Clinic', 'Nursing Home', 'Government']
    
    # Base Remarks
    normal_remarks = [
        "All documents verified.", "Standard procedure followed.", "Patient discharged successfully.",
        "Bills are in order.", "No issues found.", "Claim approved.", "Treatment as per protocol."
    ]
    fraud_remarks = [
        "Duplicate Bill Detected", "Fake Discharge Summary", "Inflated Billing", 
        "Repeated Implant Charges", "Signatures forged", "Mismatch in diagnosis and treatment",
        "Patient not admitted on claimed dates", "Overcharged for room rent"
    ]

    data = []
    
    for _ in range(num_records):
        claim_id = f"CLM{random.randint(100000, 999999)}"
        patient_id = f"PAT{random.randint(1000, 9999)}"
        hospital = random.choice(hospitals)
        state = random.choice(states)
        provider_type = random.choice(provider_types)
        
        # Fraud probability logic
        is_fraud = random.random() < 0.15 # 15% overall fraud rate
        
        if is_fraud:
            claim_amount = np.random.lognormal(mean=11.5, sigma=1.0) # Higher claims for fraud
            settled_amount = claim_amount * random.uniform(0.1, 0.4) # Settled much lower
            remark = random.choice(fraud_remarks)
            target = "Suspected Fraud"
        else:
            claim_amount = np.random.lognormal(mean=10.0, sigma=0.5)
            settled_amount = claim_amount * random.uniform(0.7, 1.0)
            remark = random.choice(normal_remarks)
            target = "Clean"
            
        claim_amount = round(claim_amount, 2)
        settled_amount = round(settled_amount, 2)
        
        date = datetime.today() - timedelta(days=random.randint(0, 730))
        
        data.append({
            "Claim_ID": claim_id,
            "Patient_ID": patient_id,
            "Hospital": hospital,
            "State": state,
            "Provider_Type": provider_type,
            "Date": date.strftime("%Y-%m-%d"),
            "Claim_Amount": claim_amount,
            "Settled_Amount": settled_amount,
            "Remarks": remark,
            "Status": target
        })

    df = pd.DataFrame(data)
    
    # Add repeated claims for fraud cases
    fraud_indices = df[df['Status'] == 'Suspected Fraud'].index
    for idx in random.sample(list(fraud_indices), int(len(fraud_indices) * 0.3)):
        # Create a duplicate/repeated claim
        dup = df.loc[idx].copy()
        dup['Claim_ID'] = f"CLM{random.randint(100000, 999999)}"
        dup['Date'] = (datetime.strptime(dup['Date'], "%Y-%m-%d") + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")
        dup['Remarks'] = "Repeated Claim"
        df = pd.concat([df, pd.DataFrame([dup])], ignore_index=True)
        
    df.to_csv("HL Main.csv", index=False)
    print("Dataset generated: HL Main.csv")

if __name__ == "__main__":
    generate_synthetic_data()
