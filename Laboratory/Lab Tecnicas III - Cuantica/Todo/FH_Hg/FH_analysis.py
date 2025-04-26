# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:31:55 2024

@author: Fisica
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import scipy.constants as cte
import scipy.optimize as so
from Funciones import parabola, sacavalores, aproximaparabolas, energia, Emedia, longitud_onda


U2 = ["0_4","0_5","0_6","1_0", "1_5", "2_0"]
files = ["{}.csv".format(val) for val in U2]
dfs = [pd.read_csv(file, sep="\s+", decimal=",") for file in files]

colors = [(0.2,0.5,0.3), (0.3,0.6,0.3),(0.4,0.7,0.3),(0.5,0.8,0.3),(0.6,0.9,0.3),(0.7,0.99,0.3)]
labels = ["U2 = 0.4 V", 
          "U2 = 0.5 V",
          "U2 = 0.6 V",
          "U2 = 1 V",
          "U2 = 1.5 V",
          "U2 = 2 V"]

plt.figure(1)
a=np.zeros([6,5])
sa=np.zeros([6,5])
i=0
for df, color, label in zip(dfs, colors, labels):
    f=i/6
    plt.plot(df["U1/V"], df["IA/nA"],"." ,color=(0.1+f,0.16+f/3,0.6), label=label,markersize="0.5" )
    i+=1
plt.xlabel("V1 (V)")
plt.ylabel("I (nA)")
plt.legend()
plt.savefig("FH_Hg.pdf")

"""
l=0.95
extremos=np.array([[[13.85-l,13.85+l],[18.53-l,18.53+l],[23.25-l,23.25+l],[28.16-l,28.16+l],[33.14-l,33.14+l]],
[[13.85-l,13.85+l],[18.56-l,18.56+l],[23.30-l,23.30+l],[28.25-l,28.25+l],[33.22-l,33.22+l]],
[[13.92-l,13.92+l],[18.62-l,18.62+l],[23.35-l,23.35+l],[28.24-l,28.24+l],[33.22-l,33.22+l]],
[[14.07-l,14.07+l],[18.75-l,18.75+l],[23.49-l,23.49+l],[28.40-l,28.40+l],[33.40-l,33.40+l]],
[[14.32-l,14.32+l],[19.00-l,19.00+l],[23.71-l,23.71+l],[28.73-l,28.73+l],[33.58-l,33.58+l]],
[[14.44-l,14.44+l],[19.16-l,19.16+l],[23.92-l,23.92+l],[28.81-l,28.81+l],[33.79-l,33.79+l]]])
j=0
for df, color, label in zip(dfs, colors, labels):
    plt.figure()
    plt.plot(df["U1/V"], df["IA/nA"], ".r", label=label,markersize="0.5" )
    for i in range(len(extremos[j])):
        x=df["U1/V"]
        y=df["IA/nA"]
        u,v=sacavalores(extremos[j,i], x.to_numpy(), y.to_numpy())
        a0,sa0=aproximaparabolas(parabola, u, v)
        a[j,i]=a0
        sa[j,i]=sa0
    plt.savefig("Parabola-%d.pdf"%(j+1))
    j+=1


E,sE=energia(a, sa)

plt.figure(2)

Em,sEm=Emedia(E, sE)
l,sl=longitud_onda(Em, sEm)
for i in range(len(l)):
    print("Longitud de onda: %.2f +- %.2f nm"%(l[i]*10**9,sl[i]*10**9))
"""
"""
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
    a0,b0,c0=so.curve_fit(parabola,u,v,maxfev=10000)[0]
    s=so.curve_fit(parabola,u,v,maxfev=10000)[1]
    sb0=s[1,1]
    sc0=s[2,2]
    t=np.linspace(min(u),max(u))
    y=f(t,a0,b0,c0)
    plt.plot(t,y,"blue")
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
"""