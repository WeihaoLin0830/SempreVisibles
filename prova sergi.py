import streamlit as st
import folium
from streamlit_folium import folium_static
import osmnx as ox
import networkx as nx
import geopy
from geopy.geocoders import Nominatim
from folium import CustomIcon

# Sample store data with more detailed location information

def geocode_address(address):
    """
    Convert address to coordinates using geopy
    """
    try:
        geolocator = Nominatim(user_agent="store_locator")
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return None

def find_route(start_address, end_address):
    """
    Find the shortest route between two addresses and center the map on the start location
    """
    try:
        # Geocode start and end addresses
        start_coords = geocode_address(start_address)
        end_coords = geocode_address(end_address)
        
        if not start_coords or not end_coords:
            st.error("Could not find coordinates for one or both locations")
            return None
        
        # Download street network
        G = ox.graph_from_point(start_coords, dist=5000, network_type="drive")
        
        # Find nearest nodes
        start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
        end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])
        
        # Calculate route
        route = nx.shortest_path(G, start_node, end_node, weight='length')
        
        # Center map on start location
        st.session_state['map_center'] = start_coords
        
        return G, route, start_coords, end_coords
    
    except Exception as e:
        st.error(f"Route finding error: {e}")
        return None

def create_map(selected_store=None, route_data=None):
    """
    Create a Folium map with store markers and optional route
    """
    # Center the map on New York
    m = folium.Map(
        location=[41.3851, 2.1734],  # Coordinates for Catalunya (Barcelona)
        zoom_start=8,
        tiles="cartodbdark_matter"
    )
    
    # Add store markers
 

    
    # Add route if available
    if route_data:
        G, route, start_coords, end_coords = route_data
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        
        # Add start and end markers
        folium.Marker(
            start_coords, 
            icon=folium.Icon(color='green', icon='play'),
            popup='Start Location'
        ).add_to(m)
        
        folium.Marker(
            end_coords, 
            icon=folium.Icon(color='red', icon='stop'),
            popup='End Location'
        ).add_to(m)
        
        # Draw route
        folium.PolyLine(
            route_coords,
            color='#00FF9D',
            weight=5,
            opacity=0.8
        ).add_to(m)
    
    return m

def main():
    # Page configuration
    st.set_page_config(page_title="Store Locator", layout="wide")
    
    # Custom CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');
    
    div.block-container{padding-top:0rem;}
    body {
        background-color: #1E1E1E;
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 12px 20px;
    }
    .store-list {
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 10px;
    }
    .store-item {
        display: flex;
        align-items: center;
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        cursor: pointer;
    }
    .store-item:hover {
        background-color: #3D3D3D;
    }
    .store-logo {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 15px;
        object-fit: contain;
    }
    
    /* Elimina padding superior */
    .main .block-container {
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        margin-top: -3rem;  /* Reduce margen superior */
    }
    
    /* Asegura que el contenedor principal ocupe todo el ancho */
    .reportview-container .main {
        max-width: 100%;
        margin-top: -65px;  /* Reduce aún más el margen superior */
    }
    
    /* Opcional: Oculta completamente el header de Streamlit */
    header {
        display: none !important;
    }
                
    

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
                

    </style>
    """, unsafe_allow_html=True)
    
    # Layout
    col1, col2 = st.columns([3, 7])
    
    with col1:
        st.markdown("<h2 style='font-size: 24px; margin-bottom: 20px;'>Store Locator</h2>", unsafe_allow_html=True)
        
        # Route search
        st.markdown("<h3 style='font-size: 18px; margin-bottom: 10px;'>Find Route</h3>", unsafe_allow_html=True)
        start_address = st.text_input("Start Address", placeholder="Enter start location")
        end_address = st.text_input("End Address", placeholder="Enter destination")
        
        # Find route button
        if st.button("Get Route", type="primary"):
            if start_address and end_address:
                # Find route
                route_data = find_route(start_address, end_address)
                
                if route_data:
                    # Create map with route
                    m = create_map(route_data=route_data)
                    
                    # Display map in column 2
                    with col2:
                        folium_static(m, width=900, height=800)
        
        # Store list
        
    
    with col2:
        # Initialize map
        m = create_map()
        folium_static(m, width=900, height=800)

if __name__ == "__main__":
    main()