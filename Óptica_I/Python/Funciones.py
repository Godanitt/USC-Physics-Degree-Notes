# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:50:13 2023

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


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Creamos la superficie a ser representada 

X = np.arange(-2, 2, 0.08)
Y = np.arange(-2, 2, 0.08)
X, Y = np.meshgrid(X, Y)
r = np.sqrt(X**2 + Y**2)
theta = np.arctan(Y/(X))

I = 1
Z = I*(np.cos(theta)/(r+1))**2 


surf = ax.plot_surface(X, Y, Z, rstride=1, cstride = 1,cmap=cm.winter_r, linewidth=2)

plt.title("$I = I_0 sen^2 (\\theta)/ R^2$")
plt.xlabel("y")
plt.ylabel("x")

ax.set_zlim(0, 1)

plt.savefig("Irradiancia.pdf")

# Figura para la seccion eficaz

f, (ax2,ax1) = plt.subplots(1, 2, figsize=(12,8))

def secc2(w,w0,G):
    sig=(G)/(4*((w-w0)**2+(G/2)**2))
    return sig

G=[2,4,6,8]
w0=5000
x=np.linspace(4985,5015,1000)
for i in range(len(G)):
    y2=secc2(x,5000,G[i])
    ax2.plot(x,y2,label="$\\Gamma=%d $"%G[i],linewidth=3.0,color=(0.4+0.20*i,0.5+0.06*i,1))
    
ax2.legend(fontsize=15.0)    
ax2.set_xlabel("$\omega \ (\mathrm{rad}/s)$")
ax2.set_xlim(4985,5015)

x=np.linspace(4985,5015,1000)
y2=secc2(x, 5000, G[0])
ax1.plot(x,y2,label="$\\Gamma=%d $"%G[0],linewidth=3.0,color=(0.4,0.5,1))
    
ax1.legend(fontsize=12.0)    
ax1.set_xlabel("$\omega \ (\mathrm{rad}/s)$")
ax1.set_xlim(4992,5008)

a,b=secc2(w0-G[0]/2, w0, G[0]),secc2(w0+G[0]/2, w0, G[0])

t=np.linspace(w0-G[0]/2,w0+G[0]/2,2)
ax1.plot(t,[a,b],linewidth=2.0,linestyle="--",color=(0.4,0.5,1))

ax1.annotate('$\\Gamma$',
            xy=(4999.9, 0.22),fontsize=12,color=(0.4,0.5,1))
plt.savefig("Seccion.pdf")

# Figura para las frecunecias de resonancia indice complejo

def n(w,w0,G):
    n = 1 - (w**2-w0**2)/(2*((w**2-w0**2)**2+(w*G)**2))
    return n

def k(w,w0,G):
    k = (w*G)/(2*((w**2-w0**2)**2+(w*G)**2))
    return k

def n1(w,w0,G):
    n1 = - (w**2-w0**2)/(2*((w**2-w0**2)**2+(w*G)**2))
    return n1



f,  axs = plt.subplots(2, 2, figsize=(12,9))

xlim=[5,25]
w0=15
G=[2,4,6,8]
w=np.linspace(xlim[0],xlim[1],1000)

        

for i in range(2):
    for j in range(2):
        axs[i,j].set_xlabel("$\omega \ (\mathrm{rad}/s)$")
        axs[i,j].set_xticks([w0],["$\omega_0$"])
        axs[i,j].set_yticks([0],["0"])
        axs[i,j].set_xlim(xlim[0],xlim[1])
        t=np.linspace(0,5000,3)
        axs[i,j].plot(t,3*[0],color="black",linewidth=1,linestyle="--")

na=n1(w,w0,G[0])
k1=k(w,w0,G[0])

axs[0,0].plot(w,na,color="blue",linewidth=2.0,label="$n-1$")
axs[0,0].plot(w,k1,color="red",linewidth=2.0,label="$\\kappa$")
axs[0,0].legend()


axs[0,1].set_xlim(xlim[0]+4.75,xlim[1]-4.75)
axs[0,1].set_ylim(min(na)-0.001,max(k1)+0.001)
axs[0,1].plot(w,na,color="blue",linewidth=2.0,label="$n-1$")
axs[0,1].plot(w,k1,color="red",linewidth=2.0,label="$\\kappa$")

axs[0,1].set_xticks([w0-G[0]/2],["$\omega_0-\Gamma/2$"])
axs[0,1].set_xticks([w0,w0+G[0]/2,w0-G[0]/2],["$\omega_0$","$\omega_0+\Gamma/2$","$\omega_0-\Gamma/2$"])
ya=k(w0-G[0]/2,w0,G[0])
axs[0,1].plot([w0-G[0]/2,w0+G[0]/2],[ya,ya],color="red",linestyle="--")
axs[0,1].legend()
axs[0,1].annotate('$\\Gamma$',
            xy=(w0+1.3,ya),fontsize=12,color="red")


axs[0,1].plot([w0,w0],[-5,max(k1)],color="grey",linestyle="--")
axs[0,1].plot([w0-G[0]/2,w0-G[0]/2],[-5,ya],color="grey",linestyle="--")
axs[0,1].plot([w0+G[0]/2,w0+G[0]/2],[-5,ya],color="grey",linestyle="--")


for i in range(len(G)):
    na=n1(w,w0,G[i])
    axs[1,0].plot(w,na,label="$\\Gamma=%d $"%G[i],linewidth=2,color=(0.3+0.20*i,0.2+0.06*i,1))
axs[1,0].legend()


for i in range(len(G)):
    ka=k(w,w0,G[i])
    axs[1,1].plot(w,ka,label="$\\Gamma=%d $"%G[i],linewidth=2,color=(0.3+0.20*i,0.2+0.06*i,1))
axs[1,1].legend()



plt.savefig("indicecomplejo.pdf")