# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 18:26:02 2024

@author: danie
"""


import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as so
import sympy as symp
import scipy.special as scipy
import scipy.constants as cte

def Bode2(s,Q,w0,a0,a1,a2,a):
    H = np.log10(np.sqrt((a0**2-a2*s**2)**2+(a1*s)**2)/np.sqrt((w0**2-s**2)**2+((w0/Q)*s)**2))
    return H

def f(x,a,b,c,d,e,f):
    y=a+b*x
    return y

def plotea(Q,w0,a0,a1,a2,a):
    nombres=np.array(["Pasa baja","Pasa banda","Pasa alta","Pasa Alta Notch","Notch","Pasa Baja Notch"])
    w=np.linspace(1,100,2000)
    for i in range(len(a0)):
        plt.figure()
        for j in range(len(Q)):
            f=j/5
            color=(0.95-f,0.3-f/3,0.4)
            plt.plot(w,Bode2(w, Q[j], w0[j], a0[i], a1[i], a2[i],a),label="Q = %d"%(Q[j]),color=color)
            
        plt.xscale("log")    
        plt.xlabel("$\omega$")
        plt.title("%r"%nombres[i])
        plt.legend()
        plt.savefig("Bode_%i.pdf"%(i+1),dpi=300,bbox_inches="tight")

# Definicion de datos

a0=np.array([1,0,0,9,10,11])
a1=np.array([0,1,0,0,0,0])
a2=np.array([0,0,1,1,1,1])
a=100
w0=10*np.array([1,1,1,1,1,1])
Q=10*np.array([0.25,0.5,1,2,10])

# Ploteamos

plotea(Q, w0, a0, a1, a2, a)