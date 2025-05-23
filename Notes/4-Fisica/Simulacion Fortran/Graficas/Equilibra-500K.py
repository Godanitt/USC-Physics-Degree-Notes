# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 12:45:47 2024

@author: danie
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from matplotlib.gridspec import GridSpec

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
def graficar_datos(Etot, Ecin, Epot,Nombre):
    gs = GridSpec(2, 3)
    x = range(len(Etot))  # Índices en el eje x
    x=np.array(x)
    x=x*100/10000
    
    E=np.array([Etot,Ecin,Epot])
    nombres=np.array(["Et-equilibra.pdf","Ecin-equilibra.pdf","Epot-equilibra.pdf"])
    limites=np.array([-575.6,-574.95])
    nombre=np.array(["$E_{tot}$","$E_{cin}$","$E_{pot}$"])
    color=np.array(["red","cornflowerblue","limegreen"])
    
    fig=plt.figure(figsize=(13, 6))
    
    ax1=fig.add_subplot(gs[:,:-1])
    ax2=fig.add_subplot(gs[0,-1])
    ax3=fig.add_subplot(gs[-1,-1])
    
    
    for i, ax in enumerate(fig.axes):
    # Graficar las energías
        
        ax.plot(x, E[i], label='%s'%nombre[i], color=color[i], marker='.',linewidth=0.3,markersize=0.1)    
    # Configuración de la gráfica
        ax.legend()
        ax.grid(True)
        if i==0:
            ax.set_ylim(-575*(1+0.025/100),-575*((1-0.025/100)))
            ax.set_ylabel('Energía')
            ax.set_xlabel('Tiempo')
        elif i==2:            
            ax.set_xlabel('Tiempo')
    # Mostrar gráfica
    plt.savefig(Nombre,dpi=300.0,bbox_inches="tight")
    
    
    
    

# Ejemplo de uso
archivo = os.path.join('..', 'Datos','Datos_energia_equilibracion-500K-1.dat')
Etot, Ecin, Epot = leer_datos(archivo)
graficar_datos(Etot, Ecin, Epot,"Et-equilibra-500K-1.pdf")

Ecin=np.array(Ecin)
Etot=np.array(Etot)
n=len(Etot)
Emedio=sum(Etot)/n
Ecmedio=sum(Ecin)/n

Incertidumbre=np.sqrt(sum(Etot-Emedio)/(n*(n-1)))
Incertidumbre2=np.sqrt(sum(Ecin-Ecmedio)/(n*(n-1)))

print("La energía media 1",Emedio, "con incertidumbre", Incertidumbre)
print("La energía cinetica 1",Ecmedio, "con incertidumbre", Incertidumbre2)
print("--------------------------------")

archivo = os.path.join('..', 'Datos','Datos_energia_equilibracion-500K-2.dat')
Etot, Ecin, Epot = leer_datos(archivo)
graficar_datos(Etot, Ecin, Epot,"Et-equilibra-500K-2.pdf")

Etot=np.array(Etot)
Ecin=np.array(Ecin)
n=len(Etot)
Emedio=sum(Etot)/n
Emedio=sum(Etot)/n
Ecmedio=sum(Ecin)/n

Incertidumbre=np.sqrt(sum(Etot-Emedio)/(n*(n-1)))
Incertidumbre2=np.sqrt(sum(Ecin-Ecmedio)/(n*(n-1)))

print("La energía media",Emedio, "con incertidumbre", Incertidumbre)
print("La energía cinetica 1",Ecmedio, "con incertidumbre", Incertidumbre2)