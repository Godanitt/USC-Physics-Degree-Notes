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
from tabulate import tabulate



def parabola(x, a, b, c):
    y=a+b*x+c*x**2
    return y

def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

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

def aproximaparabolas(f,u,v,maxy):
    bbox = dict(boxstyle="round", fc="0.8")
    a0,b0,c0=so.curve_fit(parabola,u,v,maxfev=100000)[0]
    s=so.curve_fit(parabola,u,v,maxfev=100000)[1]
    sb0=s[1,1]
    sc0=s[2,2]
    sb0=sb0
    sc0=sc0
    t=np.linspace(min(u),max(u))
    y=f(t,a0,b0,c0)
    plt.plot(t,y,"blue",alpha=0.8)
    plt.xlabel("$U_1$ (V)")
    plt.ylabel("I (nA)")
    plt.grid(linestyle="--")
    a=-b0/(2*c0)
    if c0<0:
        plt.annotate("$U_1$ = %.2f \nI = %.2f nA"%(a,f(a,a0,b0,c0)),
                     (a-2,f(a,a0,b0,c0)+0.075*(np.sqrt(maxy))))
    elif c0>0:
        plt.annotate("$U_1$ = %.2f \nI = %.2f nA"%(a,f(a,a0,b0,c0)),
                     (a-2,f(a,a0,b0,c0)-0.15*np.sqrt(maxy)))
    sa=np.sqrt((sb0/(c0))**2+(sc0*b0/(c0**2))**2)/2
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
        sEm1=np.sqrt((sum(E[i]-np.average(E[i])))**2/(len(E)*(len(E)-1)))
        sEm2=np.sqrt(sum(sE[i]**2)/(len(sE[i]))**2)
        sEm0=np.sqrt(sEm2**2+sEm1**2)
        sEm=np.append(sEm,sEm0)
    return Em,sEm

def longitud_onda(Em,sEm):
    l=cte.c*cte.h/(cte.e*Em)
    sl=(l/Em)*sEm
    return l,sl
