# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:17:20 2024

@author: danie
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from Efecto_fotoelectrico_Datos import I1,V1,V2,I2,I3,V3,I4,V4,I5,V5,l
from Efecto_fotoelectrico_Funciones import lineal, printea_sticks, regresion_lineal_s, corte, regresion_lineal



V0=np.array([1.15,1.2,0.85,0.5,0.35])
sV0=np.array([0.2,0.15,0.1,0.1,0.08])

h=-V0
sh=sV0
"""
plt.figure()
l=10**(9)*l
a,b,sa,sb=regresion_lineal_s(1/l, -h,sh)
u=np.linspace(min(1/l),max(1/l),10)
v=lineal(u,a,b)
plt.plot(u,v,color="red",label="Aproximación lineal")
plt.errorbar(1/l,-h,yerr=sh,fmt=".",capsize=2.0,color="blue",ecolor="cornflowerblue",label="Datos experimentales")
bbox = dict(boxstyle="round", fc="0.98",alpha=0.8)
plt.annotate("   a=%.1f (V) \nb=%d (V$\cdot$nm)"%(a,b),((min(1/l)+max(1/l))/2,0.4),bbox=bbox)
plt.xlabel("$1/\lambda$ (nm$^{-1}$)")
plt.ylabel("$V_0$ (V)")
printea_sticks(h)
plt.xlim(min(1/l)-0.00005,max(1/l)+0.00005)
plt.grid(True,linestyle="--")
plt.legend()
plt.savefig("Metodo_1-con.pdf",bbox_inches="tight")

cp_c=cte.e*b/cte.c*10**(-9)
scp_c=cte.e*sb/cte.c*10**(-9)
print(cp_c,scp_c)
# Eliminamos ultimo dato

plt.figure()
l=l[1:]
h=h[1:]
sh=sh[1:]
a,b,sa,sb=regresion_lineal(1/l, -h)
u=np.linspace(min(1/l),max(1/l),10)
v=lineal(u,a,b)
plt.ylabel("$V_0$ (V)")
printea_sticks(h)
plt.plot(u,v,color="red",label="Aproximación lineal")
plt.errorbar(1/l,-h,yerr=sh,fmt=".",capsize=2.0,color="blue",ecolor="cornflowerblue",label="Datos experimentales")
bbox = dict(boxstyle="round", fc="0.98",alpha=0.8)
plt.annotate("   a=%.1f (V) \nb=%d (V$\cdot$nm)"%(a,b),((min(1/l)+max(1/l))/2,0.4),bbox=bbox)
plt.xlabel("$1/\lambda$ (nm$^{-1}$)")
plt.ylabel("$V_0$ (V)")
plt.grid(True,linestyle="--")
plt.legend()
plt.savefig("Metodo_1-sin.pdf",bbox_inches="tight")

cp_c=cte.e*b/cte.c*10**(-9)
scp_c=cte.e*sb/cte.c*10**(-9)
print(cp_c,scp_c)
"""