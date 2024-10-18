import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 

# Función para leer el archivo .dat
def leer_datos(archivo):
    Etot, Ecin, Epot = [], [], []
    
    with open(archivo, 'r') as file:
        for linea in file:
            # Separar los valores basados en 2 espacios
            datos = linea.split('  ')  # Usa split con 2 espacios
            if len(datos) == 3:
                Etot.append(float(datos[0].strip()))
                Ecin.append(float(datos[1].strip()))
                Epot.append(float(datos[2].strip()))
    
    return Etot, Ecin, Epot

# Ejemplo de uso

# Función para graficar los datos
def graficar_datos(Etot, Ecin, Epot):
    x = range(len(Etot))  # Índices en el eje x
    x=np.array(x)
    x=x*20/1000
    plt.figure(figsize=(10, 6))
    E=np.array([Etot,Ecin,Epot])
    nombres=np.array(["Et-equilibra.pdf","Ecin-equilibra.pdf","Epot-equilibra.pdf"])
    limites=np.array([-575.6,-574.95])
    nombre=np.array(["$E_{tot}$","$E_{cin}$","$E_{pot}$"])
    for i in range(len(E)):
    # Graficar las energías
        plt.figure()
        plt.plot(x, E[i], label='%s'%nombre[i], color='r', marker='.')    
    # Configuración de la gráfica
        plt.xlabel('tiempo')
        plt.ylabel('Energía')
        plt.title('Gráfico de Energía')
        plt.legend()
        plt.grid(True)
        if i==0:
            plt.ylim(-575.6,-574.95)
    
    # Mostrar gráfica
        plt.savefig("%s"%nombres[i],dpi=300.0,bbox_inches="tight")
    
    
    
    

# Ejemplo de uso
archivo = os.path.join('..', 'Datos','Datos_energia_equilibracion.dat')
Etot, Ecin, Epot = leer_datos(archivo)
graficar_datos(Etot, Ecin, Epot)