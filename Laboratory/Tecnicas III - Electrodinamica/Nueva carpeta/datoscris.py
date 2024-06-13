

import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so
import sympy as symp
import scipy.special as scipy
import scipy.constants as cte
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

V1=np.array([2790, 2336, 1911, 1415, 934, 438])
D1=np.array([15.6, 4.9, 16.9, 4.9, 18.5, 2.3])

V2=np.array([2822, 2331, 1878, 1382, 919])
D2=np.array([5.6, 17.0, 4.8, 17.9, 3.4])


def aproximasenos(x,y,nombre):
    plt.figure()
    ymedia=y
    if len(y)%2==1:
        ymedia=y[0:(len(y)-1)]
    m = np.average(ymedia)
    k=np.array([])
    A=np.array([])
    for i in range(len(x)):
        if not(i==len(x)-1):
            k=np.append(k,x[i+1]-x[i])  
            if y[i+1]-y[i]>0:
                A=np.append(A,y[i+1]-y[i])
    A = np.average(A)/2
    k = np.average(k)
    t = np.linspace(min(x),max(x),500)
    z = m - A*np.cos((t-min(x))*np.pi/(k))  
    
    plt.plot(t,z,color="royalblue")   
    plt.plot(x,y,".",color="blue")
    plt.xlabel("$d \ (cm)$")
    plt.ylabel("$V \  (V)$")
    plt.savefig(nombre)
    
    p01 = [A,(np.pi)/k,m,x[0]]
    return p01
    
p01=aproximasenos(V1,D1,"hola1.pdf")
p02=aproximasenos(V2,D2,"hola2.pdf")
    

def coseno(x,A,k,C,x0):
    y = C+A*np.cos((x-x0)*k)
    return y

def aproximasenos2(x,y,p01,nombre):
    print("p01=",p01)
    sol,dsol = so.curve_fit(coseno,x,y,p0=p01,maxfev=200)
    print("sol=",sol)
    A,k,C,x0=sol
    t = np.linspace(min(x),max(x),500)

    z = coseno(t,A,k,C,x0)

    plt.figure()
    plt.plot(t,z,color="royalblue")
    plt.plot(x,y,".",color="blue")
    plt.xlabel("$d \ (cm)$")
    plt.ylabel("$V \  (V)$")
    plt.savefig(nombre)


aproximasenos2(V1,D1,p01,"grafica1.pdf")
aproximasenos2(V2,D2,p02,"grafica2.pdf")

    
    
    