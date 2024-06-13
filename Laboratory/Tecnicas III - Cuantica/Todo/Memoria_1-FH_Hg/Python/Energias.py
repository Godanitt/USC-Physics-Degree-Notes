# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:14:41 2024

@author: danie
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import scipy.constants as cte
import scipy.optimize as so
from Funciones import parabola, sacavalores, aproximaparabolas, energia, Emedia, longitud_onda
from Parabolas import an,san,ap,sap

En,sEn=energia(an, san)
Ep,sEp=energia(ap, sap)

Enm,sEnm=Emedia(En[:,:], sEn[:,:])
Epm,sEpm=Emedia(Ep[:,:], sEp[:,:])

# Regresiones lineales de Delta E respecto el orden del extremo

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
plt.savefig("Extremo-minmos-par.pdf",bbox_inches="tight")

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
plt.savefig("Extremo-maximos-par.pdf",bbox_inches="tight")




outfile=open("Energías-parabolas.txt","w")

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
     outfile.write("\\label{Tab:E-parabola-%d} \n"%(i+1))
     outfile.write("\\end{table} \n")
     outfile.write("\n \n \n")
     
outfile.close()

print(Enm,Epm)

def media(x):
    xm=np.average(x)
    return xm

def incertidumbre(sx):
    sxm=np.sqrt(np.dot(sx,sx)/len(sx)**2)
    return sxm



outfile=open("Energías-medias-parabolas.txt","w")

V2=[0.4,0.5,0.6,1,1.5,2]
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{ccccc} \n")
outfile.write("\\hline $U_2$ (V) & $ \Delta E_{\\max} $ (eV) & $s(\Delta E_{\\max})$ (eV) & $ \Delta E_{\\min} $ (eV) & $s(\Delta E_{\\min})$ (eV) \\\ \\hline \n")
for j in range(len(Enm)):
    outfile.write("%.2f & %.2f & %.2f & %.2f & %.2f \\\ \n"%(V2[j],Epm[j],sEpm[j],Enm[j],sEnm[j]))
outfile.write("\\hline  \\hline \n")
outfile.write("- & %.3f & %.3f & %.3f & %.3f \\\ \n"%(media(Epm),incertidumbre(sEpm),media(Enm),incertidumbre(sEnm)))
outfile.write("\\hline\n")
outfile.write("\\end{tabular}\n")
outfile.write("\\caption{valores medios de la $\Delta E$  usando la aproximación parabólica.} \n")
outfile.write("\\label{Tab:Em-parabola-%d} \n"%(i+1))
outfile.write("\\end{table} \n")
     
outfile.close()


# Sin el primer dato

Enm,sEnm=Emedia(En[:,:], sEn[:,:])
Epm,sEpm=Emedia(Ep[:,1:], sEp[:,1:])

print(Enm,Epm)

outfile=open("Energías-medias-par-sin.txt","w")
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
outfile.write("\\caption{valores medios de la $\Delta E$ por los valores del programa sin $\Delta E_{\max}^{1-2}$.}\n")
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
    tEpm=abs(Og-x)/(np.sqrt(sx/np.sqrt(4)))
    return tEpm

tEpm=test_student(mEpm,smEpm,Og)
tEnm=test_student(mEnm,smEnm,Og)

print("t_{\min}^{par} = %.3f"%tEnm)
print("t_{\max}^{par} = %.3f"%tEpm)
