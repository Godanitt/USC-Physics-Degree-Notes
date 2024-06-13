# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:46:36 2024

@author: danie
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from tabulate import tabulate


# Medida de la primera focal

def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a


def distancia(x_0,x):
    y = abs(x_0-x)
    return y

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

sd = (0.1)/(np.sqrt(12))                       # En cm, para todos los datos

# Primera lente

objeto1=[10]*4 # En centimetros
lente1=[25,25,25,25]
imagen1=[54.4,57.1,55.6,57.2]

objeto2=[10]*4 # En centimetros
lente2=[27.5,27.5,27.5,27.5]
imagen2=[52.5,52.5,51.8,51.4]

objeto3=[10]*4 # En centimetros
lente3=[30]*4
imagen3=[50.3,50.8,50.4,50.6]


objeto=np.array([objeto1,objeto2,objeto3])
imagen=np.array([imagen1,imagen2,imagen3])
lente=np.array([lente1,lente2,lente3])

sobjeto=np.zeros(len(objeto))
simagen=np.zeros(len(imagen))

objeto=distancia(lente,objeto)
imagen=distancia(lente,imagen)

ob=np.zeros(len(objeto))
im=np.zeros(len(imagen))

for i in range(len(objeto)): 
    ss=incertidumbrepropagada(sd, sd)
    sobjeto[i]=ss
    simagen[i]=incertidumbrepropagada(ss, incertidumbre(imagen[i]))    
    ob[i]=np.average(objeto[i])
    im[i]=np.average(imagen[i])

sob=sobjeto
sim=simagen

f1=(ob*im)/(ob+im)
sf1=np.sqrt((sob*(ob**2/(ob+im)**2))**2+(sim*(im**2/(ob+im)**2))**2)

f_1=np.average(f1)
sf_1=incertidumbrepropagadan(sf1)
sf3=incertidumbre(f1)
sf_1=incertidumbrepropagada(sf3,sf_1)

print("f_1=",f_1,"s(f_1)",sf_1)


tabla=concatenarbueno((f1,sf1))
header=["f (cm)", "s(f) (cm)"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f"))
outfile=open("Focales1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Datos para la medida número %d} \n"%(7))
outfile.write("\\label{tab:datos-parte-1.1.%d} \n"%(7))
outfile.write("\\end{table} \n \n \n")
outfile.close()



# Segunda lente

objeto=[10]*4 # En centimetros
lente1=[20]*4
imagen1=[31,30.1,30.9,30.7]

objeto=[10]*4 # En centimetros
lente2=[19]*4
imagen2=[31.1,33,31.4,33.1]

objeto=[10]*4 # En centimetros
lente3=[23]*4
imagen3=[31.5,31.6,31.1,31.5]


objeto=np.array([objeto1,objeto2,objeto3])
imagen=np.array([imagen1,imagen2,imagen3])
lente=np.array([lente1,lente2,lente3])

sobjeto=np.zeros(len(objeto))
simagen=np.zeros(len(imagen))

objeto=distancia(lente,objeto)
imagen=distancia(lente,imagen)

ob=np.zeros(len(objeto))
im=np.zeros(len(imagen))

for i in range(len(objeto)): 
    ss=incertidumbrepropagada(sd, sd)
    sobjeto[i]=ss
    simagen[i]=incertidumbrepropagada(ss, incertidumbre(imagen[i]))    
    ob[i]=np.average(objeto[i])
    im[i]=np.average(imagen[i])

sob=sobjeto
sim=simagen

f1=(ob*im)/(ob+im)
sf1=np.sqrt((sob*(ob**2/(ob+im)**2))**2+(sim*(im**2/(ob+im)**2))**2)

f2=np.average(f1)
sf_1=incertidumbrepropagadan(sf1)
sf3=incertidumbre(f1)
sf2=incertidumbrepropagada(sf3,sf_1)

print("f_2=",f2,"s(f_2)",sf2)


tabla=concatenarbueno((f1,sf1))
header=["f (cm)", "s(f) (cm)"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f"))
outfile=open("Focales2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Datos para la medida número %d} \n"%(7))
outfile.write("\\label{tab:datos-parte-1.1.%d} \n"%(7))
outfile.write("\\end{table} \n \n \n")
outfile.close()

