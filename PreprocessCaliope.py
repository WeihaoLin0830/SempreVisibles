#pip install xarray netCDF4 pandas
import os
import xarray as xr  # Más eficiente que netCDF4
import pandas as pd  # Para convertir a CSV

# Ruta de la carpeta donde se encuentran los archivos .nc

""" def obtenir_dadesCALIOPE(directorio):
    # Lista para almacenar todos los DataFrames generados
    archivos = os.listdir(directorio)
    mitad = len(archivos) // 2
    lista_dataframes = []
        
            # Obtener la mitad de los archivos
              # División entera para obtener la mitad
    archivos_a_recorrer = archivos[:31]
        
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
        df_CALIOPE = pd.concat(lista_dataframes, ignore_index=True, join='outer', axis=0)
        print(f"Concatenación final exitosa. Total de filas: {df_CALIOPE.shape[0]}")
        return df_CALIOPE
    else:
        print("No se generó ningún DataFrame.")
        return pd.DataFrame()# Retorna un DataFrame vacío si no hay archivos .nc válidos

# Ejecutar la función para procesar los archivos y concatenar
datos_caliope = obtenir_dadesCALIOPE(directorio)
datos_caliope.to_csv('C:/Users/jiahu/OneDrive/Escritorio/AI3/Bitsxm/Dades/CALIOPE/NO2/NO30.csv', index=False)

# Mostrar las columnas del DataFrame concatenado
print("Columnas del DataFrame concatenado:")
print(datos_caliope.columns)
print(datos_caliope.shape)
 """

import os
import pandas as pd
import xarray as xr

def extract_random_rows_v3(nc_data, num_rows=1000):
    """ Extraer 1000 filas aleatorias de las columnas time, lat, lon y sconcno2. """
    # Convertir el dataset de xarray a DataFrame y seleccionar solo las columnas necesarias
    df = nc_data[['time', 'lat', 'lon', 'sconcno2']].to_dataframe().reset_index()

    # Seleccionar 1000 filas aleatorias
    if len(df) > num_rows:
        sampled_df = df.sample(n=num_rows, random_state=42).reset_index(drop=True)
    else:
        sampled_df = df

    return sampled_df


# Ruta de la carpeta donde se encuentran los archivos .nc
directorio = r'C:/Users/jiahu/OneDrive/Escritorio/AI3/Bitsxm/Dades/CALIOPE/NO2/'

# Listar los archivos .nc de la carpeta
archivos = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.nc')]

# Lista para almacenar todos los DataFrames generados
lista_dataframes = []

# Recorre todos los archivos .nc de la carpeta
for archivo in archivos:
    try:
        ruta_archivo = os.path.join(directorio, archivo)
        print(f"Procesando archivo: {archivo}")
        
        # Abrir el archivo NetCDF
        nc_data = xr.open_dataset(ruta_archivo)
        
        # Extraer 1000 filas aleatorias
        sampled_data = extract_random_rows_v3(nc_data)
        
        # Agregar el DataFrame a la lista
        lista_dataframes.append(sampled_data)
        
        # Cerrar el dataset para liberar memoria
        nc_data.close()
        
        print(f"Archivo procesado correctamente: {archivo} | Filas extraídas: {sampled_data.shape[0]}")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")

# Concatenar todos los DataFrames
data_final = pd.concat(lista_dataframes, ignore_index=True)
data_final = data_final.drop(columns=['x', 'y', 'lev'])
# Guardar el DataFrame final como CSV
output_path = 'C:/Users/jiahu/OneDrive/Escritorio/AI3/Bitsxm/Dades/CALIOPE/NO2/NO2_final.csv'
data_final.to_csv(output_path, index=False)
print(f"Archivo CSV guardado en: {output_path}")

# Mostrar las primeras filas para verificar
print("Vista previa de los primeros registros:")
print(data_final.head())

# Mostrar información general del DataFrame
print(f"Total de filas: {data_final.shape[0]}")
print(f"Columnas del DataFrame: {data_final.columns}")

# Mostrar una vista previa de los primeros 5 registros de cada conjunto
""" import ace_tools as tools
tools.display_dataframe_to_user(name="Sampled Data from File 1 (Final V2)", dataframe=sampled_data_1_final_v2.head())
 """