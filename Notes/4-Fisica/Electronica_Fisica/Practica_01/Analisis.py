import numpy as np
import pandas as pd

def leer_archivo_txt(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        lineas = f.readlines()
    
    datos = {}  # Diccionario para almacenar las variables
    clave_actual = None
    valores_temp = []  # Lista temporal para almacenar los datos

    for linea in lineas:
        linea = linea.strip()
        
        # Si la línea está vacía, se ignora
        if not linea:
            continue

        # Si la línea contiene una etiqueta (nombre de la variable)
        if not linea[0].isdigit() and not linea[0] == "-":
            # Si ya hay datos en la clave anterior, los almacenamos
            if clave_actual and valores_temp:
                datos[clave_actual] = np.array(valores_temp)
                valores_temp = []
            
            clave_actual = linea  # Guardamos la nueva clave
        else:
            # Convertimos la línea en dos números flotantes (posición y variable)
            try:
                valores_temp.append([float(x) for x in linea.split()])
            except ValueError:
                print(f"Error al procesar la línea: {linea}")

    # Guardar el último conjunto de datos
    if clave_actual and valores_temp:
        datos[clave_actual] = np.array(valores_temp)
    
    # Convertir los datos a un DataFrame
    df = pd.DataFrame()
    for clave, valores in datos.items():
        posiciones = valores[:, 0]
        valores_variable = valores[:, 1]
        df[clave] = pd.Series(valores_variable, index=posiciones)
    
    return datos, df

# Ejemplo de uso
nombre_archivo = "datos.txt"  # Cambia esto por el nombre real del archivo
datos_np, datos_df = leer_archivo_txt(nombre_archivo)

