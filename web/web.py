import math 
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import geopandas as gpd
import branca.colormap as cm
from folium.plugins import HeatMap, MarkerCluster
import openrouteservice as ors
from folium import plugins
import osmnx as ox
import networkx as nx
import geopy

# Set Mapbox access token (replace with your token)
mapbox_token = "your_mapbox_token"

# Add OpenRouteService client (get API key from openrouteservice.org)
ors_key = "your_ors_key"
ors_client = ors.Client(key=ors_key)

# Test with free API key
ors_client = ors.Client(key="5b3ce3597851110001cf6248559770e6473e4b08a048b18d77335d77")

# Page configuration
st.set_page_config(page_title="Interactive Map", layout="wide")
st.title("🌍 Interactive Map Explorer")

# Initialize default map in Barcelona
map_center = [41.3851, 2.1734]  # Barcelona coordinates
zoom = 10

# Initialize geocoder
geolocator = Nominatim(user_agent="streamlit-maps")

# Catalan cities data
cities = ["Barcelona", "Girona", "Lleida", "Tarragona", "Other"]

cities_coords = {    
        "Barcelona": [41.3851, 2.1734],
        "Girona": [41.9842, 2.8237],
        "Lleida": [41.6176, 0.6200],
        "Tarragona": [41.1189, 1.2445]}


# Sidebar configuration
st.sidebar.markdown("<h1>Control Panel</h2>", unsafe_allow_html=True)

# Load air quality data
# gdf = gpd.read_file("data/air_quality/air_quality.shp")

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
    
    # Create marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add city markers to cluster
    for city, coords in cities_coords.items():
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


# Add route selection to sidebar
st.sidebar.header("Route Planning")
start_city = st.sidebar.text_input("Start city:")
end_city = st.sidebar.text_input("End city:")

if st.sidebar.button("Calculate Route"):
    try:
        # Get coordinates for route
        location = geolocator.geocode(start_city)
        end_location = geolocator.geocode(end_city)

        if location and end_location:
            st.sidebar.success(f"Location found: {location.address}")
            st.sidebar.success(f"End location found: {end_location.address}")
            average_coords = [(location.latitude + end_location.latitude) / 2, (location.longitude + end_location.longitude) / 2]
            map_center = [average_coords[0], average_coords[1]]
            zoom = 15

            # Get street network
            G = ox.graph_from_point(
                (location.latitude, location.longitude),
                dist=10000,
                network_type="drive"
            )
            
            # Find nearest nodes
            start_node = ox.distance.nearest_nodes(
                G, 
                location.longitude,
                location.latitude
            )
            end_node = ox.distance.nearest_nodes(
                G,
                end_location.longitude,
                end_location.latitude
            )
            
            # Calculate route
            route = nx.shortest_path(G, start_node, end_node, weight='length')
            
            # Create map
            m = folium.Map(
                location=[(location.latitude + end_location.latitude)/2,
                         (location.longitude + end_location.longitude)/2],
                zoom_start=10
            )
            
            # Add markers
            folium.Marker(
                [location.latitude, location.longitude],
                popup='Start',
                icon=folium.Icon(color='green')
            ).add_to(m)
            
            folium.Marker(
                [end_location.latitude, end_location.longitude],
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
            st_folium(m)

        else:
            st.sidebar.error("Location not found. Please try again.")
        
        # # Get route from OpenRouteService
        # route = ors_client.directions(
        #     coordinates=[[location.longitude, location.latitude], [end_location.longitude, end_location.latitude]],
        #     profile='driving-car',
        #     format='geojson'
        # )

        # # Add route to map
        # folium.GeoJson(
        #     route,
        #     name='route',
        #     style_function=lambda x: {'color': 'red', 'weight': 2}
        # ).add_to(m)

        # st_folium(m)

        # # Display map with route
        # st.write("Displaying map with route...")
        # map_container = st.container()

        # with map_container:
        #     st_folium(
        #     m,
        #     width=None,  # Let Streamlit handle responsive width
        #     height=600,
        #     returned_objects=["last_clicked"]
        #     )

        # # Add route line
        # route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) 
        #               for node in route]
        # folium.PolyLine(
        #     route_coords,
        #     weight=2,
        #     color='blue',
        #     opacity=0.8
        # ).add_to(m)
            
        # # Display map
        # st_folium(m)    

        # Add distance and duration info
        distance = route['features'][0]['properties']['segments'][0]['distance']
        duration = route['features'][0]['properties']['segments'][0]['duration']

        st.sidebar.info(f"Distance: {distance/1000:.1f} km")
        st.sidebar.info(f"Duration: {duration/60:.0f} min")
        st.sidebar.success("Route calculated successfully!")

    except Exception as e:
        st.sidebar.error(f"Error calculating route: {e}")