import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import geopandas as gpd
import branca.colormap as cm
from folium.plugins import HeatMap, MarkerCluster
import openrouteservice as ors
from folium import plugins

# Set Mapbox access token (replace with your token)
mapbox_token = "your_mapbox_token"

# Add OpenRouteService client (get API key from openrouteservice.org)
ors_key = "your_ors_key"
ors_client = ors.Client(key=ors_key)

# Page configuration
st.set_page_config(page_title="Interactive Map", layout="wide")
st.title("🌍 Interactive Map Explorer")

# Initialize geocoder
geolocator = Nominatim(user_agent="streamlit-maps")

# Sidebar configuration
st.sidebar.markdown("<h1>Control Panel</h2>", unsafe_allow_html=True)

# Load air quality data
# gdf = gpd.read_file("data/air_quality/air_quality.shp")


# Catalan cities data
cities = {
    "Barcelona": [41.3851, 2.1734],
    "Girona": [41.9842, 2.8237],
    "Lleida": [41.6176, 0.6200],
    "Tarragona": [41.1189, 1.2445],
    "Other": []
}

# Add route selection to sidebar
st.sidebar.header("Route Planning")
start_city = st.sidebar.selectbox("Start city:", list(cities.keys()))
end_city = st.sidebar.selectbox("End city:", list(cities.keys()))

if st.sidebar.button("Calculate Route"):
    try:
        # Get coordinates for route
        coords = [[cities[start_city][1], cities[start_city][0]], 
                 [cities[end_city][1], cities[end_city][0]]]
        
        # Get route from OpenRouteService
        route = ors_client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson'
        )

        # Add route to map
        folium.GeoJson(
            route,
            name='route',
            style_function=lambda x: {'color': 'red', 'weight': 2}
        ).add_to(m)

        # Add distance and duration info
        distance = route['features'][0]['properties']['segments'][0]['distance']
        duration = route['features'][0]['properties']['segments'][0]['duration']
        st.sidebar.info(f"Distance: {distance/1000:.1f} km")
        st.sidebar.info(f"Duration: {duration/60:.0f} min")

    except Exception as e:
        st.sidebar.error(f"Error calculating route: {e}")

# Sidebar configuration
st.sidebar.header("Search Options")
custom_location = st.sidebar.selectbox("Select a city:", list(cities.keys()))
if custom_location == "Other":
    custom_location = st.sidebar.text_input("Enter a location:")

# Initialize map center and zoom
map_center = cities[custom_location] 
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





