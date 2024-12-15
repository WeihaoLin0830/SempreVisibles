import math 
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
from geopy.geocoders import Nominatim
import geopandas as gpd
import branca.colormap as cm
from folium.plugins import HeatMap, MarkerCluster
import openrouteservice as ors
from folium import plugins
import osmnx as ox
import networkx as nx
import geopy
from geopy.exc import GeocoderTimedOut

# Set Mapbox access token (replace with your token)
mapbox_token = "your_mapbox_token"

# Test with free API key
ors_client = ors.Client(key="5b3ce3597851110001cf6248559770e6473e4b08a048b18d77335d77")

# Page configuration
st.set_page_config(page_title="Route Finder", layout="wide")
st.title("🗺️ Route Finder")

# Initialize default map in Barcelona
map_center = [41.3851, 2.1734]  # Barcelona coordinates
zoom = 10

# Initialize geocoder
geolocator = Nominatim(user_agent="route_finder_app")

# Catalan cities data
cities = ["Barcelona", "Girona", "Lleida", "Tarragona", "Other"]

cities_coords = {    
        "Barcelona": [41.3851, 2.1734],
        "Girona": [41.9842, 2.8237],
        "Lleida": [41.6176, 0.6200],
        "Tarragona": [41.1189, 1.2445]}


# Sidebar configuration
st.sidebar.markdown("<h1>Control Panel</h2>", unsafe_allow_html=True)

# # Load air quality data
# # gdf = gpd.read_file("data/air_quality/air_quality.shp")

# Sidebar configuration
st.sidebar.header("Search Options")
custom_location = st.sidebar.selectbox("Select a city:", list(cities))

if custom_location == "Other":
    custom_location = st.sidebar.text_input("Or enter a custom location:")


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
    
#     # Create marker cluster
#     marker_cluster = MarkerCluster().add_to(m)
    
#     # Add city markers to cluster
#     for city, coords in cities_coords.items():
#         folium.Marker(
#             location=coords,
#             popup=f"<strong>{city}</strong>",
#             tooltip=city,
#             icon=folium.Icon(color="red", icon="info-sign"),
#         ).add_to(marker_cluster)

#     # Check if location exists before adding marker
#     if 'location' in locals() and location is not None:
#         try:
#             folium.Marker(
#                 location=[location.latitude, location.longitude],
#                 popup=f"<strong>{location.address}</strong>",
#                 tooltip="Searched location",
#                 icon=folium.Icon(color="blue", icon="info-sign")
#             ).add_to(m)
#         except Exception as marker_error:
#             st.error(f"Error adding marker: {marker_error}")
    
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
    
#     # Add instructions in sidebar
#     st.sidebar.markdown("""
#     ### Instructions:
#     - 🌍 Select a predefined city or
#     - 🔎 Search for any location
#     - 🗺️ Use map controls to change views
#     - 📍 Click markers for more info
#     """)

except Exception as e:
    st.error(f"Error creating map: {e}")
    st.info("Please try refreshing the page")



# Sidebar inputs
st.sidebar.header("Route Options")
start_location = st.sidebar.text_input("Start Location", "Barcelona")
end_location = st.sidebar.text_input("End Location", "Hospitalet del Llobregat")

if st.sidebar.button("Find Route"):
    try:
        # Get coordinates
        start_coords = geolocator.geocode(start_location)
        end_coords = geolocator.geocode(end_location)
        
        if start_coords and end_coords:
            # Get street network
            G = ox.graph_from_point(
                (start_coords.latitude, start_coords.longitude),
                dist=10000,
                network_type="drive"
            )
            
            # Find nearest nodes
            start_node = ox.distance.nearest_nodes(
                G, 
                start_coords.longitude,
                start_coords.latitude
            )
            end_node = ox.distance.nearest_nodes(
                G,
                end_coords.longitude,
                end_coords.latitude
            )
            
            # Calculate route
            route = nx.shortest_path(G, start_node, end_node, weight='length')
            
            # Create map
            m = folium.Map(
                location=[(start_coords.latitude + end_coords.latitude)/2,
                         (start_coords.longitude + end_coords.longitude)/2],
                zoom_start=10
            )
            
            # Add markers
            folium.Marker(
                [start_coords.latitude, start_coords.longitude],
                popup='Start',
                icon=folium.Icon(color='green')
            ).add_to(m)
            
            folium.Marker(
                [end_coords.latitude, end_coords.longitude],
                popup='End',
                icon=folium.Icon(color='red')
            ).add_to(m)
            
            # Add route line
            route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) 
                          for node in route]
            folium.PolyLine(
                route_coords,
                weight=2,
                color='blue',
                opacity=0.8
            ).add_to(m)
            
            # Display map
            st.write("Route found!")
            map_container = st.container()
            with map_container:
                folium_static(m, width=None, height=600)
            
        else:
            st.error("Could not find one or both locations")
            
    except Exception as e:
        st.error(f"Error finding route: {str(e)}")

