# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:32:03 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from tabulate import tabulate
"""
def focal(s,sprima,d) :
    f=[0]*len(s)
    for i in range(len(s)):
        f[i] = -(1/(-sprima[i]+d[i])-1/(d[i]-s[i]))**(-1)
    return np.array(f)
"""

def incertidumbre(x):
    sx=np.sqrt(sum((x-(np.average(x)))**2)/((len(x)-1)*len(x)))
    return sx


def lineal1(x,a):
    y=a+x
    return y

def incertidumbrepropagada(sx,sy):
    sz = np.sqrt(sx**2+sy**2)
    return sz

def incertidumbrepropagadan(s):
    for i in range(len(s)):
        b=sum((s/len(s))**2)
    a=np.sqrt(b)
    return a

def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

imagen=np.array([33.4,19.9,35.7,59.8,24.4,15.0,27.6,39,46,31.4])
lente=np.array([50,36.5,52,75.3,40.2,32.0,44.6,56.2,62.9,48.5])

focal=lente-imagen
d=0.1/(np.sqrt(12))
ss=np.sqrt(2)*d
sfocal=np.sqrt((ss/(np.sqrt(len(imagen))))**2+incertidumbre(focal)**2)
print('f= %.2f  \\quad s(f)=%.2f'%(np.average(focal),sfocal))



tabla=concatenarbueno((imagen,[d]*len(imagen),lente,[d]*len(lente),focal,[ss]*len(focal)))
header=["d (cm)", "s(d) (cm)","l (cm)", "s(l) (cm)","f (cm)", "s(f) (cm)"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".2f",".2f",".2f",".2f",".3f", ".3f"))
outfile=open("Regresion%d.txt"%(7), 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Datos para el método de la autocolimación} \n")
outfile.write("\\label{tab:datos-parte-1.2.%d} \n"%(1))
outfile.write("\\end{table} \n \n \n")
outfile.close()


"""
D=lente
Dp=imagen
sDp=[d]*len(lente)
a=curve_fit(lineal1,D,Dp,sigma=sDp,absolute_sigma=True, maxfev=5000)[0]
ss=curve_fit(lineal1,D,Dp,sigma=sDp,absolute_sigma=True,maxfev=5000)[1]
sa=ss
x=np.linspace(min(D),max(D),10)
y=lineal1(x, a)
plt.figure(dpi=1000)
plt.grid(True,linestyle="--")
plt.plot(x,y,"royalblue")
plt.xlabel("$D \ (cm^{-1})$")
plt.ylabel("$D' \ (cm^{-1})$")
plt.errorbar(D, Dp, yerr=sDp, fmt=".",capsize=3.0,ecolor="cornflowerblue",color="blue")
plt.savefig("1-Focal.pdf",dpi=300,bbox_inches="tight")

f1=a
sf1=sa
print("f_1=",f1,"s(f_1)",sf1)!"""