import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load the data files
@st.cache_data
def load_csv():
    return pd.read_csv('data.csv')

@st.cache_data
def load_geojson():
    return gpd.read_file('up_districts.geojson')

data = load_csv()
geojson = load_geojson()

# Streamlit UI
st.title("Uttar Pradesh Map Visualization")
st.write("This app visualizes data from 'data.csv' on the Uttar Pradesh map.")

# Toggle to select dataset
data_option = st.radio("Select data to display:", ("Rahat", "IMD", "Combined"))

# Map setup with a minimal base map
m = folium.Map(location=[26.8467, 80.9462], zoom_start=7, tiles="CartoDB positron")

# Add GeoJSON layer
folium.GeoJson(
    geojson,
    name='Uttar Pradesh Districts',
    style_function=lambda feature: {
        'fillColor': 'white',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.1,
    },
).add_to(m)

# Add markers and styled markers based on selected data

def add_rahat_markers(data, map_object):
    for _, row in data.iterrows():
        if not pd.isna(row['Lat1']) and not pd.isna(row['Long1']):
            marker_type = row.get('Rahat', 'Unknown')
            if marker_type == 'AWS':
                color = 'red'
                folium.Marker(
                    location=[row['Lat1'], row['Long1']],
                    popup=f"Rahat ({marker_type})\nLat: {row['Lat1']}\nLong: {row['Long1']}\nStation: {row['District']}\nTehsil: {row['Tehsil']}",
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(map_object)
            elif marker_type == 'ARG':
                color = 'red'
                folium.CircleMarker(
                    location=[row['Lat1'], row['Long1']],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=f"Rahat ({marker_type})\nLat: {row['Lat1']}\nLong: {row['Long1']}\nStation: {row['District']}\nTehsil: {row['Tehsil']}"
                ).add_to(map_object)

def add_imd_markers(data, map_object):
    for _, row in data.iterrows():
        if not pd.isna(row['Lat2']) and not pd.isna(row['Long2']):
            marker_type = row.get('IMD', 'Unknown')
            if marker_type == 'AWS':
                color = 'blue'
                folium.Marker(
                    location=[row['Lat2'], row['Long2']],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=f"IMD ({marker_type})\nLat: {row['Lat2']}\nLong: {row['Long2']}\nStation: {row['DISTRICT-Name']}\nTehsil: {row['Station-Name']}"
                ).add_to(map_object)
            elif marker_type == 'ARG':
                color = 'blue'
                folium.CircleMarker(
                    location=[row['Lat2'], row['Long2']],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=f"IMD ({marker_type})\nLat: {row['Lat2']}\nLong: {row['Long2']}\nStation: {row['DISTRICT-Name']}\nTehsil: {row['Station-Name']}"
                ).add_to(map_object)

def add_combined(data, map_object):
    add_rahat_markers(data, map_object)
    add_imd_markers(data, map_object)

if data_option == "Rahat":
    add_rahat_markers(data, m)
elif data_option == "IMD":
    add_imd_markers(data, m)
elif data_option == "Combined":
    add_combined(data, m)

# Display the map
st_data = st_folium(m, width=800, height=600)

# Add a legend below the map
st.markdown("""
### Legend
- **Red Markers**: Rahat AWS (Rahat data with marker type 'AWS')
- **Red Circles**: Rahat ARG (Rahat data with 'ARG' type, displayed as circles)
- **Blue Circles**: IMD AWS (IMD data with 'AWS' type, displayed as circles)
- **Blue Markers**: IMD ARG (IMD data with 'ARG' type, displayed as markers)
""")

# Optionally allow downloading the map as an HTML file
if st.button("Download Map as HTML"):
    map_file_path = "uttar_pradesh_map.html"
    m.save(map_file_path)
    with open(map_file_path, "rb") as file:
        st.download_button(
            label="Download Map HTML",
            data=file,
            file_name="uttar_pradesh_map.html",
            mime="text/html"
        )
