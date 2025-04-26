# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:00:07 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from Efecto_fotoelectrico_Datos import I1,V1,V2,I2,I3,V3,I4,V4,I5,V5,l
from Efecto_fotoelectrico_Funciones import corte,lineal,regresion_lineal_s, printea_sticks, concatenarbueno
from tabulate import tabulate
# Calculo de los cortes de las rectas

V=[V1,V2,V3,V4,V5]
I=[I1,I2,I3,I4,I5]
p=np.array([0.002,0.002,0.002,0.002,0.002])*10**3 # Este parametro regula a partir del punto que hacer el ajuste de la recta con pendiente
c=np.array([0.35,0.035,0.6,1,0.6]) # Este parametro regula a partir del punto que hacer el ajuste de la recta con meons pendiente
q=np.array([1,0.5,0.5,0.3,0.4]) # Este parametro regula a partir del aparece la gráfica de corte

h,sh,a1,a2,b1,b2,sa1,sa2,sb1,sb2=corte(V,I,l,p,q,c)

#tabla=concatenarbueno(a1,sa1,b1,sb1,a2,sa2,b2,sb2)
#header=["a (nA)", "s(a) (nA)","b (nA/V)","s(b) (nA/V)","a (nA)", "s(a) (nA)","b (nA/V)","s(b) (nA/V)"]
#tabla=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f"))













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
plt.grid(True,linestyle="--")
printea_sticks(h)
plt.xlim(min(1/l)-0.00005,max(1/l)+0.00005)
plt.legend()
plt.savefig("Metodo_2-con.pdf",bbox_inches="tight")

cp_c=cte.e*b/cte.c*10**(-9)
scp_c=cte.e*sb/cte.c*10**(-9)
print(cp_c,scp_c)
# Eliminamos ultimo dato

plt.figure()
l=l[1:]
h=h[1:]
sh=sh[1:]
a,b,sa,sb=regresion_lineal_s(1/l, -h,sh)
u=np.linspace(min(1/l),max(1/l),10)
v=lineal(u,a,b)
printea_sticks(h)
plt.xlim(min(1/l)-0.00005,max(1/l)+0.00005)
plt.plot(u,v,color="red",label="Aproximación lineal")
plt.errorbar(1/l,-h,yerr=sh,fmt=".",capsize=2.0,color="blue",ecolor="cornflowerblue",label="Datos experimentales")
bbox = dict(boxstyle="round", fc="0.98",alpha=0.8)
plt.annotate("   a=%.1f (V) \nb=%d (V$\cdot$nm)"%(a,b),((min(1/l)+max(1/l))/2,0.4),bbox=bbox)
plt.xlabel("$1/\lambda$ (nm$^{-1}$)")
plt.ylabel("$V_0$ (V)")
plt.grid(True,linestyle="--")
plt.legend()
plt.savefig("Metodo_2-sin.pdf",bbox_inches="tight")

cp_c=cte.e*b/cte.c*10**(-9)
scp_c=cte.e*sb/cte.c*10**(-9)
print(cp_c,scp_c)

"""