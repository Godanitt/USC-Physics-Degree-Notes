# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:53:16 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte


def lineal(x,a,b):
    y = a+b*x
    return y

def regresion_lineal(x,y):
    a,b=curve_fit(lineal,x,y,maxfev=10000)[0]
    return a,b

def plotea(x,y,a,b):
    plt.figure()
    u=np.linspace(min(x),max(x),20)
    v=lineal(u,a,b)
    plt.plot(u,v,color="blue")
    plt.plot(x,y,".",color="red")
    


    
#%%
D1=np.array([95.9-8.6,80-8.6,75.5-8.6,63.5-8.6])*10**(-2)+0.0032
i1=np.array([815.02/4,1032.02/5,1020.04/5])
i2=np.array([1174.21/7,1176.07/7,1006.06/6])
i3=np.array([944.00/6,945.02/6,948.01/6])
i4=np.array([1030.02/8,1037/8,1039.02/8])
d=np.array([754.21,751,754.03])

i=np.array([np.average(i1),np.average(i2),np.average(i3),np.average(i4)])
i1=4.2*10**(-6)*i

d1=d*(1/4)*10**(-3)/588.17

a1,b1=regresion_lineal(D1, i1)
plotea(D1,i1,a1,b1)

lambda11=np.average(d1)*i/D1

print(D1)
print(i1)

lamb1=b1*np.average(d1)*10**9

print("lambda1= %.2f"%lamb1)

#%%

D2=np.array([95.9-8.6,80-8.6,75.5-8.6,63.5-8.6])*10**(-2)
i11=np.array([650.00/3,652.05/3,864/4])
i2=np.array([965.05/5,970.02/5,980/5])
i3=np.array([990/6,988/6,985.02/6])
i4=np.array([837.01/6,968.05/7,980.02/7])
d=np.array([729.17,728.03,726.05])



i=np.array([np.average(i11),np.average(i2),np.average(i3),np.average(i4)])
i2=5.2*10**(-6)*i
d2=d*(1/4)*10**(-3)/588.17

a2,b2=regresion_lineal(D2, i2)
plotea(D2,i2,a2,b2)

print(D2)
print(i2)

lamb2=b2*np.average(d2)*10**9

print("lambda2= %.2f"%lamb2)