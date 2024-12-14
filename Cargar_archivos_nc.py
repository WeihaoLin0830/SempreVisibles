#pip install xarray netCDF4 pandas
import os
import xarray as xr  # Más eficiente que netCDF4
import pandas as pd  # Para convertir a CSV

# Ruta de la carpeta donde se encuentran los archivos .nc
directorio = r'C:/Users/jiahu/OneDrive/Escritorio/AI3/Bitsxm/Dades/CALIOPE/NO2'

def obtenir_dadesCALIOPE(directorio):
    # Lista para almacenar todos los DataFrames generados
    archivos = os.listdir(directorio)
    mitad = len(archivos) // 2
    lista_dataframes = []
        
            # Obtener la mitad de los archivos
              # División entera para obtener la mitad
    archivos_a_recorrer = archivos[:mitad]
        
    # Recorre todos los archivos .nc de la carpeta
    for archivo in archivos_a_recorrer:
        if archivo.endswith('.nc'):
            ruta_archivo = os.path.join(directorio, archivo)
                
            print(f"Procesando archivo: {archivo}")
                
            try:
                # 1. Abrir el archivo .nc con xarray
                dataset = xr.open_dataset(ruta_archivo)
                    
                # 2. Muestra las variables disponibles en el archivo
                print(f"Variables en {archivo}: {list(dataset.data_vars.keys())}")
                    
                # 3. Convertir todas las variables del archivo a un DataFrame
                df = dataset.to_dataframe().reset_index()

                print(df.shape)

                # 5. Convertir la columna de tiempo a datetime
                    
                df['time'] = pd.to_datetime(df['time'])

                # 6. Escoger las columnas que queremos.
                df = df.loc[:, ['time', 'lat', 'lon', 'sconcno2']]

                # 7. Agregar el DataFrame a la lista
                lista_dataframes.append(df)
                    
                # Mostrar las primeras filas del DataFrame para verificar
                print(df.head())

            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")
        
        # 8. Concatenar todos los DataFrames acumulados
    if lista_dataframes:
        df_CALIOPE = pd.concat(lista_dataframes, ignore_index=True, join='outer')
        print(f"Concatenación final exitosa. Total de filas: {df_CALIOPE.shape[0]}")
        return df_CALIOPE
    else:
        print("No se generó ningún DataFrame.")
        return pd.DataFrame()# Retorna un DataFrame vacío si no hay archivos .nc válidos

# Ejecutar la función para procesar los archivos y concatenar
sconcno2_2023122600 = obtenir_dadesCALIOPE(directorio)

# Mostrar las columnas del DataFrame concatenado
print("Columnas del DataFrame concatenado:")
print(sconcno2_2023122600.columns)
