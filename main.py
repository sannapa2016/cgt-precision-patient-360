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

from src.geo_mapping import calculate_distance

# Mock data for Treatment Centers
qtc_locations = [{'name': 'Mayo Clinic', 'lat': 44.02, 'lon': -92.46}]

def filter_by_access(patient_df, centers, max_miles=100):
    eligible_ids = []
    for _, patient in patient_df.iterrows():
        for center in centers:
            dist = calculate_distance(patient['lat'], patient['lon'], center['lat'], center['lon'])
            if dist <= max_miles:
                eligible_ids.append(patient['patient_id'])
                break
    return set(eligible_ids)

# --- BEGIN GENERATED DUMMY DATA --- #
# For demonstration, creating dummy patient_data_with_coords since it's not defined.
# In a real scenario, this would come from previous data processing.
import pandas as pd

# Assuming high_value_target (from _SNEXC8c3yHQ) contained patients 1 and 3
# and that these patients would have associated coordinates.
# Current high_value_target is empty due to dummy data in _SNEXC8c3yHQ.
# We will make sure our dummy patient_data_with_coords has some patients
# that might intersect with genetically eligible ones (Patient 1, 3 for BCMA_POSITIVE).

patient_data_with_coords = pd.DataFrame({
    'patient_id': [1, 2, 3, 4],
    'lat': [44.00, 34.05, 44.03, 33.9],
    'lon': [-92.40, -118.24, -92.50, -118.3]
})
# --- END GENERATED DUMMY DATA --- #

# Execute the final Patient-360 Filter
access_eligible = filter_by_access(patient_data_with_coords, qtc_locations)

# Assuming high_value_target is defined from a previous cell.
# If not, for testing, we can define a dummy high_value_target here.
# For consistency with previous dummy data, high_value_target was 0. Let's make it more interesting for access filtering.
# Based on previous execution, candidates_genomic = {1, 3} for BCMA_POSITIVE.
# If candidates_3l was empty, then high_value_target would be empty. Let's make a dummy high_value_target that has some overlap.
if 'high_value_target' not in locals(): # Check if high_value_target is already defined
    print("high_value_target not found, creating dummy for demonstration.")
    high_value_target = {1, 3} # Example if patients 1 and 3 were high-value based on genetics

final_target_list = set(high_value_target).intersection(access_eligible)

print(f"Final Actionable Patients: {len(final_target_list)}")

from src.visualizer import generate_patient_map

# ... (Previous Logic for Genomic and Claims filtering) ...

# Generate the map for the final high-value population
generate_patient_map(final_target_df, qtc_locations)
