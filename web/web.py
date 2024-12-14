import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import geopandas as gpd
import branca.colormap as cm
from folium.plugins import HeatMap, MarkerCluster

# Set Mapbox access token (replace with your token)
mapbox_token = "your_mapbox_token"

# Page configuration
st.set_page_config(page_title="Interactive Map", layout="wide")
st.title("🌍 Interactive Map Explorer")

# Initialize geocoder
geolocator = Nominatim(user_agent="streamlit-maps")

# Catalan cities data
cities = {
    "Barcelona": [41.3851, 2.1734],
    "Girona": [41.9842, 2.8237],
    "Lleida": [41.6176, 0.6200],
    "Tarragona": [41.1189, 1.2445]
}

# Sidebar configuration
st.sidebar.header("Search Options")
selected_city = st.sidebar.selectbox("Select a city:", list(cities.keys()))
custom_location = st.sidebar.text_input("📍 Search custom location:", "")

# Initialize map center and zoom
map_center = cities[selected_city]
zoom = 12

# Handle custom location search
if st.sidebar.button("Search"):
    try:
        location = geolocator.geocode(custom_location)
        if location:
            st.sidebar.success(f"Location found: {location.address}")
            map_center = [location.latitude, location.longitude]
            zoom = 15
        else:
            st.sidebar.error("Location not found. Please try again.")
    except Exception as e:
        st.sidebar.error(f"Search error: {str(e)}")

try:
    # Debug message
    st.write("Initializing map...")
    
    # Create base map with multiple tile layers
    m = folium.Map(
        location=map_center,  # Default to selected city
        zoom_start=zoom,
        tiles=None  # Remove default tiles
    )
    
    # Add various tile layers
    folium.TileLayer(
        tiles='https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=' + mapbox_token,
        attr='Mapbox',
        name='Mapbox Streets'
    ).add_to(m)
    
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(m)
    folium.TileLayer('cartodbpositron', name='CartoDB Positron').add_to(m)
    
    # Create marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add city markers to cluster
    for city, coords in cities.items():
        folium.Marker(
            location=coords,
            popup=f"<strong>{city}</strong>",
            tooltip=city,
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(marker_cluster)

    # Check if location exists before adding marker
    if 'location' in locals() and location is not None:
        try:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=f"<strong>{location.address}</strong>",
                tooltip="Searched location",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
        except Exception as marker_error:
            st.error(f"Error adding marker: {marker_error}")
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Display map with adjusted dimensions and container
    st.write("Displaying map...")
    map_container = st.container()
    with map_container:
        st_folium(
            m,
            width=None,  # Let Streamlit handle responsive width
            height=600,
            returned_objects=["last_clicked"]
        )
    
    # Add instructions in sidebar
    st.sidebar.markdown("""
    ### Instructions:
    - 🌍 Select a predefined city or
    - 🔎 Search for any location
    - 🗺️ Use map controls to change views
    - 📍 Click markers for more info
    """)

except Exception as e:
    st.error(f"Error creating map: {e}")
    st.info("Please try refreshing the page")





