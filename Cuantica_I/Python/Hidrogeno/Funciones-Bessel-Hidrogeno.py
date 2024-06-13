# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:51:00 2023

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

X = np.arange(-20, 20, 0.25)
Y = np.arange(-20, 20, 0.25)
X, Y = np.meshgrid(X, Y)
r = np.sqrt(X**2 + Y**2)
theta = np.arctan(Y/X)

#Definimos las funciones radiales

def R(r,n,m):
    R = 0
    if n==2 and m==0:
       R = 2*((1/2)**(3/2))*(1-r/2)*np.e**(-r/2)
    if n==2 and m==1:
       R = (1/np.sqrt(3))*((1/2)**(3/2))*(r)*(np.exp(-r/2))
    if n==3 and m==0:
       R = 2*((1/3)**(3/2))*(1-2*r/3+2*(r**2)/27)*np.e**(-r/3)
    if n==3 and m==2:   
       R = (2*np.sqrt(2)/(27*np.sqrt(5)))*((1/3)**(3/2))*(r**2)*(np.exp(-r/3))
    return R      


# Calculamos Z

phi = 0
Z = abs(R(r,3,2))*scipy.sph_harm(0,2, phi, theta, out=None)



# Pintamos la superfie
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride = 1,cmap=cm.twilight_shifted, linewidth=0.5, antialiased=False)

# Customizamos el eje z
ax.set_zlim(-0, 0.05)
ax.zaxis.set_major_locator(LinearLocator(0))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.8, aspect=6)

plt.savefig("Hidrogeno_320.pdf")


# Representamos las funciones radiales

maxi = 20


plt.figure()
x = np.linspace(0,maxi,200)
y1 = abs(R(x,2,1))
y2 = abs(R(x,3,2))

plt.grid(True,linestyle="--")
plt.plot(x,y1,label="$|R_{21}|$",color="red")
plt.plot(x,y2,label="$|R_{32}|$",color="blue")
plt.ylim(-0.2,0.2)
plt.xlim(0,maxi)
plt.xlabel("$a_0$")
plt.ylabel("$R(r)$")
plt.legend()
plt.savefig("Funcionesradialesabsolutas.pdf")
"""
# Calculamos las energías problema 4 Cuantica

def E(Z,n):
    E = -(1/(4*np.pi*cte.epsilon_0)**2)*((4*np.pi**2*cte.m_e*(cte.e)**4)/(2*cte.h**2))*(1/(n**2))
    return E
    
E1 = E(1,2)/cte.e
E2 = E(1,3)/cte.e
prob = 10**(-16)

E = E1*prob**2+E2*(1-prob)**2
DE = np.sqrt(prob*(1-prob))*(E1-E2)

Dt = cte.h/(2*2*np.pi*DE*cte.e)

lamb = cte.c*cte.h/((E2-E1)*cte.e)
"""
