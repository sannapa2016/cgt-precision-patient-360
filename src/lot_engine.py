import pandas as pd

def flag_treatment_lines(df, gap_days=90):
    """
    Calculates Lines of Therapy (LOT). 
    A new line is triggered by a significant gap in treatment or a drug switch.
    """
    df = df.sort_values(by=['patient_id', 'service_date'])
    
    # Calculate gap between treatments
    df['prev_date'] = df.groupby('patient_id')['service_date'].shift(1)
    df['days_since_last'] = (df['service_date'] - df['prev_date']).dt.days
    
    # Flag new lines
    df['new_line_flag'] = (df['days_since_last'] > gap_days) | (df['days_since_last'].isna())
    df['current_lot'] = df.groupby('patient_id')['new_line_flag'].cumsum()
    
    return df
