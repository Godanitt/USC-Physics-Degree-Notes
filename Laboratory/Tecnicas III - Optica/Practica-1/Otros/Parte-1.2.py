# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:32:03 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
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

def incertidumbrepropagada(sx,sy):
    sz = np.sqrt(sx**2+sy**2)
    return sz

def incertidumbrepropagadan(s):
    for i in range(len(s)):
        b=sum(s**2)/len(s)
    a=np.sqrt(b)
    return a

imagen=np.array([33.4,19.9,35.7,59.8,24.4,15.0,27.6,39,46,31.4])
lente=np.array([50,36.5,52,75.3,40.2,32.0,44.6,56.2,62.9,48.5])

focal=lente-imagen
d=0.1/(np.sqrt(12))
ss=incertidumbrepropagadan(np.array([np.sqrt(2)*d]*len(imagen)))
sfocal=incertidumbrepropagada(ss/(np.sqrt(len(imagen))), incertidumbre(focal))
print('f= %.2f  \\quad s(f)=%.2f'%(np.average(focal),sfocal))



tabla=concatenarbueno((f3,sf3))
header=["f (cm)", "s(f) (cm)"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f"))
outfile=open("Regresion%d.txt"%(7), 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Datos para la medida número %d} \n"%(7))
outfile.write("\\label{tab:datos-parte-1.1.%d} \n"%(7))
outfile.write("\\end{table} \n \n \n")
outfile.close()



#a,b=curve_fit(lineal,imagen,lente,maxfev=10000)[0]
#focal1=a