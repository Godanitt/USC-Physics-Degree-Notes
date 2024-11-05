# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 21:58:57 2024

@author: danie
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from matplotlib.gridspec import GridSpec

def leer_datos(archivo):
    t, A = [], []
    
    with open(archivo, 'r') as file:
        for linea in file:
            # Separar los valores basados en 2 espacios
            datos = linea.split('  ')  # Usa split con 2 espacios
            if len(datos) == 2:
                t.append(float(datos[0].strip()))
                A.append(float(datos[1].strip()))
    return t,A


for i in range(9):    
    archivox1 = os.path.join('..', 'Datos','Optativo2','Datos_Desplazamiento2_DM_%02i.dat'%(i+1))
    archivox2 = os.path.join('..', 'Datos','Optativo2','Datos_CorrVel_DM_%02i.dat'%(i+1))
    archivox3 = os.path.join('..', 'Datos','Optativo2','Datos_gr_DM_%02i.dat'%(i+1))
     
    df1 = pd.read_csv(archivox1)
    df2 = pd.read_csv(archivox2)
    df3 = pd.read_csv(archivox3)
    t,X1=leer_datos(archivox1)
    t,X2=leer_datos(archivox2)
    r,X3=leer_datos(archivox3)
    
    
plt.figure()
plt.ylabel('$d_{cm}$')
plt.xlabel('t')
plt.plot(t,X1)    
plt.savefig("dcm2.pdf",dpi=300.0,bbox_inches="tight")
    
plt.figure()
plt.ylabel('$Corr_v$')
plt.xlabel('t')
plt.plot(t,X2)    
plt.savefig("Corr_vel.pdf",dpi=300.0,bbox_inches="tight")
    
    
plt.figure()
plt.ylabel('$g(r)$')
plt.xlabel('r')
plt.plot(r,X3)    
plt.savefig("gr.pdf",dpi=300.0,bbox_inches="tight")
    
    