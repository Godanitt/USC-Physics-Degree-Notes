# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 22:41:54 2024

@author: danie
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import *


def Semiempirica_plot(A,Z):
    Av=15.5
    As=16.8
    Ac=0.72
    Asy=23
    Ap=34
    if (A%2==1):
        valor=Av*A-As*A**(2/3)-Ac*(Z*(Z-1))*A**(-1/3)-(Asy*(A-2*Z)**2)/A
  #  elif(Z%2==0):
  #      valor=Av*A-As*A**(2/3)-Ac*(Z*(Z-1))*A**(-1/3)-(Asy*(A-2*Z)**2)/A+Ap*(A**(-3/4))
    else:    
        valor=Av*A-As*A**(2/3)-Ac*(Z*(Z-1))*A**(-1/3)-(Asy*(A-2*Z)**2)/A-Ap*(A**(-3/4))
    valor=valor*(10**6*e)
    return valor # En Julios

def Masa(A,Z):
    M=(Z*m_p+(A-Z)*m_n-Semiempirica_plot(A, Z)/c**2)/(1.66053906660e-27)
    return M # En umas

A=125
Z=np.linspace(48,58,120)

plt.plot(Z,Masa(A, Z))
#plt.plot(Z,Masa(A, Z)+(2*34*(A**(-3/4)))*(10**6*e)*(1/(c**2*1.66053906660e-27)),linestyle="--")