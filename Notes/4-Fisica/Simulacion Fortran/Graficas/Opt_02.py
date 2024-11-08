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
import scipy.optimize as so

def media_e_incertidumbre(datos):
    # Convertimos a array para realizar operaciones con numpy
    datos = np.array(datos)
    
    # Calcular la media
    media = np.mean(datos)
    
    # Calcular la desviación estándar de la muestra
    desviacion_estandar = np.std(datos, ddof=1)  # ddof=1 para muestra
    
    # Calcular la incertidumbre de la media (error estándar de la media)
    incertidumbre = desviacion_estandar / np.sqrt(len(datos))
    
    return media, incertidumbre

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

def f(t,A,B):
    y = A + B*t
    return y

def regresion(x,y,f):
    sol=so.curve_fit(f,x,y)
    a,b=sol[0]
    sa,sb=np.diag(sol[1])
    return a,sa,b,sb

D1,sD1=np.array([]),np.array([])
D2,sD2=np.array([]),np.array([])

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
    a,sa,b,sb=regresion(t[150:300],X1[150:300],f)
    
    D1=np.append(D1,b/6)
    sD1=np.append(sD1,sb/6)
    integral=0
    taux=0
    for j in range(len(t)):
        integral=integral+X2[j]*(t[j]-taux)
        taux=t[j]
        
    
    D2=np.append(D2,integral/3)
    
    
    
D1m, sD1m = media_e_incertidumbre(D1)
D2m, sD2m = media_e_incertidumbre(D2)


df1 = pd.DataFrame({"$D_{dcm}$":[D1m],"$s(D_{dcm}$)":[3*sD1m],
                   "$D_{Corrv}$":[D2m],"$s(D_{Corrv})$":[3*sD2m]}) 



df2 = pd.DataFrame({"$D_{dcm}$":D1,"$D_{Corrv}$":D2})    

archivotex1 = os.path.join('..', 'Memorias','Optativo_2-Memoria','Tabla1.tex')

archivotex2 = os.path.join('..', 'Memorias','Optativo_2-Memoria','Tabla2.tex')

latex_table1 = df1.to_latex(index=False,float_format="%.4f")
latex_table2 = df2.to_latex(index=False,float_format="%.4f")
with open(archivotex1, 'w') as f:
    f.write(latex_table1)
    
latex_table2 = df2.to_latex(index=False,float_format="%.4f")
with open(archivotex2, 'w') as f:
    f.write(latex_table2)

plt.figure()
plt.ylabel('$d_{cm}$')
plt.xlabel('t')
plt.grid()
plt.plot(t,X1,color="red")    
plt.savefig("dcm2.pdf",dpi=300.0,bbox_inches="tight")
    
plt.figure()
plt.ylabel('$Corr_v$')
plt.xlabel('t')
plt.grid()
plt.plot(t,X2,color="red")    
plt.savefig("Corr_vel.pdf",dpi=300.0,bbox_inches="tight")
    
    
plt.figure()
plt.ylabel('$g(r)$')
plt.xlabel('r')
plt.grid()
plt.plot(r,X3,color="blue")    
plt.savefig("gr.pdf",dpi=300.0,bbox_inches="tight")
    
    