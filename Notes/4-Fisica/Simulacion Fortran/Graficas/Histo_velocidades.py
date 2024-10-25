# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 20:21:19 2024

@author: danie
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 

# Función para leer el archivo .dat
def leer_datos(archivo):
    x, vx, vy, vz = [], [], [], []
    
    with open(archivo, 'r') as file:
        for linea in file:
            # Separar los valores basados en 2 espacios
            datos = linea.split('  ')  # Usa split con 2 espacios
            if len(datos) == 2:
                x.append(float(datos[0].strip()))
                vx.append(float(datos[1].strip()))
    
    return x,vx

# Ejemplo de uso

# Función para graficar los datos
def graficar_datos(x, vx, vy, vz):
    vx=np.array(vx)
    vy=np.array(vy)
    vz=np.array(vz)
    plt.plot(x,vx,".",label="$v_x$",markersize=0.08)    
    plt.plot(x,vy,".",label="$v_y$",markersize=0.08)    
    plt.plot(x,vz,".",label="$v_z$",markersize=0.08)
    plt.legend(markerscale=80.0)
    plt.savefig("Velocidades_histo.pdf")
    
  #  plt.figure()
  #  plt.plot(x,vx*vx,color="red",label="$v_x^2$",markersize=0.08)

  #  plt.legend(markerscale=80.0)
    
    
# Ejemplo de uso
archivox = os.path.join('..', 'Datos','Histogramas_vx.dat')
archivoy = os.path.join('..', 'Datos','Histogramas_vy.dat')
archivoz = os.path.join('..', 'Datos','Histogramas_vz.dat')
x, vx = leer_datos(archivox)
x, vy = leer_datos(archivoy)
x, vz = leer_datos(archivoz)
graficar_datos(x, vx, vy, vz)