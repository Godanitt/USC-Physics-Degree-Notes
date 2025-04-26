# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:24:52 2023

@author: danie
"""


import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so




def todo(t,T):
    def f(t,A,B):
        y = A + B*t
        return y

    par = [1,1]
    sol = so.curve_fit(f,t,T,p0=(par))
    A,B=sol[0]
    x = np.linspace(min(t),max(t),100)
    y = f(x,A,B)
    plt.figure()
    plt.grid(True, linestyle="--")
    plt.plot(x,y,"r")
    plt.plot(t,T,".",color="darkred")
    


t = [1,2,3,4]
T = [2,4,7,8]

todo(t,T)