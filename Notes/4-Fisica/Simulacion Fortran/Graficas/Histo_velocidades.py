# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 20:21:19 2024

@author: danie
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from scipy.constants import *
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

def fv(T,v):
    k=1
    fv=np.sqrt(1/(2*np.pi*k*T))*np.exp(-v**2/(2*k*T))
    return fv
# Función para graficar los datos
def graficar_datos(x, vx, vy, vz,nombre,Ecin,C):
    k=1
    T=2*Ecin/((1500-3)*k)
    print(T)
    
    x=np.array(x)
    vx=np.array(vx)
    vy=np.array(vy)
    vz=np.array(vz)
    plt.figure()
    plt.plot(x,vx,".",label="$v_x$",markersize=0.08) 
    plt.plot(x,vy,".",label="$v_y$",markersize=0.08)    
    plt.plot(x,vz,".",label="$v_z$",markersize=0.08)
    plt.plot(x,fv(T,x)*C,color="black",linestyle="--",linewidth=0.8,label="T=%.3f"%T)
    plt.legend(markerscale=80.0)
    plt.savefig(nombre,dpi=300.0,bbox_inches="tight")
    
  #  plt.figure()
  #  plt.plot(x,vx*vx,color="red",label="$v_x^2$",markersize=0.08)

  #  plt.legend(markerscale=80.0)
    
    
# Ejemplo de uso
archivox = os.path.join('..', 'Datos','Histogramas_vx_1.dat')
archivoy = os.path.join('..', 'Datos','Histogramas_vy_1.dat')
archivoz = os.path.join('..', 'Datos','Histogramas_vz_1.dat')
x, vx = leer_datos(archivox)
x, vy = leer_datos(archivoy)
x, vz = leer_datos(archivoz)
graficar_datos(x, vx, vy, vz,"Velocidades_histo_1.pdf",1095,17120)

archivox = os.path.join('..', 'Datos','Histogramas_vx_2.dat')
archivoy = os.path.join('..', 'Datos','Histogramas_vy_2.dat')
archivoz = os.path.join('..', 'Datos','Histogramas_vz_2.dat')
x, vx = leer_datos(archivox)
x, vy = leer_datos(archivoy)
x, vz = leer_datos(archivoz)
graficar_datos(x, vx, vy, vz,"Velocidades_histo_2.pdf",1090,18120)