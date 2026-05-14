import pandas as pd

# 1. Load your datasets (Use mock data for testing)
# If 'data/claims.csv' and 'data/genomics.csv' are not in your Colab environment,
# you will need to upload them. For demonstration, I will create dummy data.
try:
    claims_data = pd.read_csv('data/claims.csv', parse_dates=['service_date'])
    genomic_data = pd.read_csv('data/genomics.csv')
except FileNotFoundError:
    print("Required data files not found. Creating dummy data for demonstration.")
    # Create dummy claims data with required columns for flag_treatment_lines
    claims_data = pd.DataFrame({
        'patient_id': [1, 1, 1, 2, 2, 3, 3, 3],
        'service_date': [
            pd.to_datetime('2023-01-01'), pd.to_datetime('2023-01-15'), pd.to_datetime('2023-03-01'),
            pd.to_datetime('2023-02-01'), pd.to_datetime('2023-02-10'), pd.to_datetime('2023-01-05'), pd.to_datetime('2023-01-20'), pd.to_datetime('2023-03-10')
        ],
        'drug_name': ['DrugA', 'DrugA', 'DrugB', 'DrugC', 'DrugC', 'DrugA', 'DrugA', 'DrugD']
    })

    # Create dummy genomic profiles data with required columns for get_genomic_candidates
    genomic_data = pd.DataFrame({
        'patient_id': [1, 2, 3],
        'biomarker': ['BCMA_POSITIVE', 'HER2_POS', 'BCMA_POSITIVE']
    })

# 2. Process Claims to find patients in 3rd Line of Therapy (3L+)
processed_claims = flag_treatment_lines(claims_data)
candidates_3l = processed_claims[processed_claims['current_lot'] >= 3]['patient_id'].unique()

# 3. Process Genomics to find specific biomarkers (e.g., BCMA+)
candidates_genomic = get_genomic_candidates(genomic_data, 'biomarker', 'BCMA_POSITIVE')

# 4. Identify the "High-Value" Sub-population
high_value_target = set(candidates_3l).intersection(candidates_genomic)

print(f"Project Insight: Found {len(high_value_target)} patients eligible for CGT intervention.")
