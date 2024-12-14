import os
import xarray as xr  # Más eficiente que netCDF4
import pandas as pd  # Para convertir a CSV

# Ruta de la carpeta donde se encuentran los archivos .nc
directorio = r'C:/Users/jiahu/OneDrive/Escritorio/AI3/Bitsxm/Dades/CALIOPE/hourly/sconcno2'

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
            
            # Convertir todas las variables del archivo a un DataFrame
            df = dataset.to_dataframe().reset_index()
            
            # Mostrar las primeras filas del DataFrame para verificar
            print(df.head())
            
            # Ruta de salida para guardar el CSV
            nombre_csv = archivo.replace('.nc', '.csv')
            ruta_csv = os.path.join(directorio, nombre_csv)
            
            # Guardar los datos en CSV
            df.to_csv(ruta_csv, index=False)
            
            print(f"Archivo CSV guardado: {ruta_csv}")
        
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
