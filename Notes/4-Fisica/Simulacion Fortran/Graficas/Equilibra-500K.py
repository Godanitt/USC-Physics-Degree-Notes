# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 12:45:47 2024

@author: danie
"""
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
    x=x*100/1000
    E=np.array([Etot,Ecin,Epot])
    nombres=np.array(["Et-equilibra-500K.pdf","Ecin-equilibra-500K.pdf","Epot-equilibra-500K.pdf"])
    limites=0.0005/2
    nombre=np.array(["$E_{tot}$","$E_{cin}$","$E_{pot}$"])
    for i in range(len(E)):
    # Graficar las energías
        plt.figure(figsize=(10, 8))
        plt.plot(x, E[i], label='%s'%nombre[i], color='r',linewidth=0.25)    
    # Configuración de la gráfica
        plt.xlabel('tiempo')
        plt.ylabel('Energía')
        plt.title('Gráfico de Energía')
        plt.legend()
        plt.grid(True)
     #  plt.xlim(0,10)
        if i==0:
                plt.ylim(-575*(1+limites),-575*(1-limites))
    
    # Mostrar gráfica
        plt.savefig("%s"%nombres[i],dpi=300.0,bbox_inches="tight")
    
    
    
    

# Ejemplo de uso
archivo = os.path.join('..', 'Datos','Datos_energia_equilibracion.dat')
Etot, Ecin, Epot = leer_datos(archivo)
graficar_datos(Etot, Ecin, Epot)

Etot=np.array(Etot)
n=len(Etot)
Emedio=sum(Etot)/n

Incertidumbre=np.sqrt(sum(Etot-Emedio)/(n*(n-1)))

print("La energía media",Emedio, "con incertidumbre", Incertidumbre)