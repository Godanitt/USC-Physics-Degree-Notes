# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:14:41 2024

@author: danie
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import scipy.constants as cte
import scipy.optimize as so
from Funciones import parabola, sacavalores, aproximaparabolas, energia, Emedia, longitud_onda
from Parabolas import an,san

E,sE=energia(an, san)

plt.figure(2)

Em,sEm=Emedia(E, sE)
l,sl=longitud_onda(Em, sEm)
for i in range(len(l)):
    #print("Longitud de onda: %.2f +- %.2f nm"%(l[i]*10**9,sl[i]*10**9))
    print("La energía media: %.2f +- %.2f eV"%(Em[i],sEm[i]))

print("La energía debería ser 4.86")