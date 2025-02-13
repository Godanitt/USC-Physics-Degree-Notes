   
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress

# Definición de la función lineal

def lineal(x,a,b):
    y=a*x-b
    return y

# Ruta del archivo ODS
ruta_archivo = "Hall_Datos.ods"

# Leer todas las hojas del archivo
sheets = pd.read_excel(ruta_archivo, sheet_name=None, engine="odf")

# Diccionario para almacenar los datos de cada hoja en arrays
datos = {}
resultados = []

# Crear carpeta para las gráficas
ruta_graficas = "./Graficas"
os.makedirs(ruta_graficas, exist_ok=True)

# Procesar cada hoja y almacenarla en arrays separados
count=0
j=[1,1,2,2,2]
for nombre_hoja, df in sheets.items():
    print(nombre_hoja)
    datos[nombre_hoja] = np.array(df.values)
    
    Nombres=df.columns
    
    # Realizar regresión lineal para las hojas 2,3,4,5
    if nombre_hoja in ["Correcion Espuria", "Medida 1", "Medida 2", "Medida 3", "Medida 4"]:
        x = datos[nombre_hoja][:, 0]  # Primera columna
        y = datos[nombre_hoja][:, j[count]]  # Segunda columna
        
        # Ajuste de regresión lineal
        result= linregress(x, y)
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        itercept_err=result.intercept_stderr
        
        # Guardar los resultados en la lista
        resultados.append([nombre_hoja, slope, std_err, intercept,itercept_err])
        
        # Crear gráfico y guardar
        plt.figure()
        plt.scatter(x, y, label="Datos")
        plt.plot(x, slope*x + intercept, color="red", label=f"Ajuste: y = {slope:.3f}x + {intercept:.3f}")
        plt.ylabel(Nombres[0])
        plt.xlabel(Nombres[j[count]])
        plt.legend()
        plt.title(f"Regresión Lineal - {nombre_hoja}")
        plt.savefig(f"{ruta_graficas}/{nombre_hoja}.pdf")
        plt.close()
    count+=1    

# Guardar resultados en un nuevo archivo ODS
ruta_resultados = "Resultados.ods"
df_resultados = pd.DataFrame(resultados, columns=["Hoja", "Pendiente", "Error Pendiente", "Intercepto","Error Intercepto"])
df_resultados.to_excel(ruta_resultados, index=False, engine="odf")

# Acceso a los datos de cada hoja (ejemplo de impresión)
for nombre, array in datos.items():
    print(f"Datos de {nombre}:")
    print(array)
    print("-" * 40)

# Cosas que faltan: hacer que la primera regresión corrija el resultado de las posteriores, relacionar la pendiente
#   con el valor de n y su carga (aunque eso se anotará en otro sitio, supongo).