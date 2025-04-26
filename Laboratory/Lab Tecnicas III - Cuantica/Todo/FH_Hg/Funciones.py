# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:15:55 2024

@author: danie
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import scipy.constants as cte
import scipy.optimize as so


def parabola(x, a, b, c):
    y=a+b*x+c*x**2
    return y

def sacavalores(extremos,x,y):
    i=0
    j=0
    while(x[i]<extremos[1]):
        while(x[j]<extremos[0]):
            j+=1
        i+=1
    m=i
    n=j
    u=x[n:m]
    v=y[n:m]    
    return u,v

def aproximaparabolas(f,u,v):
    a0,b0,c0=so.curve_fit(parabola,u,v,maxfev=100000)[0]
    s=so.curve_fit(parabola,u,v,maxfev=100000)[1]
    sb0=s[1,1]
    sc0=s[2,2]
    sb0=np.sqrt(sb0)
    sc0=np.sqrt(sc0)
    t=np.linspace(min(u),max(u))
    y=f(t,a0,b0,c0)
    plt.plot(t,y,"blue",alpha=0.8)
    plt.xlabel("$U_2$ (V)")
    plt.ylabel("I (nA)")
    a=-b0/(2*c0)
    sa=np.sqrt((sb0/(2*c0))**2+(sc0*b0/(2*c0**2))**2)
    return a,sa

def energia(a,sa):
    E=np.zeros([len(a),len(a[0])-1])
    sE=np.zeros([len(a),len(a[0])-1])
    for i in range(len(a)):
        for j in range(len(a[0])-1):
            E[i,j]=a[i,j+1]-a[i,j]
            sE[i,j]=np.sqrt(sa[i,j+1]**2+sa[i,j]**2)
    return E,sE

def Emedia(E,sE):
    Em=np.array([])
    sEm=np.array([])
    for i in range(len(E)):
        Em=np.append(Em,np.average(E[i]))
        sEm=np.append(sEm,np.average(sE[i]))
    return Em,sEm

def longitud_onda(Em,sEm):
    l=cte.c*cte.h/(cte.e*Em)
    sl=(l/Em)*sEm
    return l,sl