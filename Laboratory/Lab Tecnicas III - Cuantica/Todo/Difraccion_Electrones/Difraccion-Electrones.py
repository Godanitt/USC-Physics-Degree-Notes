# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 11:13:03 2024

@author: danie
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte

def londa1(V):
    londa = (cte.h)/(np.sqrt(2*cte.m_e*cte.e*V))
    return londa

def londa2(d,D,L):
    londa = (d*D)/(2*L)
    return londa

def f(x,a,b):
    y = a + b*x
    return y

def d(L,k):
    d = (2*L*cte.h)/(k*np.sqrt(2*cte.m_e*cte.e)) 
    return d

###############################################################################
#################################### DATOS ####################################
###############################################################################

d1=2.13*10**(-10)
d2=1.23*10**(-10)
L=13.5*(10**(-2))

V=np.array([3,3.5,4,4.5,5])*10**3

D1v=np.array([[28.60,27.30,27.30,26.95],[25.50,26.09,26.15,26.60],[23.54,24.04,24.48,23.82],[22.73,22.63,23.03,23.72],[21.06,21.32,21.20,21.08]]) # En mm
D2v=np.array([[48.85,49.56,50.33,49.51],[46.54,46.12,46.67,45.87],[42.75,42.63,42.91,43.51],[39.70,41.25,39.29,39.89],[37.86,37.90,38.33,38.18]]) # En mm

sD1=np.sqrt(0.01**2+2**2) # Incertidumbre aparto electrico + personal # mm
sD2=np.sqrt(0.01**2+2**2) # Incertidumbre aparto electrico + personal # mm

###############################################################################
################################## RESULTADOS #################################
###############################################################################

# Parte 1: calculo de longitudes de onda experimentales

D1=np.array([])
D2=np.array([])

for i in range(len(D1v)):
    D1=np.append(D1,np.average(D1v[i])*10**(-3))
    D2=np.append(D2,np.average(D2v[i])*10**(-3))

l1=np.array([])
l2=np.array([])
for i in range(len(D1)):
    l1=np.append(l1,londa2(d1,D1[i],L))
    l2=np.append(l2,londa2(d2,D2[i],L))
    
# Parte 2: calculo de longitudes de onda teoricas


l1t=np.array([])
l2t=np.array([])
for i in range(len(V)):
    l1t=np.append(l1t,londa1(V[i]))
    l2t=np.append(l2t,londa1(V[i]))
    
diferencia1=l1-l1t
diferencia2=l2-l2t

# Parte 3: determinacion de las distancias d1 y d2 experimentalmente

sqrtV =(np.sqrt(V))**(-1)
a0,k1=curve_fit(f,sqrtV,D1,maxfev=30000)[0]
a0,k2=curve_fit(f,sqrtV,D2,maxfev=30000)[0]

d1exp=d(L,k1)
d2exp=d(L,k2)
