# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:52:50 2024

@author: danie
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import scipy.constants as cte
import scipy.optimize as so
from Funciones import parabola, sacavalores, concatenarbueno, aproximaparabolas, energia, Emedia, longitud_onda
from tabulate import tabulate
U2 = ["0_4","0_5","0_6","1_0", "1_5", "2_0"]
files = ["{}.txt".format(val) for val in U2]
dfs = [pd.read_csv(file, sep="\s+", decimal=",") for file in files]

maximos=np.zeros([6,5])
minimos=np.zeros([6,5])

i=0
for df in dfs:
    tipo=df["tipo"].to_numpy()
    V=df["U1[V]"].to_numpy()
    I=df["IA[nA]"].to_numpy()
    for j in range(len(tipo)):
        if str(tipo[j])=='maximo':
            maximos[i,j//2]=V[j]
        elif str(tipo[j])=='minimo':
            minimos[i,j//2]=V[j]
    i+=1
    


an=minimos
san=np.ones(np.shape(minimos))*0.20
ap=maximos    
sap=np.ones(np.shape(minimos))*0.20

V2=[0.4,0.5,0.6,1,1.5,2]
outfile=open("Extremos-lab.txt", 'w')
for i in range(len(an)):
    tabla=concatenarbueno(([1,2,3,4,5],ap[i],sap[i],an[i],san[i]))
    hola=tabulate(tabla,tablefmt="latex",floatfmt=(".0f",".2f",".2f",".2f",".2f"))
    outfile.write("\\begin{table}[h!] \t \centering \n") 
    outfile.write(hola)
    outfile.write("\\caption{Extremos para $U_2=%.2f$ V usando datos laboratorio.} \n"%(V2[i]))
    outfile.write("\\label{Tab:lab-%d} \n"%(i+1))
    outfile.write("\\end{table} \n \n \n")
outfile.close()



En,sEn=energia(an, san)
Ep,sEp=energia(ap, sap)


outfile=open("Energías-lab.txt","w")

V2=[0.4,0.5,0.6,1,1.5,2]
for i in range(len(En)):
     outfile.write("\\begin{table}[h!] \\centering \n")
     outfile.write("\\begin{tabular}{ccccc} \n")
     outfile.write("\\hline  & $ \Delta E_{\\max} $ (eV) & $s(\Delta E_{\\max})$ (eV) & $ \Delta E_{\\min} $ (eV) & $s(\Delta E_{\\min})$ (eV) \\\ \\hline \n")
     for j in range(len(En[i])):
        outfile.write("%d-%d & %.2f & %.2f & %.2f & %.2f \\\ \n"%(j+1,j+2,Ep[i,j],sEp[i,j],En[i,j],sEn[i,j]))
     outfile.write("\\hline \n")
     outfile.write("\\end{tabular}")
     outfile.write("\\caption{valores de la energía para $U_2=%.2f$} \n"%(V2[i]))
     outfile.write("\\label{Tab:E-lab-%d} \n"%(i+1))
     outfile.write("\\end{table} \n")
     outfile.write("\n \n \n")
     
outfile.close()

Enm,sEnm=Emedia(En[:,:], sEn[:,:])
Epm,sEpm=Emedia(Ep[:,:], sEp[:,:])



def media(x):
    xm=np.average(x)
    return xm

def incertidumbre(sx):
    sxm=np.sqrt(np.dot(sx,sx)/len(sx)**2)
    return sxm

outfile=open("Energías-medias-lab.txt","w")

V2=[0.4,0.5,0.6,1,1.5,2]
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{ccccc} \n")
outfile.write("\\hline $U_2$ (V) & $ \Delta E_{\\max} $ (eV) & $s(\Delta E_{\\max})$ (eV) & $ \Delta E_{\\min} $ (eV) & $s(\Delta E_{\\min})$ (eV) \\\ \\hline \n")
for j in range(len(Enm)):
    outfile.write("%.2f & %.2f & %.2f & %.2f & %.2f \\\ \n"%(V2[j],Epm[j],sEpm[j],Enm[j],sEnm[j]))
outfile.write("\\hline  \\hline \n")
outfile.write("- & %.3f & %.3f & %.3f & %.3f \\\ \n"%(media(Epm),incertidumbre(sEpm),media(Enm),incertidumbre(sEnm)))
outfile.write("\\hline\n")
outfile.write("\\end{tabular}")
outfile.write("\\caption{valores medios de la $\Delta E$ por los valores del programa.} \n")
outfile.write("\\label{Tab:Em-lab-%d} \n"%(i+1))
outfile.write("\\end{table} \n")
     
outfile.close()


# Sin el primer dato

Enm,sEnm=Emedia(En[:,:], sEn[:,:])
Epm,sEpm=Emedia(Ep[:,1:], sEp[:,1:])

outfile=open("Energías-medias-lab-sin.txt","w")
V2=[0.4,0.5,0.6,1,1.5,2]
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{ccccc} \n")
outfile.write("\\hline $U_2$ (V) & $ \Delta E_{\\max} $ (eV) & $s(\Delta E_{\\max})$ (eV) & $ \Delta E_{\\min} $ (eV) & $s(\Delta E_{\\min})$ (eV) \\\ \\hline \n")
for j in range(len(Enm)):
    outfile.write("%.2f & %.2f & %.2f & %.2f & %.2f \\\ \n"%(V2[j],Epm[j],sEpm[j],Enm[j],sEnm[j]))
outfile.write("\\hline  \\hline \n")
outfile.write("- & %.3f & %.3f & %.3f & %.3f \\\ \n"%(media(Epm),incertidumbre(sEpm),media(Enm),incertidumbre(sEnm)))
outfile.write("\\hline\n")
outfile.write("\\end{tabular}")
outfile.write("\\caption{valores medios de la $\Delta E$ por los valores del programa sin $\Delta E_{\max}^{1-2}$.} \n")
outfile.write("\\label{Tab:Em-lab-%d} \n"%(i+1))
outfile.write("\\end{table} \n")     
outfile.close()


# Test estadistico

mEpm=media(Epm)
mEnm=media(Enm)
smEpm=incertidumbre(sEpm)
smEnm=incertidumbre(sEnm)

Og=4.886

def test_student(x,sx,Og):
    tEpm=abs(Og-x)/np.sqrt(sx/np.sqrt(4))
    return tEpm

tEpm=test_student(mEpm,smEpm,Og)
tEnm=test_student(mEnm,smEnm,Og)

print("t_{\min}^{lab} = %.3f"%tEnm)
print("t_{\max}^{lab} = %.3f"%tEpm)


# Printemaos Delta E en función del grado del extremo

plt.figure()
n=[1,2,3,4]
V2=[0.4,0.5,0.6,1,1.5,2]
for i in range(len(En)):
    f=i/6
    color=(0.95-f,0.3-f/3,0.05+f)
    plt.plot(n,En[i],"1",color=color,label="$V_2=%.2f$"%V2[i],
    markersize=10.0,alpha=0.9,markeredgewidth=1.5 )
plt.grid(linestyle="--")
plt.xlabel("n (orden del extremo)")
plt.ylabel("$\Delta E$ (eV)")
plt.legend()
plt.savefig("Extremo-minmos-lab.pdf",bbox_inches="tight")

plt.figure()
n=[1,2,3,4]
V2=[0.4,0.5,0.6,1,1.5,2]
for i in range(len(En)):
    f=i/6
    color=(0.95-f,0.3-f/3,0.05+f)
    plt.plot(n,Ep[i],"1",color=color,label="$V_2=%.2f$"%V2[i],
    markersize=10.0,alpha=0.9,markeredgewidth=1.5 )
plt.grid(linestyle="--")
plt.xlabel("n (orden del extremo)")
plt.ylabel("$\Delta E$ (eV)")
plt.legend()
plt.savefig("Extremo-maximos-lab.pdf",bbox_inches="tight")

