# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:13:30 2024

@author: danie
"""

# Cuarto experimento
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from tabulate import tabulate

# Funciones interesantes:
    
def combinada(sx,sy):
    sz=np.sqrt(sx**2+sy**2)
    return sz

def incertidumbre(x):
    s=np.sqrt(sum((x-np.average(x))**2)/(len(x)-1))
    return s

def combinadan(sx):
    s=np.sqrt(sum(sx**2)/(len(sx))**2)
    return s


def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

def focalita(im,ob,sim,sob):
    f=-(ob*im)/(ob-im)
    sf=np.sqrt((sob*(ob**2/(ob-im)**2))**2+(sim*(im**2/(ob-im)**2))**2)
    return f,sf

def lineal1(x,a):
    y=(a+x)
    return y

def promedioincertidumbre(x,sx):
    w=1/sx**2
    xm=np.sum(x*w)/np.sum(w)
    sxm=1/np.sqrt(sum(w))   
  #  xm=np.average(x)          
   # sxm=combinadan(sx)
    return xm,sxm

# Medida 1


di = np.array([13.0,13.5,13.4]) # Posicion objeto con lente divergente
dl = np.array([27.7,27.7,27.7]) # Posicion lente divergente (enfocada)

si = np.array([18.7,18.6,18.9]) # Posición objeto sin lente divergente
sl = np.array([27.7,27.7,27.7]) # Posición lente divergente (desenfocada)

si1=np.array([[0]*3]*5)
so=np.array([[0]*3]*5)

si1[0,:]=(di-dl)
so[0,:]=(si-sl)


# Medida 2


di = np.array([23.4,22.8,23.4]) # Posicion objeto con lente divergente
dl = np.array([40.9]*3) # Posicion lente divergente (enfocada)

si = np.array([31.2,30.5,31.1]) # Posición objeto sin lente divergente
sl = np.array([40.9]*3) # Posición lente divergente (desenfocada)


si1[1]=(di-dl)
so[1]=(si-sl)
# Medida 3

di = np.array([25.2,26.4,24.3]) # Posicion objeto con lente divergente
dl = np.array([39.6]*3) # Posicion lente divergensite (enfocada)

si = np.array([30.9,30.9,31.1]) # Posición objeto sin lente divergente
sl = np.array([39.6,]*3) # Posición lente divergente (desenfocada)

si1[2]=(di-dl)
so[2]=(si-sl)

# Medida 4

di = np.array([29.4,28.7,30.4]) # Posicion objeto con lente divergente
dl = np.array([53]*3) # Posicion lente divergente (enfocada)

si = np.array([42.6,42.3,42.6]) # Posición objeto sin lente divergente
sl = np.array([53]*3) # Posición lente divergente (desenfocada)

si1[3]=(di-dl)
so[3]=(si-sl)
# Medida 5

di = np.array([18.7,19.3,18.9]) # Posicion objeto con lente divergente
dl = np.array([35.5]*3) # Posicion lente divergente (enfocada)

si = np.array([26.4,26.2,26.4]) # Posición objeto sin lente divergente
sl = np.array([35.5]*3) # Posición lente divergente (desenfocada)

si1[4]=(di-dl)
so[4]=(si-sl)

si=si1

# RESULTADOS


ssi=np.array([[0.1/np.sqrt(6)]*3]*5)
sso=np.array([[0.1/np.sqrt(6)]*3]*5)

sim,som=np.array([]),np.array([])
ssim,ssom=np.array([]),np.array([])
focal,sfocal=np.array([]),np.array([])
outfile=open("Datos.txt", 'w')
for i in range(len(si)):
    sim=np.append(sim,np.average(si[i]))
    som=np.append(som,np.average(so[i]))
    ssim=np.append(ssim,combinada(incertidumbre(si[i]),(ssi[i,0])))
    ssom=np.append(ssom,combinada(incertidumbre(so[i]),(sso[i,0])))
    focal=np.append(focal,focalita(sim[i],som[i],ssim[i],ssom[i])[0])
    sfocal=np.append(sfocal,focalita(sim[i],som[i],ssim[i],ssom[i])[1])
    
    tabla=concatenarbueno((so[i],ssi[i],si[i],sso[i]))
    header=["s (cm)", "s(s) (cm)", "s' (cm)","s(s') (cm)"]
    hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".2f", ".2f",".2f",".2f",))

    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write(hola)
    outfile.write("\\caption{Datos para la medida número %d} \n"%(i+1))
    outfile.write("\\label{tab:datos-parte-1.4.%d} \n"%(i+1))
    outfile.write("\\end{table} \n \n \n")
    
outfile.close()

outfile=open("Focales.txt","w")
tabla=concatenarbueno((focal,sfocal))
header=["f (cm)", "s(f) (cm)"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f"))
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Datos para la medida número %d} \n"%(6))
outfile.write("\\label{tab:datos-parte-1.4.%d} \n"%(6))
outfile.write("\\end{table} \n \n\n")  
outfile.close()


f2,sf2=promedioincertidumbre(focal, sfocal)
sf2=combinada(incertidumbre(focal),sf2)
# Regresion lineal


D=abs(1/sim)
Dp=abs(1/som)
sD = ssom*D**2
sDp = ssim*Dp**2


a,ss=curve_fit(lineal1,D,Dp,p0=0.04648574,sigma=sDp,absolute_sigma=True, maxfev=5000)
sa=np.sqrt(ss)
x=np.linspace(min(D),max(D),10)
y=lineal1(x, a)
plt.figure(dpi=1000)
plt.grid(True,linestyle="--")
plt.plot(x,y,"red",label="Regresión lineal")
plt.xlabel("$D \ (cm^{-1})$")
plt.ylabel("$D' \ (cm^{-1})$")
plt.errorbar(D,Dp, yerr=sDp, fmt=".",capsize=3.0,ecolor="cornflowerblue",color="blue",label="Datos experimentales")
plt.legend()
plt.savefig("3-Focal.pdf",dpi=300,bbox_inches="tight")

f1=-1/a
sf1=sa*f1**2
print("f^{(1)} = %.3f  \\quad s\\parentesis{f^{(1)}} = %.3f"%(f1,sf1))
print("f^{(2)} = %.3f  \\quad s\\parentesis{f^{(2)}} = %.3f"%(f2,sf2))
