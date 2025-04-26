   
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress
from scipy.optimize import curve_fit

# Definición de la función lineal

def lineal(x,a,b):
    y=a*x-b
    return y

def campo_magnetico(I):
    c=55.1
    a=2*1350/np.pi
    b=0.56*np.tan((1500/2-c)/a)
    print(a,b,c)
    B=c+a*np.arctan(I/b)
    return B


def rational_func(x, a2, a1, a0, b1, b0):
    return (a2*x**2 + a1*x + a0) / (b1*x + b0)

def fit_rational(x, y):
    # Valores iniciales razonables para los parámetros
    p0 = [1, 1, 1, 1, 1]
    
    # Ajuste con curve_fit
    popt, _ = curve_fit(rational_func, x, y, p0=p0)
    
    return popt  # Devuelve los coeficientes ajustados


def evaluate_rational(x, params):
    a2, a1, a0, b1, b0 = params
    return rational_func(x, a2, a1, a0, b1, b0)

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
j=[1,1,1,1,1,1]
for nombre_hoja, df in sheets.items():
    print(nombre_hoja)
    datos[nombre_hoja] = np.array(df.values)
    
    Nombres=df.columns
    
    # Realizar regresión lineal para las hojas 2,3,4,5
    if nombre_hoja in ["Correcion Espuria", "Medida 1", "Medida 2", "Medida 3", "Medida 4"]:
        x = datos[nombre_hoja][:, 0]  # Primera columna
        y = datos[nombre_hoja][:, j[count]]  # Segunda columna
       
        
        # Crear gráfico y guardar
        if (count==2):
            y=y-lineal(x,a0,b0)
            
            
        if (count>2):
            z = datos[nombre_hoja][:,2]
            z=np.array([ lineal(z[0],a0,b0)   ]*len(y))
            print(z)
            y = y - z 
            x = evaluate_rational(x, params)

        if (not(count==0)):
            print(linregress(x,y))
            result = linregress(x, y)
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            itercept_err=result.intercept_stderr
            resultados.append([nombre_hoja, slope, std_err, intercept,itercept_err])
        
        if (count==1):
            a0,b0=slope,intercept
            
        # Ajuste de regresión lineal
            
            
        # Guardar los resultados en la lista
        
        plt.figure()

        if (not(count==0)):
            plt.plot(x, slope*x + intercept, color="red", label=f"Ajuste: y = {slope:.7f}x + {intercept:.3f}")
          
        plt.scatter(x, y, label="Datos",color="blue")
        plt.xlabel(Nombres[0])
        plt.ylabel(Nombres[j[count]])
        if (count>2):
            plt.xlabel("B (mT)")
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