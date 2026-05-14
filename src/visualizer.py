import folium
from folium.plugins import HeatMap

def generate_patient_map(patient_df, qtc_list, output_file='cgt_access_map.html'):
    """
    Creates an interactive map showing patient density and QTC locations.
    """
    # Initialize map at the average coordinates
    m = folium.Map(location=[patient_df['lat'].mean(), patient_df['lon'].mean()], zoom_start=5)

    # 1. Add Heatmap Layer for Patients
    heat_data = [[row['lat'], row['lon']] for index, row in patient_df.iterrows()]
    HeatMap(heat_data, name="Patient Density", radius=15).add_to(m)

    # 2. Add Markers for Treatment Centers (QTCs)
    for center in qtc_list:
        folium.Marker(
            location=[center['lat'], center['lon']],
            popup=center['name'],
            icon=folium.Icon(color='red', icon='plus-sign')
        ).add_to(m)

    m.save(output_file)
    print(f"Map saved to {output_file}")
