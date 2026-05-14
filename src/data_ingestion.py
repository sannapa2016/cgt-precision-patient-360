import pandas as pd

def filter_genomic_candidates(genomic_df, target_mutation="BRAF_V600E"):
    """
    Filters for patients possessing the target mutation.
    """
    return genomic_df[genomic_df['mutation'] == target_mutation]['patient_id'].unique()
