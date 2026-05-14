import pandas as pd

def calculate_lot(claims_df, gap_threshold=60):
    """
    Identifies Lines of Therapy based on treatment gaps and drug switches.
    """
    # Sort by patient and service date
    df = claims_df.sort_values(['patient_id', 'service_date'])
    
    df['prev_date'] = df.groupby('patient_id')['service_date'].shift(1)
    df['date_diff'] = (df['service_date'] - df['prev_date']).dt.days
    
    # Logic: New line if gap > threshold OR if a new drug is added
    df['is_new_line'] = (df['date_diff'] > gap_threshold) | (df['drug_name'] != df.groupby('patient_id')['drug_name'].shift(1))
    df['line_number'] = df.groupby('patient_id')['is_new_line'].cumsum()
    
    return df
