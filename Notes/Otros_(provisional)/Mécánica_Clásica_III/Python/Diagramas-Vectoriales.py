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

from matplotlib.colors import Normalize



plt.figure()
X, Y = np.meshgrid(np.arange(-4.5,4.5, .5), np.arange(-4.5,4.5, .5))
U = -0.6*X
V = -0.8*Y

# No colores



fig1, ax1 = plt.subplots()

x = np.linspace(-5,5,10)
y = 10*[0]
ax1.plot(x,y,color="red",linestyle="--",label="$v_1$")
ax1.plot(y,x,color="red",linestyle="--",label="$v_2$")

Q =ax1.quiver(X, Y, U, V, units='xy',pivot="mid",scale=4)
qk = ax1.quiverkey(Q, 0.9, 0.9, 2, r'', labelpos='E',
                   coordinates='figure')

plt.legend()
plt.xlabel("q")
plt.ylabel("p")
plt.xlim(-4.1,4.1)
plt.ylim(-4.1,4.1)
plt.savefig("nodo-estable.pdf")


# Colores

plt.figure()

fig3, ax3 = plt.subplots()
M = np.hypot(U, V)

plt.xlabel("q")
plt.ylabel("p")
plt.xlim(-4.1,4.1)
plt.ylim(-4.1,4.1)

colormap = cm.inferno


Q = ax3.quiver(X, Y, U, V, M, cmap=colormap, units='xy', pivot="mid",scale=4)
qk = ax3.quiverkey(Q, 0.9, 0.9, 2, r'', labelpos='E',
                   coordinates='figure')


plt.savefig("color-nodo-estable.pdf")