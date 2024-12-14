import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Page config
st.set_page_config(
    page_title="Data Visualization App",
    layout="wide"
)

# Título
st.title("Mapa Interactivo - Búsqueda por Zona")

# Entrada del usuario para la zona
zona_busqueda = st.text_input("Ingresa el nombre de la zona o coordenadas (opcional):", "")

# Crear un mapa base con folium
map_center = [40.4168, -3.7038]  # Madrid, por ejemplo
map_zoom = 6
if zona_busqueda:
    # Ajustar el mapa al resultado de la búsqueda (ejemplo estático)
    map_center = [40.4168, -3.7038]  # Cambiar según la búsqueda
    map_zoom = 12

mapa = folium.Map(location=map_center, zoom_start=map_zoom)

# Cargar un GeoJSON o shapefile para zonas si es necesario
geojson_path = "path_to_zones.geojson"  # Cambiar al archivo real
try:
    geo_data = gpd.read_file(geojson_path)
    folium.GeoJson(geo_data).add_to(mapa)
except Exception as e:
    st.warning("No se pudo cargar las zonas. Error: " + str(e))

# Mostrar el mapa
st_folium(mapa, width=1200, height=1200)

# Opcional: Incluir funcionalidad para buscar coordenadas o zonas
st.write("Añade más filtros o datos según sea necesario.")

