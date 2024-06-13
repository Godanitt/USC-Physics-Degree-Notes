# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

def fn(x,t,k,w):
    An = np.sin(w*t-x*k)
    return An

def fe(x,t,k,w):
    Ae = np.sin(w*t)*np.sin(x*k)
    return Ae

a=6

x = np.linspace(0,a,200)

t = np.linspace(0.25,1,4)

k = (2*np.pi)/6
w = (2*np.pi)/6



fig, axs = plt.subplots(2, 2)
for i in range(len(t)):
    ti = t[i]
    An = fn(x,ti,k,w)
    Ae = fe(x,ti,k,w)
    j=0
    if not(i%2==0):
        j=1
    l=0
    if i>1:
        l=1
    axs[l,j].grid(linestyle="--")    
    axs[l,j].set_title("t=%.2f s"%(t[i]))
    axs[l,j].plot(x,An,color="red",label="No estacionaria")
    axs[l,j].plot(x,Ae,color="blue",label="Estacionaria")
    

for ax in axs.flat:
    ax.set(xlabel='$r$ (m)', ylabel='$A$ (m)')
    
    
for ax in axs.flat:
    ax.label_outer()

plt.savefig("Comparacion.pdf")
    

l = [1,2,3,4,5]
x = np.linspace(0,20,200)
plt.figure()
plt.grid(True,linestyle="--")

color=["red"]

for i in l:
    y = scipy.jv(i,x)
    f=i/6
    plt.plot(x,y,label="$j_%d$"%i,color=(0.1+f,0.2+f/4,0.5))
    plt.legend()
    plt.xlim(0,21)
    plt.ylim(-0.5,1.15)
    plt.savefig("bessel1.pdf")
    

l = [1,2,3,4,5]
x = np.linspace(0,20,200)
plt.figure()
plt.grid(True,linestyle="--")


for i in l:
    y = scipy.yv(i,x)
    f=i/6
    plt.plot(x,y,label="$n_%d$"%i,color=(0.1+f,0.2+f/4,0.5))
    plt.legend()
    plt.xlim(0,21)
    plt.ylim(-1.5,0.5)
    plt.savefig("bessel2.pdf")
    