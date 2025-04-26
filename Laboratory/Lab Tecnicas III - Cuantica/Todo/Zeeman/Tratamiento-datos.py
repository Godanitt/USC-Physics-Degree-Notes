# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:26:47 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cte
from scipy.optimize import curve_fit
from Zeeman_Normal import R1,R2,R3,R4,R5,R6,B


def magBohr(b,mu,t):
    muB=b*(cte.h*cte.c)/(t*mu)
    return muB

def lineal(x,b):
    y = b*x
    return y

def regresion_lineal(x,y):
    b3=curve_fit(lineal,x,y,maxfev=5000)[0]
    return b3

def deltas(R):
    RM=np.array([])
    for i in range(len(R)-1):
        RM=np.append(RM,abs(R[i+1]**2-R[i]**2))
    return np.average(RM)

def Deltas(Ri,Ro):
    RM=np.array([])
    for i in range(len(Ri)):
        RM=np.append(RM,abs(Ri[i]**2-Ro[i]**2))
    return np.average(RM)

def plotea(x,y,b3):
    plt.plot(x,y,".",color="red")
    u=np.linspace(min(x),max(x),20)
    v=lineal(u,b3)
    plt.plot(u,v,color="blue")

t = 0.003
mu=np.array([1.4560*2,1.4519])

#%%

delta=np.zeros([len(B),2])
for i in range(len(B)):
    delta[i]=np.array([deltas(R1[i]),deltas(R2[i])])
    
Delta=np.zeros([len(B),1])
for i in range(len(B)):
    Delta[i]=np.array([Deltas(R1[i],R2[i])])

b=np.array([])
for i in range(len(delta[0])):
    plt.figure()
    y=delta[:,i]/Delta[:,0]
    x=B
    b1=regresion_lineal(x, y)
    plotea(x, y, b1)
    b=np.append(b,b1)

muB=magBohr(b, mu[0], t)
print(muB)
muBm=np.average(muB)
print(muBm)


