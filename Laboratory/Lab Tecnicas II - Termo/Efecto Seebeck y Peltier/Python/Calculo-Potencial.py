# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:53:00 2023

@author: danie
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
import modulo_1_aproximador as md







def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y la incertidumbre de y(sig)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=lng.det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(lng.inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb


# EN ESTE PROGRAMA VAMOS A CALCULAR MEDIANTE REGRESIONES LINEALES LA FUERZA ELECTROMOTRIZ Y LA RESISTENCIA



# PRIMERA VEZ
    
Datos1 = np.array([[0.049,100.7],[0.107,92.5],[0.155,86.2],[0.189,81.9],[0.237,75.9],[0.285,70.1],[0.323,65.3],[0.354,61.4],[0.382,58.0],[0.406,55.1],[0.447,50.0]])

V1=Datos1[:,0]
I1=Datos1[:,1]/1000

sV1 = np.array([0.001]*len(V1))

valores1 = ajustelinealponderado(I1, V1, sV1)


E1 = valores1[0]
sE1 = valores1[2]
r1 = valores1[1]
sr1 = valores1[3]

x1 = np.linspace(0, max(I1),100)
y1 = E1+r1*x1


plt.figure()
plt.grid(True, linestyle="--")
plt.plot(x1, y1, "c")
plt.errorbar(I1,V1,sV1,fmt='.', ecolor='blue')
plt.xlabel("I (A)")
plt.ylabel("$\Delta V_{R_x}$ (V)")
plt.xlim(0, max(I1)*1.1)
plt.savefig("I1-vs-V1.png", dpi=500)

# SEGUNDA VEZ

Datos2=np.array([[0.089,140.5],[0.184,125.1],[0.258,118.1],[0.315,111.0],[0.362,104.9],[0.418,98.4],[0.439,94.7],[0.487,89.2],[0.528,84.3],[0.581,77.8],[0.630,71.5],[0.677,65.6]])


V2=Datos2[:,0]
I2=Datos2[:,1]/1000

sV2 = np.array([0.001]*len(V2))

valores2 = ajustelinealponderado(I2, V2, sV2)


E2 = valores2[0]
sE2 = valores2[2]
r2 = valores2[1]
sr2 = valores2[3]

x2 = np.linspace(0, max(I2),100)
y2 = E2+r2*x2


plt.figure()
plt.grid(True, linestyle="--")
plt.plot(x2, y2, "c")
plt.errorbar(I2,V2,sV2,fmt='.', ecolor='blue')
plt.xlabel("I (A)")
plt.ylabel("$\Delta V_{R_x}$ (V)")
plt.xlim(0, max(I2)*1.1)
plt.savefig("I2-vs-V2.png", dpi=500)


#COMPARANDO AMBAS REGRESIONES

plt.figure()
plt.grid(True, linestyle="--")
plt.plot(x1,y1,"cornflowerblue")
plt.plot(x2,y2,"orange")
plt.plot(I1,V1,".", color='blue',label="V =125 $V$")
plt.plot(I2,V2,".", color='darkorange', label="V = 150 $V$")
plt.xlabel("I (A)")
plt.ylabel("$\Delta V_{R_x}$ (V)")
plt.xlim(0.0, max(I2)*1.1)
plt.ylim(0,E2*1.1)
plt.legend(loc="upper right")
plt.savefig("I-vs-V.png", dpi=500)



outfile=open("datos2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\varepsilon \ (V)$ & $s(\\varepsilon) \ (V)$ & $r_i \ (\Omega)$ & $r_i \ (\Omega)$  \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f \\\ \n\\hline\n"%(E1,md.aproximaciondecimales(sE1),r1,md.aproximaciondecimales(sr1)))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores para la fuerza electromotriz y la resistencia V=150V} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()


outfile=open("datos2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\varepsilon \ (V)$ & $s(\\varepsilon) \ (V)$ & $r_i \ (\Omega)$ & $r_i \ (\Omega)$  \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f \\\ \n\\hline\n"%(E2,md.aproximaciondecimales(sE2),r2,md.aproximaciondecimales(sr2)))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores para la fuerza electromotriz y la resistencia V=150V} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()

    
