# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:13:24 2023

@author: danie
"""

# Datos teóricos

import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so
from mpl_toolkits.mplot3d import Axes3D




R = 328  + 17.8
sR = np.sqrt((2+328*0.005)**2+(0.02+17.8*0.005)**2)

L = 33*10**(-3)
sL = 0.05*L

C = 22*10**(-9)
sC = 0.05*C

w0 =  1/np.sqrt(L*C)
sw0 = (np.sqrt((sC/np.sqrt(L*C**3))**2+((sL/np.sqrt(C*L**3))**2)))/2

Q = w0*L/R
sQ = np.sqrt((sw0*L/R)**2+(sL*w0/R)**2+(sR*L*w0/(R**2))**2)

B = w0/(2*np.pi*Q)
sB = np.sqrt((sQ*w0/(2*np.pi*(Q**2)))**2+(sw0/(2*np.pi*Q))**2)


outfile = open('DatosTeorios1.txt',"w")
outfile.write("\\begin{equation} \n")
outfile.write("\\begin{array}{lllllllll}\n")
outfile.write("R_T & = & %.1f & \ \Omega &  \ \ &  s(R_T) & =  & %.1f & \ \Omega \\\ \n"%(R,sR))
outfile.write("C & = & %.1f & \ nF &  \ \ &  s(C) & =  & %.1f & \ nF \\\ \n"%(22.0, 1.1))
outfile.write("L & = & %0.1f & \ mH &  \ \ &  s(L) & =  & %.1f & \ mH \\\ \n"%(33,1.6))       
outfile.write("\\end{array} \n")
outfile.write("\\end{equation} \n \n ")
outfile.close()


outfile = open('DatosTeorios2.txt',"w")
outfile.write("\\begin{equation} \n")
outfile.write("\\begin{array}{lllllllll}\n")
outfile.write("w_0 & = & %d \cdot 10^{2} & \ \mathrm{rad}/s &  \ \ &  s(w_0) & =  & %d \cdot 10^{2} & \ \mathrm{rad}/s \\\ \n"%(w0/100,sw0/100))
outfile.write("f_0 & = & %d \cdot 10 & \ \Hz &  \ \ &  s(f_0) & =  & %d \cdot 10 & \ \Hz \\\ \n"%(w0/(10*2*np.pi),sw0/(100*2*np.pi)))
outfile.write("Q & = & %.2f  &   \ & \ &  s(Q) & =  & %.2f & \\\ \n"%(Q, sQ))
outfile.write("B & = & %d \cdot 10 & \ s^{-1} &  \ \ &  s(B) & =  & %d  \cdot 10 & \ s^{-1} \\\ \n"%(B/10,sB/10))       
outfile.write("\\end{array} \n")
outfile.write("\\end{equation} \n \n ")
outfile.close()

