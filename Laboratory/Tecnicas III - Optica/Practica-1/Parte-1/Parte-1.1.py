# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:50:14 2024

@author: danie
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte

def lineal1(x,a):
    y=a-x
    return y
import sympy as sy
from tabulate import tabulate

x, y, z, a, b = sy.symbols('x y z a b')
fun = sy.Function('f')
sy.init_printing(use_unicode=True)


def lineal(x,a,b):
    y=a-b*x
    return y

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
        b=sum((s/len(s))**2)
    a=np.sqrt(b)
    return a

def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

# PRIMER EXPERIMENTO

sd = (0.1)/(np.sqrt(12))                       # En cm, para todos los datos

# Primera distancia
objeto1=np.array([5.0]*6)          #En cm
imagen1=np.array([101.1,100,101.2,100.3,102.00,100.9])
lente1=np.array([80.5]*6)


# Segunda distancia
objeto2=np.array([5.0]*6)          #En cm
imagen2=np.array([105.0,105.9,104.5,105.9,104.9,105.8])
lente2=np.array([85.0]*6)

# Terce distancia
objeto3=np.array([5]*6)          #En cm
imagen3=np.array([110.5,109.6,110.8,109.6,110.5,109.6])
lente3=np.array([90.0]*6)


# Cuarta distancia
objeto4=np.array([5.0]*6)          #En cm
imagen4=np.array([114.9,113.9,114.7,113.7,115.0,113.9])
lente4=np.array([95.0]*6)

# Quinta distancia
objeto5=np.array([5.0]*6)          #En cm
imagen5=np.array([119.0,119.9,118.9,119.9,118.9,119.7])
lente5=np.array([100.0]*6)


# Sexta distancia

objeto6=np.array([5.0]*6)          #En cm
imagen6=np.array([124.5,123.9,124.6,123.6,124.5,123.8])
lente6=np.array([105.0]*6)

# GENERAL:

objeto=np.array([objeto1,objeto2,objeto3,objeto4,objeto5,objeto6])
imagen=np.array([imagen1,imagen2,imagen3,imagen4,imagen5,imagen6])
lente=np.array([lente1,lente2,lente3,lente4,lente5,lente6])

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



for i in range(len(imagen)):
    tabla=concatenarbueno((objeto[i],[ss]*len(objeto[i]),imagen[i],[ss]*len(imagen[i])))
    header=["s (cm)", "s(s) (cm)", "s' (cm)","s(s') (cm)"]
    hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".2f", ".2f",".2f",".2f"))
    outfile=open("Regresion%d.txt"%(i+1), 'w')
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write(hola)
    outfile.write("\\caption{Datos para la medida número %d} \n"%(i+1))
    outfile.write("\\label{tab:datos-parte-1.1.%d} \n"%(i+1))
    outfile.write("\\end{table} \n \n \n")
    outfile.close()


    


# CALCULO DE DATOS:
   
D=(1/ob)
Dp=(1/im)
sD = sob*D**2
sDp = sim*Dp**2

# CALCULAMOS POR REGRESION:

a=curve_fit(lineal1,D,Dp,sigma=sDp,absolute_sigma=True,method="trf",bounds=(0.05,0.07), maxfev=5000)[0]
ss=curve_fit(lineal1,D,Dp,sigma=sDp,absolute_sigma=True,method="trf",bounds=(0.05,0.07),maxfev=5000)[1]
sa=np.sqrt(ss)
x=np.linspace(min(D),max(D),10)
y=lineal1(x, a)
plt.figure(dpi=1000)
plt.grid(True,linestyle="--")
plt.plot(x,y,"red",label="Regresión lineal")
plt.xlabel("$D \ (cm^{-1})$")
plt.ylabel("$D' \ (cm^{-1})$")
plt.errorbar(D, Dp, yerr=sDp, fmt=".",capsize=3.0,ecolor="cornflowerblue",color="blue",label="Datos experimentales")
plt.legend()
plt.savefig("1-Focal.pdf",dpi=300,bbox_inches="tight")

f1=1/a
sf1=sa*f1**2
print("f_1=",f1,"s(f_1)",sf1)

# CALCULAMOS POR MEDIO


f3=(ob*im)/(ob+im)
sf3=np.sqrt((sob*(ob**2/(ob+im)**2))**2+(sim*(im**2/(ob+im)**2))**2)

f_3=np.average(f3)
sf_3=incertidumbrepropagadan(sf3)
sf3l=incertidumbre(f3)
print(sf3l,sf_3)
sf_3=incertidumbrepropagada(sf3l,sf_3)

print("f_3=",f_3,"s(f_3)",sf_3)


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




    

# PRINTEAMOS LAS TABLAS EN FORMATO DE LATEX


# PRINTEAMOS LAS TABLAS DE RESULTADOS EN LATEX



#