# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 21:00:38 2023

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



w = 3
Y, X = np.mgrid[-w:w:50j, -w:w:50j]
U = Y
V = X*(X**2-1)
speed = np.sqrt(U**2 + V**2)
lw = 5*speed / speed.max()



x = np.linspace(-w,w,10)
y = 10*[0]

plt.streamplot(X, Y, U, V, arrowsize=1.1, linewidth=1.2, density = w/5, broken_streamlines=False,color="black")

#plt.plot(x,y,color="red",linestyle="--",label="$v_1$",linewidth=0.7)
#plt.plot(y,x,color="orangered",linestyle="--",label="$v_2$",linewidth=0.7)

plt.xlabel("q")
plt.ylabel("p")
plt.xlim(-w,w)
plt.ylim(-w,w)
plt.legend()
plt.savefig("Ejercicio-23b.pdf")
