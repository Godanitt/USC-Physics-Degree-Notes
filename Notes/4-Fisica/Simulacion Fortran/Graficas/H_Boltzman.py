# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 13:21:40 2024

@author: danie
"""



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from matplotlib.gridspec import GridSpec

# Función para leer el archivo .dat
def leer_datos(archivo):
    t, Hx, Hy, Hz = [], [], [], []
    
    with open(archivo, 'r') as file:
        for linea in file:
            # Separar los valores basados en 2 espacios
            datos = linea.split('  ')  # Usa split con 2 espacios
            if len(datos) == 4:
                t.append(float(datos[0].strip()))
                Hx.append(float(datos[1].strip()))
                Hy.append(float(datos[2].strip()))
                Hz.append(float(datos[3].strip()))
    
    return t,Hx,Hy,Hz

# Ejemplo de uso

# Función para graficar los datos
def graficar_datos(x, Hx, Hy, Hz,nombre1,nombre2):
    gs = GridSpec(3, 1)
    H=np.array([Hx,Hy,Hz])
    
    nombre=np.array(["$H_x$","$H_y$","$H_z$"])
    color=np.array(["red","blue","green"])
    
    fig=plt.figure(figsize=(12, 12))
    
    ax1=fig.add_subplot(gs[-1,0])
    ax2=fig.add_subplot(gs[1,0])
    ax3=fig.add_subplot(gs[0,0])
    
    for i, ax in enumerate(fig.axes):
    # Graficar las energías
        
        ax.plot(t, H[i], label='%s'%nombre[i], color=color[i], marker='.',linewidth=0.2,markersize=0.08)    
    # Configuración de la gráfica
        ax.legend(loc='upper right', fontsize='x-large',markerscale=60.0)
        ax.grid(True)
        ax.set_ylabel('H(t)')
        ax.set_title(nombre[i])
        if i==0:
            ax.set_xlabel('t')
            
    # Mostrar gráfica
    plt.savefig(nombre1,dpi=300.0,bbox_inches="tight")
    
    fig=plt.figure(figsize=(12,4))

    plt.plot(t,(H[0]+H[1]+H[2])/3, label='H(t)', color="orange", marker='.',linewidth=0.2,markersize=0.08)    

    plt.legend(loc='upper right', fontsize='x-large',markerscale=60.0)
    plt.ylabel('H(t)')
    plt.xlabel('t')
    plt.savefig(nombre2,dpi=300.0,bbox_inches="tight")
    

# Ejemplo de uso
archivox = os.path.join('..', 'Datos','Funcion_H_1.dat')
t, Hx,Hy,Hz = leer_datos(archivox)
graficar_datos(t, Hx, Hy, Hz,"H_Boltzmann_xyz_1.pdf","H_Boltzmann_1.pdf")

Hx,Hy,Hz=np.array(Hx),np.array(Hy),np.array(Hz)
H=(Hx+Hy+Hz)/3
Hmedio=sum(H)/len(H)
n=len(H)

Incertidumbre=np.sqrt(sum((H-Hmedio)**2)/(n-1))
print("DH1",Incertidumbre)

archivox = os.path.join('..', 'Datos','Funcion_H_2.dat')
t, Hx,Hy,Hz = leer_datos(archivox)
graficar_datos(t, Hx, Hy, Hz,"H_Boltzmann_xyz_2.pdf","H_Boltzmann_2.pdf")

Hx,Hy,Hz=np.array(Hx),np.array(Hy),np.array(Hz)
H=(Hx+Hy+Hz)/3
Hmedio=sum(H)/len(H)
n=len(H)

Incertidumbre=np.sqrt(sum((H-Hmedio)**2)/(n-1))
print("DH1",Incertidumbre)
