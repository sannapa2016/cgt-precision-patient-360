import pandas as pd
from datetime import datetime, timedelta

# 1. Load Data
# If 'claims_data.csv' and 'genomic_profiles.csv' are not in your Colab environment,
# you will need to upload them. For demonstration, I will create dummy data.
try:
    claims = pd.read_csv('claims_data.csv', parse_dates=['service_date'])
    genomics = pd.read_csv('genomic_profiles.csv')
except FileNotFoundError:
    print("Required data files not found. Creating dummy data for demonstration.")
    # Create dummy claims data with required columns for calculate_lot
    claims_data = {
        'patient_id': [1, 1, 1, 2, 2, 3, 3, 3],
        'service_date': [
            datetime(2023, 1, 1), datetime(2023, 1, 15), datetime(2023, 3, 1),
            datetime(2023, 2, 1), datetime(2023, 2, 10), datetime(2023, 1, 5), datetime(2023, 1, 20), datetime(2023, 3, 10)
        ],
        'drug_name': ['DrugA', 'DrugA', 'DrugB', 'DrugC', 'DrugC', 'DrugA', 'DrugA', 'DrugD']
    }
    claims = pd.DataFrame(claims_data)

    # Create dummy genomic profiles data with required columns for filter_genomic_candidates
    genomics_data = {
        'patient_id': [1, 2, 3],
        'mutation': ['HER2_POS', 'BRAF_V600E', 'HER2_POS']
    }
    genomics = pd.DataFrame(genomics_data)

# 2. Identify 3L+ Patients
claims_with_lot = calculate_lot(claims)
eligible_by_clinic = claims_with_lot[claims_with_lot['line_number'] >= 3]['patient_id'].unique()

# 3. Identify Genetically Eligible
eligible_by_genetics = filter_genomic_candidates(genomics, "HER2_POS")

# 4. Intersection (The High-Value Sub-population)
high_value_patients = set(eligible_by_clinic).intersection(set(eligible_by_genetics))

print(f"Total High-Value Candidates identified for CGT: {len(high_value_patients)}")
