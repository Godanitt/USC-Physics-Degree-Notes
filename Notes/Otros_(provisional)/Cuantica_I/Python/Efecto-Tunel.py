# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 18:42:21 2023

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
from sympy.abc import A,B,C,D,E,k,a,b

eq1=symp.Eq(A+B-(C-D),0)
eq2=symp.Eq(symp.I*k*A-symp.I*k*B-(-b*C+b*D),0)
eq3=symp.Eq(C*symp.exp(-b*a)+D*symp.exp(b*a)-(E*symp.exp(symp.I*k*a)),0)
eq4=symp.Eq(-b*C*symp.exp(-b*a)+b*D*symp.exp(b*a)-(symp.I*k*E*symp.exp(symp.I*k*a)),0)

eqs=[eq1,eq2,eq3,eq4]

coeff=B,C,D,E
syms=A,k,a,b

symp.solve_undetermined_coeffs(eq1,eq2,eq3,eq4,coeff,syms,symp.S.Complexes)


eq=symp.Eq(a)