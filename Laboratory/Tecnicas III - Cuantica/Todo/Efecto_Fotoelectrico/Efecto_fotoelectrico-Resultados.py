# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:00:07 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from Efecto_fotoelectrico import I1,V1,V2,I2,I3,V3,I4,V4,I5,V5,l

def lineal(x,a,b):
    y = a+b*x
    return y

def regresion_lineal(x,y):
    a3,b3=curve_fit(lineal,x,y,maxfev=5000)[0]
    return a3,b3

def corte(u):
    corte=(u[2]-u[0])/(u[1]-u[3])
    return corte

def plotea(x,y,a3,b3):
    u=np.linspace(min(x),max(x),20)
    v=lineal(u,a3,b3)
    plt.plot(u,v,color="blue")
    

def recta(V,I,p):
    plt.figure()
    i=0
    print(I[i+1]<I[0]+0.004)
    while(I[i+1]<(I[0]+0.004)):
        i+=1
    j=0  
    while(I[j+2]-I[j]<p):
        j+=1
    a1,b1=regresion_lineal(V[0:i],I[0:i])
    a2,b2=regresion_lineal(V[j:],I[j:])
    plt.plot(V,I,".",color="red")
    plotea(V[:],I[:],a1,b1)
    plotea(V[j:],I[j:],a2,b2)
    plt.ylim(min(I)-abs(0.5*I[0]),max(I)+0.2*I[len(I)-1])
    print("a1=",a1,"a2=",a2,"\nb1=",b1,"b2=",b2)
    print("-"*50)
    return np.array([a1,b1,a2,b2])

p=0.002
h1=recta(V1,I1,p)
h2=recta(V2,I2,p)
h3=recta(V3,I3,p)
h4=recta(V4,I4,p)
p=0.002
h5=recta(V5,I5,p)

h=np.array([h1,h2,h3,h4,h5])
h=h[:]
cortes=np.array([])
for i in range(len(h)):
    cortes=np.append(cortes, corte(h[i]))    

plt.figure()
l=l[:]
plt.plot(l*10**9,abs(cortes),".",color="red")

plt.figure()
plt.plot(1/(l*10**9),abs(cortes),".",color="red")
a0,b0=regresion_lineal(1/(l*10**9), abs(cortes))
plotea(1/(l*10**9),abs(cortes),a0,b0)
plt.xlabel("$1/\lambda \ (nm^{-1})$")
plt.ylabel("$V \ (V)$")
plotea(1/(l*10**9), abs(cortes), a0, b0)

h=b0*10**(-9)*cte.e/cte.c

print("h=",h)
"""
nombre=["s","p","d","f"]
for i in range(len(nombre)):
    print("l=%d & %s & %d"%(i,nombre[i],2*(2*i+1)))
    """