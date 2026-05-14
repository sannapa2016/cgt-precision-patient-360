import pandas as pd

def get_genomic_candidates(df, biomarker_column, target_mutation):
    """
    Identifies patients who possess a high-value genetic marker.
    """
    eligible_patients = df[df[biomarker_column] == target_mutation]['patient_id'].unique()
    return set(eligible_patients)
