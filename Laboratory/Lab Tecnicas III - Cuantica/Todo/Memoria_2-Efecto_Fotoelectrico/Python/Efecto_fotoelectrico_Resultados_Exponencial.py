# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:17:18 2024

@author: danie
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from Efecto_fotoelectrico_Datos import I1,V1,V2,I2,I3,V3,I4,V4,I5,V5,l
from Efecto_fotoelectrico_Funciones import exponencialh,lineal,printea_sticks,regresion_lineal,regresion_lineal_s



V=[V1,V2,V3,V4,V5]
I=[I1,I2,I3,I4,I5]

b=np.array([[-10,10],[-1.25,-0.90],[-1,-0.6],
            [-0.39,0],[-0.24,0]])
B,sB,C,sC=exponencialh(V, I, l,b)



def printea_exponenciales(C,sC,l,nombre):
    plt.figure()
    l=10**(9)*l
    a,b,sa,sb=regresion_lineal_s(1/l, C,sC)
    u=np.linspace(min(1/l),max(1/l),10)
    v=lineal(u,a,b)
    plt.plot(u,v,color="red",label="Aproximación lineal")
    plt.errorbar(1/l,C,yerr=sC,fmt=".",capsize=2.0,color="blue",ecolor="cornflowerblue",label="Datos experimentales")
    bbox = dict(boxstyle="round", fc="0.98",alpha=0.8)
    plt.annotate("   a=%.1f (V) \nb=%d (V$\cdot$nm)"%(a,b),((min(1/l)+max(1/l))/2,min(C)),bbox=bbox)
    plt.xlabel("$1/\lambda$ (nm$^{-1}$)")
    plt.ylabel("$V_0$ (V)")
    plt.grid(True,linestyle="--")
    printea_sticks(C)
    plt.xlim(min(1/l)-0.00005,max(1/l)+0.00005)
    plt.legend()
    plt.savefig("%s.pdf"%(nombre),bbox_inches="tight")
    cp_c=cte.e*b/cte.c*10**(-9)
    scp_c=cte.e*sb/cte.c
    print(cp_c,scp_c)

printea_exponenciales(-C, sC, l,"Metodo_3-Clasico-con")
printea_exponenciales(-C[1:], sC[1:], l[1:],"Metodo_3-Clasico-sin")
printea_exponenciales(-C+1/B, sC, l,"Metodo_3-Nuevo-con")
printea_exponenciales(-C[1:]+1/B[1:], np.sqrt(sC[1:]**2+(sB[1:]/B[1:]**2)**2),
                      l[1:] , "Metodo_3-Nuevo-sin")

# Segundo Metodo -C+1/B

"""
C=-C+1/B
C=C[:]
sC=np.sqrt(sC[:]**2+(sB[:]/B[:]**2)**2)
l=l[:]
plt.figure()
l=10**(9)*l
a,b,sa,sb=regresion_lineal_s(1/l, C,sC)
u=np.linspace(min(1/l),max(1/l),10)
v=lineal(u,a,b)
plt.plot(u,v,color="red",label="Aproximación lineal")
plt.errorbar(1/l,C,yerr=sC,fmt=".",capsize=2.0,color="blue",ecolor="cornflowerblue",label="Datos experimentales")
bbox = dict(boxstyle="round", fc="0.98")
plt.annotate("   a=%.1f (V) \nb=%d (V$\cdot$nm)"%(a,b),((min(1/l)+max(1/l))/2,0.6),bbox=bbox)
plt.xlabel("$1/\lambda$ (nm$^{-1}$)")
plt.ylabel("$V_0$ (V)")
plt.grid(True,linestyle="--")
plt.legend()
plt.savefig("V_Lambda-1_Exponencial.pdf",bbox_inches="tight")

cp_c21=cte.e*b/cte.c*10**(-9)
scp_c21=cte.e*sb/cte.c

# Eliminando 


plt.figure()
C=C[1:]
l=l[1:]
sC=sC[1:]
a,b,sa,sb=regresion_lineal(1/l, C)
u=np.linspace(min(1/l),max(1/l),10)
v=lineal(u,a,b)
plt.plot(u,v,color="red",label="Aproximación lineal")
plt.errorbar(1/l,C,yerr=sC,fmt=".",capsize=2.0,color="blue",ecolor="cornflowerblue",label="Datos experimentales")
bbox = dict(boxstyle="round", fc="0.98")
plt.annotate("   a=%.1f (V) \nb=%d (V$\cdot$nm)"%(a,b),((min(1/l)+max(1/l))/2,0.6),bbox=bbox)
plt.xlabel("$1/\lambda$ (nm$^{-1}$)")
plt.ylabel("$V_0$ (V)")
plt.grid(True,linestyle="--")
plt.legend()
plt.savefig("V_Lambda-1_Exponencial-sinprimerdato.pdf",bbox_inches="tight")

cp_c22=cte.e*b/cte.c*10**(-9)
scp_c22=cte.e*sb/cte.c"""