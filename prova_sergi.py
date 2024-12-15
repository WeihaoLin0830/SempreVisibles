import streamlit as st
import folium
from streamlit_folium import folium_static
import osmnx as ox
import networkx as nx
import geopy

def find_route(start_location, end_location):
    """
    Find the shortest route between two locations using OpenStreetMap data
    """
    try:
        # Geocode the locations
        geolocator = geopy.Nominatim(user_agent="route_finder")
        start_coords = geolocator.geocode(start_location)
        end_coords = geolocator.geocode(end_location)
        
        if not start_coords or not end_coords:
            st.error("Could not find coordinates for one or both locations")
            return None
        
        # Download the street network
        G = ox.graph_from_point((start_coords.latitude, start_coords.longitude), dist=5000, network_type="drive")
        
        # Find the nearest nodes to start and end locations
        start_node = ox.distance.nearest_nodes(G, start_coords.longitude, start_coords.latitude)
        end_node = ox.distance.nearest_nodes(G, end_coords.longitude, end_coords.latitude)
        
        # Calculate the route
        route = nx.shortest_path(G, start_node, end_node, weight='length')
        
        return G, route, start_coords, end_coords
    
    except Exception as e:
        st.error(f"Error finding route: {e}")
        return None

def create_route_map(G, route, start_coords, end_coords):
    """
    Create a Folium map with the route highlighted
    """
    # Create map centered on the route
    m = folium.Map(location=[(start_coords.latitude + end_coords.latitude) / 2, 
                              (start_coords.longitude + end_coords.longitude) / 2], 
                   zoom_start=13, 
                   tiles='CartoDB positron')
    
    # Add start and end markers
    folium.Marker(
        [start_coords.latitude, start_coords.longitude], 
        popup='Start', 
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        [end_coords.latitude, end_coords.longitude], 
        popup='End', 
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # Extract route coordinates
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    
    # Add route line
    folium.PolyLine(
        route_coords, 
        color='blue', 
        weight=5, 
        opacity=0.8
    ).add_to(m)
    
    return m

def main():
    # Set page configuration
    st.set_page_config(page_title="Route Finder", layout="wide")
    
    # Custom CSS for full-screen map and aesthetic design
    st.markdown("""
    <style>
    .reportview-container {
        background: #F0F2F6;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    /* Full width for the Streamlit app */
    .reportview-container .main {
        max-width: 100%;
        padding: 0;
    }
    /* Styling for input boxes */
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #E0E0E0;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("🗺️ Route Finder")
    st.write("Enter start and end locations to find the best route.")
    
    # Input columns
    col1, col2 = st.columns(2)
    
    with col1:
        start_location = st.text_input("Start Location", placeholder="Enter start address")
    
    with col2:
        end_location = st.text_input("End Location", placeholder="Enter destination address")
    
    # Find route button
    if st.button("Find Route", type="primary"):
        if start_location and end_location:
            # Find and display route
            route_data = find_route(start_location, end_location)
            
            if route_data:
                G, route, start_coords, end_coords = route_data
                route_map = create_route_map(G, route, start_coords, end_coords)
                
                # Display full-screen map
                folium_static(route_map, width=1500, height=800)
            else:
                st.error("Could not find a route. Please check the locations.")
        else:
            st.warning("Please enter both start and end locations")

if __name__ == "__main__":
    main()