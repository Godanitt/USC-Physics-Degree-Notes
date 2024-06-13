# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 17:03:43 2023

@author: danie
"""


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


###############################################################################
################################### DATOS #####################################
###############################################################################

d1=np.array([4.85,5.95,7.05,8.05,9.25,10.4,11.4,12.5,13.6,14.75,15.8,16.75,18.05,
19.05,20.2])
V1=np.array([0.016,0.196,0.006,0.163,0.0147,0.1402,0.0063,0.1455,0.0051,0.1523,0.0065,
0.1488,0.0057,0.1533,0.0058])

d2 = np.array([5.6,6.2,7.35,8.55,9.8,10.95,11.8,12.85,14.1,15.2,16,17.3,18.5])
V2 = np.array([0.222,0.139,0.216,0.0998,0.1665,0.0995,0.1944,0.1058,0.2,0.105,
0.1782,0.0998,0.185])


d3 = np.array([5.65,6.3,7.4,8.6,9.6,10.7,11.75,12.9,14.1,15.25,16,17.3,18.5,19.6])
V3 = np.array([0.189,0.155,0.199,0.112,0.145,0.106,0.156,0.115,0.164,0.113,0.145,
0.099,0.165,0.126])

datos1=np.array([d1,V1])
datos2=np.array([d2,V2])
datos3=np.array([d3,V3])

############################## CONFIGURACIONES ################################

d4 = np.array([8.9,18.2,6.9,5.8])
d5 = np.array([5.7,6.8,18,16.9])
V4 = np.array([0.093,0.223,0.264,0.117])
V5 = np.array([0.036,0.268,0.223,0.024])

datos4=np.array([d4,d5,V4,V5])


###############################################################################
################################## GRAFICOS ###################################
###############################################################################


def aproximasenos(x,y,nombre,boole):
    p=0
    if boole:
        s = 1
    if not(boole):
        s = -1
   # plt.figure()
    m = np.average(y)
    k=np.array([])
    A=np.array([])
    for i in range(len(x)):
        if not(i==len(x)-1):
            k=np.append(k,x[i+1]-x[i])  
            if y[i+1]-y[i]>0:
                A=np.append(A,y[i+1]-y[i])
    A = np.average(A)/2+p
    k = np.average(k)
    t = np.linspace(min(x),max(x),500)
    z = m - s*A*np.cos((t-min(x))*np.pi/(k))   
    print(A,(np.pi)/k,m,x[0])
   # plt.plot(t,z,color="royalblue")   
   # plt.plot(x,y,".",color="blue")
   # plt.xlabel("$d \ (cm)$")
   # plt.ylabel("$V \  (V)$")
   # plt.savefig(nombre)
    p0 = [A,(np.pi)/k,m,x[0]]
    return p0
    
p01=aproximasenos(d1,V1,"grafica1.pdf",True)  
p02=aproximasenos(d2,V2,"grafica2.pdf",False) 
p03=aproximasenos(d3,V3,"grafica3.pdf",False)      

def coseno(x,A,k,C,x0):
    y = C+A*np.cos((x-x0)*k)
    return y

def aproximasenos2(x,y,p01,nombre):
    print(p01)
    sol,dsol = so.curve_fit(coseno,x,y,p0=p01,maxfev=10000)
    print(sol)
    A,k,C,x0=sol
    t = np.linspace(min(x),max(x),500)

    z = coseno(t,A,k,C,x0)

    plt.figure()
    plt.plot(t,z,color="royalblue")
    plt.plot(x,y,".",color="blue")
    plt.xlabel("$d \ (cm)$")
    plt.ylabel("$V \  (V)$")
    plt.savefig(nombre)


aproximasenos2(d1,V1,p01,"grafica1.pdf")
aproximasenos2(d2,V2,p02,"grafica2.pdf")
aproximasenos2(d3,V3,p03,"grafica3.pdf")





###############################################################################
################################## TABLAS #####################################
###############################################################################


outfile=open("datos1.txt", 'w')
outfile.write(" \\hline \t $z_1$ ($cm$) &  $V_{1}$ (V) &  $z_2$ ($cm$) &  $V_{2}$ (V) & $z_3$ ($cm$) &  $V_{3}$ (V)   \\\ \hline \n")
for i in range(len(datos1[0])):
    if i==13:
        V2=np.append(V2,"-")
        d2=np.append(d2,"-")
        outfile.write("%.2f  \t & %.4f \t & %s  \t & %s \t & %.2f  \t & %.4f \t \\\ \n "%(d1[i],V1[i],d2[i],V2[i],d3[i],V3[i]))

    if i==14:
        V2=np.append(V2,"-")
        d2=np.append(d2,"-")        
        V3=np.append(V3,"-")
        d3=np.append(d3,"-")
        outfile.write("%.2f  \t & %.4f \t & %s  \t & %s \t & %s \t & %s \t \\\ \n "%(d1[i],V1[i],d2[i],V2[i],d3[i],V3[i]))

    if i<13:       
        outfile.write("%.2f  \t & %.4f \t & %.2f  \t & %.4f \t & %.2f  \t & %.4f \t \\\ \n "%(d1[i],V1[i],d2[i],V2[i],d3[i],V3[i]))
outfile.write("\\hline")    
outfile.close()



outfile=open("datos2.txt", 'w')
outfile.write(" \\hline \t $d_1$ ($cm$) &  $V_{1}$ (V) &  $d_2$ ($cm$) &  $V_{2}$ (V) \\\ \hline \n")
for i in range(len(d4)):
    outfile.write("%.2f  \t & %.3f \t & %.2f  \t & %.3f \\\ \n "%(d4[i],V4[i],d5[i],V5[i]))

outfile.write("\\hline")    
outfile.close()
