# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 15:57:32 2024

@author: danie
"""



import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte

from scipy.optimize import curve_fit
import scipy.constants as cte
from Efecto_fotoelectrico_Datos import I1,V1,V2,I2,I3,V3,I4,V4,I5,V5,l

def lineal(x,a,b):
    y = a+b*x
    return y


def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

def regresion_lineal(x,y):
    a,b=curve_fit(lineal,x,y,maxfev=5000)[0]
    ss=curve_fit(lineal,x,y,maxfev=5000)[1]
    sa=np.sqrt(ss[0,0])
    sb=np.sqrt(ss[1,1])
    return a,b,sa,sb

def regresion_lineal_s(x,y,sy):
    a,b=curve_fit(lineal,x,y,sigma=sy,p0=(-1.46,1240),maxfev=15000)[0]
    ss=curve_fit(lineal,x,y,sigma=sy,p0=(-1.46,1240),maxfev=15000)[1]
    sa=np.sqrt(ss[0,0])
    sb=np.sqrt(ss[1,1])
    return a,b,sa,sb


def punto(a1,b1,a2,b2,sa1,sb1,sa2,sb2):
    h=(a2-a1)/(b1-b2)
    sh=np.sqrt((sa2/(b1-b2))**2+(sa1/(b1-b2))**2+(sb1*h/(b1-b2))**2+(sb2*h/(b1-b2))**2)
    return h,sh

def corte(V,I,l,p,q,c):
    a1=np.array([])
    b1=np.array([])
    sa1=np.array([])
    sb1=np.array([])
    a2=np.array([])
    b2=np.array([])
    sa2=np.array([])
    sb2=np.array([])
    h=np.array([])
    sh=np.array([])
    
    bbox = dict(boxstyle="round", fc="0.97",alpha=0.6)
    for k in range(len(V)):
        I[k]=I[k]*10**3
        plt.figure()
        i=0
        while(I[k][i+1]<(I[k][0]+0.004*c[k]*10**3)):
            i+=1
            j=0  
        while(I[k][j+2]-I[k][j]<p[k]):
            j+=1
        a3,b3,sa3,sb3=regresion_lineal(V[k][0:i],I[k][0:i])
        a4,b4,sa4,sb4=regresion_lineal(V[k][j:],I[k][j:])
        a1=np.append(a1,a3)
        b1=np.append(b1,b3)
        sa1=np.append(sa1,sa3)
        sb1=np.append(sb1,sb3)
        a2=np.append(a2,a4)
        b2=np.append(b2,b4)
        sa2=np.append(sa2,sa4)
        sb2=np.append(sb2,sb4)
    
        h=np.append(h,punto(a1[k],b1[k],a2[k],b2[k],sa1[k],sb1[k],sa2[k],sb2[k])[0])
        sh=np.append(sh,punto(a1[k],b1[k],a2[k],b2[k],sa1[k],sb1[k],sa2[k],sb2[k])[1])    
    
        plt.figure()
        t1=np.linspace(min(V[k]),max(V[k]),10)
        t2=np.linspace(V[k][j]-0.2*q[k],max(V[k]),10)
        v1=lineal(t1,a1[k],b1[k])
        v2=lineal(t2,a2[k],b2[k])
        plt.plot(V[k],I[k],".r",label="$\lambda = %d$ nm"%(l[k]*10**9))    
        plt.plot(t1,v1,color="royalblue")
        plt.plot(t2,v2,color="blue")
        plt.xlabel("V (V)")
        plt.ylabel("I (pA)")
       # g=lineal(h[k],a1[k],b1[k])
        plt.annotate("$V_0$=%.2f"%(h[k]),(-1.5,(min(I[k])+max(I[k]))/5),bbox=bbox,alpha=0.8)
        plt.legend()
        plt.grid(True,linestyle="--")
        plt.savefig("Datos_cortes_%d.pdf"%(k+1),bbox_inches="tight")
    return h,sh,a1,a2,b1,b2,sa1,sa2,sb1,sb2

def exponencial(x,A,B,C):
    y = A*(np.exp(B*(x-C))-1)
    return y

def printea_sticks(x):
    pos=np.array([])
    nombre=np.array([])
    for i in range(8):
        pos=np.append(pos,0.0016+0.0002*i)
        nombre=np.append(nombre,"$ %.1f \cdot 10^{-3}$"%(pos[i]*10**3))
    plt.xticks(pos,nombre,fontsize=9)

def regresion_exponencial(x,y,b):
    A,B,C=curve_fit(exponencial,x,y,
                    bounds=((-np.inf, -np.inf, b[0]),(np.inf, np.inf, b[1])),
                    maxfev=50000)[0]
    ss=curve_fit(exponencial,x,y,
                    bounds=((-np.inf, -np.inf, b[0]),(np.inf, np.inf, b[1])),
                    maxfev=50000)[1]
    

    sA=np.sqrt(ss[0,0])
    sB=np.sqrt(ss[1,1])
    sC=np.sqrt(ss[2,2])
    return A,B,C,sA,sB,sC

def exponencialh(V,I,l,b):
    A=np.array([])
    B=np.array([])
    C=np.array([])
    sA=np.array([])
    sB=np.array([])
    sC=np.array([])
    for k in range(len(V)):
        I[k]=I[k]*10**3
        A0,B0,C0,sA0,sB0,sC0=regresion_exponencial(V[k], I[k],b[k])
        A=np.append(A,A0)
        sA=np.append(sA,sA0)
        B=np.append(B,B0)
        sB=np.append(sB,sB0)
        C=np.append(C,C0)
        sC=np.append(sC,sC0)
        plt.figure()
        u=np.linspace(min(V[k]),max(V[k]), 500)
        v=exponencial(u, A[k], B[k], C[k])
        plt.plot(V[k],I[k],".",label="$\lambda = %d$ nm"%(l[k]*10**9),color="red")
        plt.plot(u,v,color="blue")
        plt.grid(True,linestyle="--")
        plt.xlabel("V (V)")
        plt.ylabel("I (pA)")
        plt.plot(C0,exponencial(C0,A0,B0,C0),"1",
                 color="black",label="$V_0=C$",markersize=10.0,alpha=0.9,
                 markeredgewidth=2.0 )
        plt.plot(C0-1/B0,exponencial(C0-1/B0,A0,B0,C0),"2",
                 color="black",label="$V_0=C-1/B$",markersize=10.0,alpha=0.9,
                 markeredgewidth=2.0 )
        plt.legend()
        plt.savefig("Datos_exponencial_%d.pdf"%(k+1),bbox_inches="tight")
    return B,sB,C,sC