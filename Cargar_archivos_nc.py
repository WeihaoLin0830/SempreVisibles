#pip install xarray netCDF4 pandas
import os
import xarray as xr  # Más eficiente que netCDF4
import pandas as pd  # Para convertir a CSV

# Ruta de la carpeta donde se encuentran los archivos .nc
directorio = r'../Dades/DADES_CALIOPE_buenos/NO2'

# Recorre todos los archivos .nc de la carpeta
for archivo in os.listdir(directorio):
    if archivo.endswith('.nc'):
        ruta_archivo = os.path.join(directorio, archivo)
        
        print(f"Procesando archivo: {archivo}")
        
        try:
            # Abrir el archivo .nc con xarray (sin cargar todos los datos a la vez)
            dataset = xr.open_dataset(ruta_archivo)
            
            # Muestra las variables disponibles en el archivo
            print(f"Variables en {archivo}: {list(dataset.data_vars.keys())}")
            
            # Convertir todas las variables del archivo a un pd.DataFrame
            archivo = dataset.to_dataframe().reset_index()
            archivo = archivo.replace('.nc', '')
            
            archivo['time'] = pd.to_datetime(archivo['time'])

            archivo = archivo.drop(columns=['x', 'y', 'Lambert_conformal', 'lev'])
            # Mostrar las primeras filas del DataFrame para verificar
            print(archivo.head())
        
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")

#print(sconcno2_2023122600.nc).columns
# TO DO:
# - Filtrar las variables que no se necesitan
# - Convertir time a datetime
