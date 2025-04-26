# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:32:03 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
"""
def focal(s,sprima,d) :
    f=[0]*len(s)
    for i in range(len(s)):
        f[i] = -(1/(-sprima[i]+d[i])-1/(d[i]-s[i]))**(-1)
    return np.array(f)
"""
def lineal(x,a,b):
    y=a+b*x
    return y

def distancia(x_0,x):
    y = abs(x_0-x)
    return y

def incertidumbre(x):
    sx=sum(x**2-(np.average(x))**2)/len(x)
    return sx



imagen=np.array([33.4,19.9,35.7,59.8,24.4,15.0,27.6,39,46,31.4])
lente=np.array([50,36.5,52,75.3,40.2,32.0,44.6,56.2,62.9,48.5])

a,b=curve_fit(lineal,imagen,lente,maxfev=10000)[0]

focal1=a
focal=lente-imagen
print('focal= %.2f'%np.average(focal))


