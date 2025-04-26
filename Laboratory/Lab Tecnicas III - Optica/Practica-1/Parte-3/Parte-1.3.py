# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:11:38 2024

@author: danie
"""


import numpy as np 
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte

def focalbessel(a,e,sa,se):    
    f=((np.average(a)**2)-(np.average(e))**2)/(4*np.average(a)) 
    e1=np.average(e)
    a1=np.average(a)
    sf=np.sqrt((sa*(a1**2+e1**2)/(4*a1**2))**2+(se*e1/(2*a1))**2)
    return f,sf

def incertidumbre(x):
    x=np.array(x)
    sx=np.sqrt(sum((x-(np.average(x)))**2)/((len(x)-1)*len(x)))
    return sx

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

def promedioincertidumbre(x,sx):
    w=1/sx**2
    xm=np.sum(x*w)/np.sum(w)
    sxm=1/np.sqrt(sum(w))             
    return xm,sxm

at=np.array([[0]*5]*5)
et=np.array([[0]*5]*5)


d=0.1/np.sqrt(12)

# Primera medida

a1 = np.array([105,105,105,105,105])
a2 = np.array([5,5,5,5,5])
a = a1-a2
e1 = np.array([85,84,85.2,84.7,84.9])
e2 = np.array([25.5,25.5,26.2,24.9,25.5])
e = e1-e2


at[0,:]=a
et[0,:]=e

# Segunda medida

a1 = np.array([100]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([25.2,26.4,25.2,26.4,25.0])
e2 = np.array([78.8,80.0,78.6,79.7,78.9])
e = e1-e2


at[1,:]=a
et[1,:]=e

# Tercera medida


a1 = np.array([95]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([26.5,26.8,25.6,26.9,27.2])
e2 = np.array([73.4,74.6,73.0,74.9,75.0])
e = e1-e2

at[2,:]=a
et[2,:]=e

# Cuarta medida

a1 = np.array([90]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([28.0,26.1,27.6,26.6,27.3])
e2 = np.array([69.0,68.4,68.8,67.9,69.2])
e = e1-e2



at[3]=a
et[3]=e

# Quinta medida

a1 = np.array([85]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([28.6,27,28.4,27.1,28.1])
e2 = np.array([63.5,61.9,63.2,62.4,62.7])
e = abs(e1-e2)

at[4]=a
et[4]=e

# DATOS
outfile=open("Datos.txt", 'w')
et=abs(et)
focal,sfocal=np.array([]),np.array([])
se,sa=np.array([]),np.array([])
e,a=np.array([]),np.array([])
for i in range(len(at)):
    sa=np.append(sa,d*np.sqrt(2))
    se=np.append(se,incertidumbrepropagada(incertidumbre(et[i]), d*np.sqrt(2)))
    e=np.append(e,np.average(et[i]))
    a=np.append(a,np.average(at[i]))
    f,sf=focalbessel(at[i], et[i], sa[i], se[i])
    focal=np.append(focal,f)
    sfocal=np.append(sfocal,sf)
    
    tabla=concatenarbueno((at[i],[d*np.sqrt(2)]*len(at[i]),et[i],[d*np.sqrt(2)]*len(et[i])))
    header=["a (cm)", "s(a) (cm)", "e (cm)","s(e) (cm)"]
    hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".2f", ".2f",".2f",".2f"))
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write(hola)
    outfile.write("\\caption{Datos para la medida número %d} \n"%(i+1))
    outfile.write("\\label{tab:datos-parte-1.3.%d} \n"%(i+1))
    outfile.write("\\end{table} \n \n\n")    

outfile.close()

outfile=open("Focales.txt","w")


tabla=concatenarbueno((focal,sfocal))
header=["f (cm)", "s(f) (cm)"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f"))
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Datos para la medida número %d} \n"%(6))
outfile.write("\\label{tab:datos-parte-1.3.%d} \n"%(6))
outfile.write("\\end{table} \n \n\n")  
outfile.close()

def bessel(x,f):
    y=-4*f*x+x**2
    return y


se2=e*se
f,sf=curve_fit(bessel, a, e**2, sigma=se)
sf=np.sqrt(sf)
x=np.linspace(min(a),max(a),200)
y=bessel(x,f)
plt.plot(x,y,"red",label="Regresión cuadratica")
plt.errorbar(a,e**2,yerr=se2,fmt=".",capsize=3.0,ecolor="cornflowerblue",color="blue",label="Datos experimentales")
plt.xlabel("$a \ (cm)$")
plt.ylabel("$e^2 \ (cm^{2})$")
plt.legend()
plt.grid(True,linestyle="--")
plt.savefig("2-focal.pdf",dpi=300,bbox_inches="tight")

f1,sf1=promedioincertidumbre(focal, sfocal)
f2,sf2=f,sf

print("f^{(1)} = %.3f \\quad s(f^{(1)}) = %.3f"%(f2,0.011))
print("f^{(2)} = %.3f \\quad s(f^{(2)}) = %.3f"%(f1,sf1))